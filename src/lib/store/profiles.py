# Everything keyed on a single Telegram user: their bot preferences
# (`user_settings`) and their hifz identity (`user_profile`).
#
# Two tables, one repository, because they share a key and a lifecycle: both are
# created on first contact and neither is ever read without the other being
# relevant. They stay separate tables so the pre-hifz settings table keeps its
# shape and an existing deployment needs no data migration.

import abc
from dataclasses import dataclass, replace
from datetime import time
from typing import List, Optional

from ._state import MemoryState


@dataclass
class UserSettingsRow:
  """A row of `user_settings`. Defaults live in `lib.user_settings`, never here —
  this layer stores what it is handed."""

  telegram_user_id: int
  ui_lang: str
  translation_lang: str
  reciter: str


@dataclass
class ProfileRow:
  """A row of `user_profile`.

  `timezone` is a fixed UTC offset as text (`"+05:00"`), not an IANA zone name:
  no tzdata dependency and no DST branches. The column is TEXT so an IANA name
  could be stored later without a migration.

  `current_streak` / `longest_streak` are denormalized from `session_log` for
  cheap reads; `lib.streaks` owns recomputing them.
  """

  telegram_user_id: int
  display_name: Optional[str] = None
  leaderboard_opt_in: bool = False
  timezone: Optional[str] = None
  reminder_time: Optional[time] = None
  current_streak: int = 0
  longest_streak: int = 0


_PROFILE_COLUMNS = ("telegram_user_id, display_name, leaderboard_opt_in, timezone, "
                    "reminder_time, current_streak, longest_streak")
_SETTINGS_COLUMNS = "telegram_user_id, ui_lang, translation_lang, reciter"

# One upsert per single-column profile setter, built once from a closed list of
# column names rather than interpolated at call time — nothing user-supplied ever
# reaches the statement text.
_PROFILE_UPSERT = {
  column: ("INSERT INTO user_profile (telegram_user_id, {c}) VALUES ($1, $2) "
           "ON CONFLICT (telegram_user_id) DO UPDATE SET {c} = EXCLUDED.{c}, "
           "updated_at = now() RETURNING {cols}").format(c=column, cols=_PROFILE_COLUMNS)
  for column in ("display_name", "leaderboard_opt_in", "timezone", "reminder_time")
}


class ProfileStore(abc.ABC):
  """Per-user preferences and hifz profile."""

  # -- user_settings -------------------------------------------------------

  @abc.abstractmethod
  async def get_settings(self, user_id: int) -> Optional[UserSettingsRow]:
    """The user's settings row, or None if they have never been seen."""

  @abc.abstractmethod
  async def ensure_settings_row(self, user_id: int, ui_lang: str, translation_lang: str,
                                reciter: str) -> Optional[UserSettingsRow]:
    """Insert the settings row if absent; return it, or None if it already existed.

    `None` is the "you lost the insert race" signal (`ON CONFLICT DO NOTHING
    RETURNING` yields no row on conflict), which is what lets the caller know
    whether the values it supplied were actually the ones written — the legacy
    Redis migration in `lib.user_settings` depends on that distinction.
    """

  @abc.abstractmethod
  async def set_ui_lang(self, user_id: int, code: str) -> None:
    """Set the interface language. No-op if the row does not exist."""

  @abc.abstractmethod
  async def set_translation_lang(self, user_id: int, code: str) -> None:
    """Set the Qur'an translation language. No-op if the row does not exist."""

  @abc.abstractmethod
  async def set_reciter(self, user_id: int, subfolder: str) -> None:
    """Set the reciter (an everyayah.com subfolder). No-op if the row does not exist."""

  # -- user_profile --------------------------------------------------------

  @abc.abstractmethod
  async def get_profile(self, user_id: int) -> Optional[ProfileRow]:
    """The user's hifz profile, or None if they have no profile row yet."""

  @abc.abstractmethod
  async def ensure_profile(self, user_id: int) -> ProfileRow:
    """Return the profile, creating an all-defaults row first if it is missing."""

  @abc.abstractmethod
  async def set_display_name(self, user_id: int, display_name: Optional[str]) -> ProfileRow:
    """Set the leaderboard display name (creating the profile if needed)."""

  @abc.abstractmethod
  async def set_leaderboard_opt_in(self, user_id: int, opted_in: bool) -> ProfileRow:
    """Opt the user into or out of every leaderboard (creating the profile if needed)."""

  @abc.abstractmethod
  async def set_timezone(self, user_id: int, utc_offset: Optional[str]) -> ProfileRow:
    """Set the fixed UTC offset, e.g. `"+05:00"` (creating the profile if needed)."""

  @abc.abstractmethod
  async def set_reminder_time(self, user_id: int, reminder_time: Optional[time]) -> ProfileRow:
    """Set the local time of day for the daily push (creating the profile if needed)."""

  @abc.abstractmethod
  async def set_streaks(self, user_id: int, current_streak: int,
                        longest_streak: int) -> ProfileRow:
    """Write both denormalized streak counters (creating the profile if needed)."""

  @abc.abstractmethod
  async def list_reminder_profiles(self) -> List[ProfileRow]:
    """Every profile with a reminder time set, ascending by user id.

    The scheduler's per-tick scan: these are the users who can be due for a push.
    """


class InMemoryProfileStore(ProfileStore):
  """Dict-backed `ProfileStore`, used when DATABASE_URL is unset."""

  def __init__(self, state: MemoryState):
    self._state = state

  # -- user_settings -------------------------------------------------------

  async def get_settings(self, user_id):
    row = self._state.user_settings.get(user_id)
    return replace(row) if row is not None else None

  async def ensure_settings_row(self, user_id, ui_lang, translation_lang, reciter):
    if user_id in self._state.user_settings:
      return None
    row = UserSettingsRow(user_id, ui_lang, translation_lang, reciter)
    self._state.user_settings[user_id] = row
    return replace(row)

  async def _set_setting(self, user_id, field, value):
    row = self._state.user_settings.get(user_id)
    if row is not None:                     # UPDATE on a missing row is a no-op in SQL too
      setattr(row, field, value)

  async def set_ui_lang(self, user_id, code):
    await self._set_setting(user_id, "ui_lang", code)

  async def set_translation_lang(self, user_id, code):
    await self._set_setting(user_id, "translation_lang", code)

  async def set_reciter(self, user_id, subfolder):
    await self._set_setting(user_id, "reciter", subfolder)

  # -- user_profile --------------------------------------------------------

  def _profile(self, user_id) -> ProfileRow:
    row = self._state.user_profile.get(user_id)
    if row is None:
      row = ProfileRow(user_id)
      self._state.user_profile[user_id] = row
    return row

  async def get_profile(self, user_id):
    row = self._state.user_profile.get(user_id)
    return replace(row) if row is not None else None

  async def ensure_profile(self, user_id):
    return replace(self._profile(user_id))

  async def set_display_name(self, user_id, display_name):
    row = self._profile(user_id)
    row.display_name = display_name
    return replace(row)

  async def set_leaderboard_opt_in(self, user_id, opted_in):
    row = self._profile(user_id)
    row.leaderboard_opt_in = bool(opted_in)
    return replace(row)

  async def set_timezone(self, user_id, utc_offset):
    row = self._profile(user_id)
    row.timezone = utc_offset
    return replace(row)

  async def set_reminder_time(self, user_id, reminder_time):
    row = self._profile(user_id)
    row.reminder_time = reminder_time
    return replace(row)

  async def set_streaks(self, user_id, current_streak, longest_streak):
    row = self._profile(user_id)
    row.current_streak = int(current_streak)
    row.longest_streak = int(longest_streak)
    return replace(row)

  async def list_reminder_profiles(self):
    rows = [r for r in self._state.user_profile.values() if r.reminder_time is not None]
    rows.sort(key=lambda r: r.telegram_user_id)
    return [replace(r) for r in rows]


class PostgresProfileStore(ProfileStore):
  """asyncpg-backed `ProfileStore`."""

  def __init__(self, pool):
    self._pool = pool

  @staticmethod
  def _settings(record) -> Optional[UserSettingsRow]:
    if record is None:
      return None
    return UserSettingsRow(record["telegram_user_id"], record["ui_lang"],
                           record["translation_lang"], record["reciter"])

  @staticmethod
  def _profile(record) -> Optional[ProfileRow]:
    if record is None:
      return None
    return ProfileRow(
      telegram_user_id=record["telegram_user_id"],
      display_name=record["display_name"],
      leaderboard_opt_in=record["leaderboard_opt_in"],
      timezone=record["timezone"],
      reminder_time=record["reminder_time"],
      current_streak=record["current_streak"],
      longest_streak=record["longest_streak"],
    )

  # -- user_settings -------------------------------------------------------

  async def get_settings(self, user_id):
    return self._settings(await self._pool.fetchrow(
      "SELECT " + _SETTINGS_COLUMNS + " FROM user_settings WHERE telegram_user_id = $1",
      user_id))

  async def ensure_settings_row(self, user_id, ui_lang, translation_lang, reciter):
    return self._settings(await self._pool.fetchrow(
      "INSERT INTO user_settings (telegram_user_id, ui_lang, translation_lang, reciter) "
      "VALUES ($1, $2, $3, $4) ON CONFLICT (telegram_user_id) DO NOTHING "
      "RETURNING " + _SETTINGS_COLUMNS,
      user_id, ui_lang, translation_lang, reciter))

  async def set_ui_lang(self, user_id, code):
    await self._pool.execute(
      "UPDATE user_settings SET ui_lang = $2, updated_at = now() WHERE telegram_user_id = $1",
      user_id, code)

  async def set_translation_lang(self, user_id, code):
    await self._pool.execute(
      "UPDATE user_settings SET translation_lang = $2, updated_at = now() "
      "WHERE telegram_user_id = $1",
      user_id, code)

  async def set_reciter(self, user_id, subfolder):
    await self._pool.execute(
      "UPDATE user_settings SET reciter = $2, updated_at = now() WHERE telegram_user_id = $1",
      user_id, subfolder)

  # -- user_profile --------------------------------------------------------

  async def _upsert(self, user_id, column, value) -> ProfileRow:
    # One statement so a first-contact write never needs a separate ensure round
    # trip; the DO UPDATE branch is what makes it return the row either way.
    return self._profile(await self._pool.fetchrow(_PROFILE_UPSERT[column], user_id, value))

  async def get_profile(self, user_id):
    return self._profile(await self._pool.fetchrow(
      "SELECT " + _PROFILE_COLUMNS + " FROM user_profile WHERE telegram_user_id = $1",
      user_id))

  async def ensure_profile(self, user_id):
    return self._profile(await self._pool.fetchrow(
      "INSERT INTO user_profile (telegram_user_id) VALUES ($1) "
      "ON CONFLICT (telegram_user_id) DO UPDATE SET telegram_user_id = EXCLUDED.telegram_user_id "
      "RETURNING " + _PROFILE_COLUMNS,
      user_id))

  async def set_display_name(self, user_id, display_name):
    return await self._upsert(user_id, "display_name", display_name)

  async def set_leaderboard_opt_in(self, user_id, opted_in):
    return await self._upsert(user_id, "leaderboard_opt_in", bool(opted_in))

  async def set_timezone(self, user_id, utc_offset):
    return await self._upsert(user_id, "timezone", utc_offset)

  async def set_reminder_time(self, user_id, reminder_time):
    return await self._upsert(user_id, "reminder_time", reminder_time)

  async def set_streaks(self, user_id, current_streak, longest_streak):
    return self._profile(await self._pool.fetchrow(
      "INSERT INTO user_profile (telegram_user_id, current_streak, longest_streak) "
      "VALUES ($1, $2, $3) ON CONFLICT (telegram_user_id) DO UPDATE "
      "SET current_streak = EXCLUDED.current_streak, "
      "    longest_streak = EXCLUDED.longest_streak, updated_at = now() "
      "RETURNING " + _PROFILE_COLUMNS,
      user_id, int(current_streak), int(longest_streak)))

  async def list_reminder_profiles(self):
    records = await self._pool.fetch(
      "SELECT " + _PROFILE_COLUMNS + " FROM user_profile "
      "WHERE reminder_time IS NOT NULL ORDER BY telegram_user_id")
    return [self._profile(r) for r in records]
