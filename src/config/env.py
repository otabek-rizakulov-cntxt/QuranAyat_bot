import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Environment:

  @classmethod
  def get_env(cls, name: str) -> str:
    variables = {
      "token": os.getenv("TOKEN"),
      "redis": os.getenv("REDIS_HOST_URL"),
      "audio_base_url": os.getenv("AUDIO_BASE_URL"),
      "quranic_images_file_path": os.getenv("PHOTO_BASE_URL"),
    }
    if name not in variables:
      raise KeyError(f"Unknown environment variable requested: {name}")
    return variables[name]
