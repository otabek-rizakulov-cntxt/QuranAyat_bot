import os
import ujson as json
from typing import Optional
from config import RedisSingleton, Environment

class File(Environment):
  redis_namespace = ""
  _performers_cache = None

  def __init__(self):
    self.redis = RedisSingleton().connection

  def _file_key(self, filename: str) -> str:
    """Single source of truth for the Telegram-cache key of a media file."""
    return self.redis_namespace + "file:" + filename

  def save_user(self, chat_id: int, state: tuple[int, int, str]):
    """State is a tuple: (surah, ayah, type). Kept for two days."""
    self.redis.set(self.redis_namespace + str(chat_id),
          json.dumps(state), ex=60 * 60 * 24 * 2)

  def get_user(self, chat_id: int):
    v = self.redis.get(self.redis_namespace + str(chat_id))
    if v is not None:
      return json.loads(v)
    return None

  def _lang_key(self, chat_id: int) -> str:
    return self.redis_namespace + "lang:" + str(chat_id)

  def save_lang(self, chat_id: int, code: str):
    """Persist the user's UI/translation language.

    Stored separately from navigation state and without an expiry, because a
    language choice is a durable preference while (surah, ayah, type) resets
    after two days.
    """
    self.redis.set(self._lang_key(chat_id), code)

  def get_lang(self, chat_id: int):
    """Return the user's saved language code, or None if they haven't chosen one."""
    return self.redis.get(self._lang_key(chat_id))

  def save_file(self, filename: str, file_id: str):
    """Cache the Telegram file_id for a media file so we can skip re-uploading."""
    if not file_id:
      return
    # keep for 2 days; Telegram file_ids are stable far longer, but this bounds staleness
    self.redis.set(self._file_key(filename), file_id, ex=60 * 60 * 24 * 2)

  def get_file(self, filename: str) -> Optional[str]:
    """Return the cached Telegram file_id, or None on a cache miss."""
    return self.redis.get(self._file_key(filename))

  @classmethod
  def _load_performers(cls):
    if cls._performers_cache is None:
      base_dir = os.path.dirname(os.path.dirname(__file__))  # up from lib/ to src/
      file_path = os.path.join(base_dir, "common", "performers.json")
      with open(file_path, "r", encoding="utf-8") as fp:
        cls._performers_cache = json.load(fp)["performers"]
    return cls._performers_cache

  def get_audio_filename(self, surah: int, ayah: int, performer: Optional[str] = "Husary_128kbps") -> str:
    performers = self._load_performers()
    subfolder = next(
      (p["subfolder"] for p in performers if p["subfolder"] == performer),
      None,
    )
    if subfolder is None:
      raise ValueError(f"Unknown performer: {performer}")
    return "{base}/{sub}/{s}{a}.mp3".format(
      base=self.get_env("audio_base_url"),
      sub=subfolder,
      s=str(surah).zfill(3),
      a=str(ayah).zfill(3),
    )

  def get_image_filename(self, s: int, a: int) -> str:
    return self.get_env("quranic_images_file_path") + "/" + str(s) + "_" + str(a) + ".png"
