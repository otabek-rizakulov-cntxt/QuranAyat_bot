import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Environment:

  @classmethod
  def get_env(cls, name: str) -> str:
    variables = {
      "token": os.getenv("TOKEN"),
      "redis": os.getenv("REDIS_HOST_URL"),
      "database_url": os.getenv("DATABASE_URL"),
      "audio_base_url": os.getenv("AUDIO_BASE_URL"),
      "quranic_images_file_path": os.getenv("PHOTO_BASE_URL"),
      # Per-ayah images the mushaf-page stitcher tiles. Wants a uniform-width set
      # (everyayah's `quranpngs`, all 1500px wide); PHOTO_BASE_URL may point at a
      # variable-width set that cannot be tiled, so this is configured separately
      # and only falls back to it when unset.
      "page_image_base_url": os.getenv("PAGE_IMAGE_BASE_URL") or os.getenv("PHOTO_BASE_URL"),
    }
    if name not in variables:
      raise KeyError(f"Unknown environment variable requested: {name}")
    return variables[name]
