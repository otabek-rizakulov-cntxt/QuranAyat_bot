from dataclasses import dataclass
from typing import Optional
from config.postgres import get_pool
from .utils import File

DEFAULT_UI_LANG = "en"
DEFAULT_TRANSLATION_LANG = "en"
DEFAULT_RECITER = "Husary_128kbps"

_SELECT = ("SELECT telegram_user_id, ui_lang, translation_lang, reciter "
           "FROM user_settings WHERE telegram_user_id = $1")
_INSERT = ("INSERT INTO user_settings (telegram_user_id, ui_lang, translation_lang, reciter) "
           "VALUES ($1, $2, $3, $4) ON CONFLICT (telegram_user_id) DO NOTHING "
           "RETURNING telegram_user_id, ui_lang, translation_lang, reciter")
_UPDATE = {
  "ui_lang": "UPDATE user_settings SET ui_lang = $2, updated_at = now() WHERE telegram_user_id = $1",
  "translation_lang": "UPDATE user_settings SET translation_lang = $2, updated_at = now() WHERE telegram_user_id = $1",
  "reciter": "UPDATE user_settings SET reciter = $2, updated_at = now() WHERE telegram_user_id = $1",
}


@dataclass
class SettingsRow:
  ui_lang: str
  translation_lang: str
  reciter: str


class UserSettings:
  """Durable per-user preferences (Postgres-backed), replacing the old single
  Redis `lang:<chat_id>` key with three independent settings: UI language,
  translation language, and reciter.

  Keyed by Telegram `telegram_user_id`, not `chat_id`: the bot only serves
  private DMs (group chats are rejected in handle_update), so the two are
  equal there, but the inline-query path only ever has a user id, and keying
  on user id keeps both paths consistent without ever needing to revisit this.
  """

  def __init__(self):
    self._file = File()

  async def get(self, user_id: int, chat_id: Optional[int] = None,
                default_ui_lang: str = DEFAULT_UI_LANG) -> SettingsRow:
    row = await self._ensure_row(user_id, chat_id, default_ui_lang)
    return SettingsRow(row["ui_lang"], row["translation_lang"], row["reciter"])

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
    pool = await get_pool()
    await pool.execute(_UPDATE["ui_lang"], user_id, code)

  async def set_translation_lang(self, user_id: int, chat_id: Optional[int], code: str) -> None:
    await self._ensure_row(user_id, chat_id, DEFAULT_UI_LANG)
    pool = await get_pool()
    await pool.execute(_UPDATE["translation_lang"], user_id, code)

  async def set_reciter(self, user_id: int, chat_id: Optional[int], subfolder: str) -> None:
    await self._ensure_row(user_id, chat_id, DEFAULT_UI_LANG)
    pool = await get_pool()
    await pool.execute(_UPDATE["reciter"], user_id, subfolder)

  async def _ensure_row(self, user_id: int, chat_id: Optional[int],
                        default_ui_lang: str = DEFAULT_UI_LANG) -> dict:
    pool = await get_pool()
    row = await pool.fetchrow(_SELECT, user_id)
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

    row = await pool.fetchrow(_INSERT, user_id, ui_lang, translation_lang, DEFAULT_RECITER)
    if row is None:
      # Lost an insert race to a concurrent call for the same user; re-read.
      row = await pool.fetchrow(_SELECT, user_id)
    elif legacy_lang is not None:
      self._file.delete_lang(chat_id)  # fully superseded now; stop bit-rotting in Redis

    return row
