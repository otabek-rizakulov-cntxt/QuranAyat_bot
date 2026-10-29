"""`File` — the old all-in-one helper, kept as a thin facade.

Its jobs now live in focused modules (docs/REFACTOR_PLAN.md step 4.1):

    infra.catalog        the reciter catalog and every CDN URL
    infra.media_cache    the Telegram file_id cache
    infra.nav_state      where each user stopped reading
    infra.pending_input  the one-turn "next message answers my question" flag

`src/` calls those directly. `File` stays because the tests and `Ctx.file`
still reach these through it; each method just forwards.
"""

from typing import Optional

from config import RedisSingleton
from infra import catalog, media_cache, nav_state, pending_input


class File:
    # Key formats are persistent state; the tests pin them through these.
    redis_namespace = ""

    def __init__(self):
        self.redis = RedisSingleton().connection

    @staticmethod
    def _lang_key(chat_id: int) -> str:
        return "lang:" + str(chat_id)

    @staticmethod
    def _awaiting_key(chat_id: int) -> str:
        return pending_input._key(chat_id)

    # --- reading position ---------------------------------------------------
    async def save_user(self, chat_id: int, state: tuple[int, int, str]):
        await nav_state.save(chat_id, *state)

    async def get_user(self, chat_id: int):
        return await nav_state.get(chat_id)

    # --- legacy language key (read only by lib.user_settings' migration) ------
    def get_lang(self, chat_id: int):
        return self.redis.get(self._lang_key(chat_id))

    def delete_lang(self, chat_id: int):
        self.redis.delete(self._lang_key(chat_id))

    # --- pending input ----------------------------------------------------------
    def set_awaiting_input(self, chat_id: int, kind: str):
        pending_input.expect(chat_id, kind)

    def pop_awaiting_input(self, chat_id: int) -> Optional[str]:
        return pending_input.take(chat_id)

    # --- file_id cache ------------------------------------------------------------
    def save_file(self, filename: str, file_id: str):
        media_cache.save(filename, file_id)

    def get_file(self, filename: str) -> Optional[str]:
        return media_cache.get(filename)

    # --- catalog and URLs -----------------------------------------------------------
    @classmethod
    def _load_performers(cls):
        return catalog.performers()

    @classmethod
    def get_performer_name(cls, subfolder: str) -> str:
        return catalog.performer_name(subfolder)

    @classmethod
    def search_performers(cls, query: str, limit: int = 8) -> list:
        return catalog.search(query, limit)

    @classmethod
    def has_page_audio(cls, subfolder: str) -> bool:
        return catalog.has_page_audio(subfolder)

    def get_audio_filename(
        self, surah: int, ayah: int, performer: Optional[str] = catalog.DEFAULT_RECITER
    ) -> str:
        return catalog.audio_url(surah, ayah, performer)

    def get_page_audio_filename(self, page: int, performer: str) -> str:
        return catalog.page_audio_url(page, performer)

    def get_image_filename(self, s: int, a: int) -> str:
        return catalog.image_url(s, a)

    def get_page_image_filename(self, s: int, a: int) -> str:
        return catalog.page_image_url(s, a)
