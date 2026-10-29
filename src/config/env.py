import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Environment:

  @classmethod
  def get_env(cls, name: str) -> str:
    variables = {
      "token": os.getenv("TOKEN"),
      "redis": os.getenv("REDIS_HOST_URL"),
      "database_url": os.getenv("DATABASE_URL"),
      # Opt-in for the in-memory stores (tests, local dev). Off by default, so a
      # deployment whose database or Redis URL is missing fails instead of
      # silently keeping every user setting in process memory.
      "allow_memory_store": os.getenv("ALLOW_MEMORY_STORE"),
      "audio_base_url": os.getenv("AUDIO_BASE_URL"),
      "quranic_images_file_path": os.getenv("PHOTO_BASE_URL"),
      # Per-ayah images the mushaf-page stitcher tiles. Wants a uniform-width set
      # (everyayah's `quranpngs`, all 1500px wide); PHOTO_BASE_URL may point at a
      # variable-width set that cannot be tiled, so this is configured separately
      # and only falls back to it when unset.
      "page_image_base_url": os.getenv("PAGE_IMAGE_BASE_URL") or os.getenv("PHOTO_BASE_URL"),
      # Mini App API (src/api): HS256 signing key for its access tokens, and the
      # comma-separated browser origins CORS lets call it.
      "miniapp_jwt_secret": os.getenv("MINIAPP_JWT_SECRET"),
      "miniapp_origins": os.getenv("MINIAPP_ORIGINS"),
      # Public URL of the Mini App; turns on the bot's "Open in app" buttons,
      # /app and the menu button (src/lib/miniapp.py).
      "miniapp_url": os.getenv("MINIAPP_URL"),
    }
    if name not in variables:
      raise KeyError(f"Unknown environment variable requested: {name}")
    return variables[name]


def memory_store_allowed() -> bool:
  """Whether the in-memory stores may stand in for Postgres and Redis."""
  value = Environment.get_env("allow_memory_store") or ""
  return value.strip().lower() in ("1", "true", "yes")
