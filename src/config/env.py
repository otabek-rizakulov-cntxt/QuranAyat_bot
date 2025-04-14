import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Environment:

  @classmethod
  def get_env(self, name: str) -> str:
    TOKEN = os.getenv("TOKEN")
    REDIS_URL = os.getenv("REDIS_HOST_URL")
    AUDIO_BASE_URL = os.getenv("AUDIO_BASE_URL")
    PERFORMERS_FILE_PATH = os.path.join(BASE_DIR, "../common/performers.json")
    QURANIC_IMAGES_FILE_PATH = os.path.join(BASE_DIR, "../quranic_images")
    variable = {
      "token": TOKEN,
      "redis": REDIS_URL,
      "audio_base_url": AUDIO_BASE_URL,
      "performers_file_path": PERFORMERS_FILE_PATH,
      "quranic_images_file_path": QURANIC_IMAGES_FILE_PATH
    }
    return variable[name]
