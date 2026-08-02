from dataclasses import dataclass
from typing import Optional
from .store import get_store
from .store.profiles import UserSettingsRow
from .utils import File

DEFAULT_UI_LANG = "en"
DEFAULT_TRANSLATION_LANG = "en"
DEFAULT_RECITER = "Husary_128kbps"


@dataclass
class SettingsRow:
  ui_lang: str
  translation_lang: str
  reciter: str


class UserSettings:
  """Durable per-user preferences, replacing the old single Redis `lang:<chat_id>`
  key with three independent settings: UI language, translation language, and
  reciter.

  Keyed by Telegram `telegram_user_id`, not `chat_id`: the bot only serves
  private DMs (group chats are rejected in handle_update), so the two are
  equal there, but the inline-query path only ever has a user id, and keying
  on user id keeps both paths consistent without ever needing to revisit this.

  Persistence lives in `lib.store.profiles`; this class holds no SQL. The one
  thing it does still own is the legacy Redis read/delete around row creation —
  the store layer has no business knowing Redis exists, and the migration is a
  property of *this* module's history, not of the settings table.
  """

  def __init__(self):
    self._file = File()

  async def get(self, user_id: int, chat_id: Optional[int] = None,
                default_ui_lang: str = DEFAULT_UI_LANG) -> SettingsRow:
    row = await self._ensure_row(user_id, chat_id, default_ui_lang)
    return SettingsRow(row.ui_lang, row.translation_lang, row.reciter)

  async def set_ui_lang(self, user_id: int, chat_id: Optional[int], code: str) -> None:
    # Seeding the row with `code` rather than the global default is deliberate,
    # and is why this setter differs from the two below: if this is the first
    # thing we ever learn about the user, picking a UI language is also our best
    # guess at their translation language (the same coupling the legacy migration
    # applies). Choosing a translation language or a reciter says nothing about
    # the other settings, so those seed from the default instead.
    # In practice handle_update always resolves settings — creating the row —
    # before any setter runs, so this only governs direct API use.
    await self._ensure_row(user_id, chat_id, code)
    store = await get_store()
    await store.profiles.set_ui_lang(user_id, code)

  async def set_translation_lang(self, user_id: int, chat_id: Optional[int],
                                 code: str) -> None:
    await self._ensure_row(user_id, chat_id, DEFAULT_UI_LANG)
    store = await get_store()
    await store.profiles.set_translation_lang(user_id, code)

  async def set_reciter(self, user_id: int, chat_id: Optional[int],
                        subfolder: str) -> None:
    await self._ensure_row(user_id, chat_id, DEFAULT_UI_LANG)
    store = await get_store()
    await store.profiles.set_reciter(user_id, subfolder)

  async def _ensure_row(self, user_id: int, chat_id: Optional[int],
                        default_ui_lang: str = DEFAULT_UI_LANG) -> UserSettingsRow:
    store = await get_store()
    row = await store.profiles.get_settings(user_id)
    if row is not None:
      return row

    # First contact for this user_id: migrate the legacy single-value Redis
    # language (if any) into both ui_lang and translation_lang, preserving
    # today's coupled behavior for existing users' first post-migration read.
    # Inline-query callers pass chat_id=None and skip this fallback — there is
    # no pre-existing chat to read a legacy value from. Absent a legacy value,
    # fall back to the caller-supplied default (typically derived from the
    # Telegram client's language_code on first-ever contact).
    legacy_lang = self._file.get_lang(chat_id) if chat_id is not None else None

    ui_lang = legacy_lang or default_ui_lang
    translation_lang = legacy_lang or default_ui_lang

    row = await store.profiles.ensure_settings_row(user_id, ui_lang, translation_lang,
                                                   DEFAULT_RECITER)
    if row is None:
      # Lost an insert race to a concurrent call for the same user; re-read.
      row = await store.profiles.get_settings(user_id)
    elif legacy_lang is not None:
      self._file.delete_lang(chat_id)  # fully superseded now; stop bit-rotting in Redis

    if row is None:
      # The re-read missed too — the row was deleted between the insert and the
      # select. Vanishingly unlikely, but every caller dereferences what comes
      # back, so answer with the values we tried to write instead of a None that
      # would surface as an AttributeError three frames up.
      row = UserSettingsRow(user_id, ui_lang, translation_lang, DEFAULT_RECITER)

    return row
