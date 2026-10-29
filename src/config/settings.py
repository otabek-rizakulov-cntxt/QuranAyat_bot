"""Typed configuration, read from the environment (see .env.example).

`get_settings()` builds a fresh, frozen `Settings` on every call: reading a dozen
variables is cheap, and it keeps the value live for code (and tests) that change
the environment after import. Attribute access means a misspelt setting fails
at the call site instead of returning None.
"""

import os
from dataclasses import dataclass
from typing import Optional, Tuple


def _flag(value: Optional[str]) -> bool:
    return (value or "").strip().lower() in ("1", "true", "yes")


@dataclass(frozen=True)
class Settings:
    token: Optional[str]
    redis_url: Optional[str]
    database_url: Optional[str]
    audio_base_url: Optional[str]
    photo_base_url: Optional[str]
    # Per-ayah images the mushaf-page stitcher tiles. Wants a uniform-width set
    # (everyayah's `quranpngs`, all 1500px wide); the photo base URL may point at a
    # variable-width set that cannot be tiled, so this is configured separately
    # and only falls back to it when unset.
    page_image_base_url: Optional[str]
    # Mini App API (src/api): HS256 signing key for its access tokens, and the
    # browser origins CORS lets call it.
    miniapp_jwt_secret: Optional[str]
    miniapp_origins: Tuple[str, ...]
    # Public URL of the Mini App; turns on the bot's "Open in app" buttons, /app
    # and the menu button (src/lib/miniapp.py).
    miniapp_url: Optional[str]
    # Opt-in for the in-memory stores (tests, local dev). Off by default, so a
    # deployment whose database or Redis URL is missing fails instead of
    # silently keeping every user setting in process memory.
    allow_memory_store: bool
    webhook_url: Optional[str]
    railway_public_domain: Optional[str]

    @classmethod
    def from_env(cls) -> "Settings":
        env = os.environ.get
        return cls(
            token=env("TOKEN"),
            redis_url=env("REDIS_HOST_URL"),
            database_url=env("DATABASE_URL"),
            audio_base_url=env("AUDIO_BASE_URL"),
            photo_base_url=env("PHOTO_BASE_URL"),
            page_image_base_url=env("PAGE_IMAGE_BASE_URL") or env("PHOTO_BASE_URL"),
            miniapp_jwt_secret=env("MINIAPP_JWT_SECRET"),
            miniapp_origins=tuple(
                o.strip() for o in (env("MINIAPP_ORIGINS") or "").split(",") if o.strip()
            ),
            miniapp_url=env("MINIAPP_URL"),
            allow_memory_store=_flag(env("ALLOW_MEMORY_STORE")),
            webhook_url=env("WEBHOOK_URL"),
            railway_public_domain=env("RAILWAY_PUBLIC_DOMAIN"),
        )

    @property
    def webhook_base_url(self) -> Optional[str]:
        """Public HTTPS base URL this app is reachable at.

        Telegram POSTs updates here, and it is also where Telegram fetches the
        stitched range recitations from (see bot.media.RANGE_AUDIO_PATH), so it is
        needed by the bot logic and not only at startup. An explicit webhook URL
        wins; otherwise Railway's auto-injected public domain (host only, so
        https:// is prepended).
        """
        if self.webhook_url:
            return self.webhook_url.rstrip("/")
        if self.railway_public_domain:
            return "https://" + self.railway_public_domain.rstrip("/")
        return None


def get_settings() -> Settings:
    return Settings.from_env()
