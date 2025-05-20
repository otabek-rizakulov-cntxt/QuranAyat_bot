import ujson as json
from typing import Optional
from config import RedisSingleton, Environment

class File(Environment):
  redis_namespace = ""

  def __init__(self):
    self.redis = RedisSingleton().connection

  def message_to_dict(self, file):
    """Parse file data to store in redis db."""
    if isinstance(file, str):
      return { 'file': file }
    return {
      'audio': {
        'title': file.audio.title,
        'file_id': file.audio.file_id,
        'duration': file.audio.duration,
        'file_name': file.audio.file_name,
        'file_size': file.audio.file_size,
        'mime_type': file.audio.mime_type,
        'performer': file.audio.performer,
        'file_unique_id': file.audio.file_unique_id,
        },
      'channel_chat_created': file.channel_chat_created,
      'chat': {
        'id': file.chat.id,
        'type': file.chat.type,
        'username': file.chat.username,
        'first_name': file.chat.first_name,
        },
      'date': file.date.isoformat(),
      'delete_chat_photo': file.delete_chat_photo,
      'from_user': {
        'id': file.from_user.id,
        'is_bot': file.from_user.is_bot,
        'username': file.from_user.username,
        'first_name': file.from_user.first_name,
        },
      'message_id': file.message_id,
      'group_chat_created': file.group_chat_created,
      'supergroup_chat_created': file.supergroup_chat_created
    }

  def save_user(self, chat_id: int, state: tuple[int, int, str]):
    """State is a tuple: (surah, ayah, type)"""
    self.redis.set(self.redis_namespace + str(chat_id),
          json.dumps(state), ex=60 * 60 * 24 * 2)  # keep state for two days for making it month add 31 instead of 2

  def get_user(self, chat_id: int):
    v = self.redis.get(self.redis_namespace + str(chat_id))
    if v is not None:
      return json.loads(v)

  def save_file(self, filename: str, file_id: str):
    message = ''
    try:
      message = self.message_to_dict(file_id)
    except Exception as err:
      message = ''
      print("Error", err)
    # keep for 2 days for making it month add 31 instead of 2
    self.redis.set(filename, json.dumps(message), ex=60 * 60 * 24 * 2)

  def get_file(self, filename: str):
    f = self.redis.get(self.redis_namespace + "file:" + filename)
    if f is not None:
      return json.loads(f)
    return filename

  def get_audio_filename(self, surah: int, ayah: int, performer: Optional[str] = "Husary_128kbps") -> str:
    with open(self.get_env("performers_file_path")) as file:
      data = json.load(file)
      performers = data["performers"]
      for perform in performers:
        if perform["subfolder"] == performer:
          perf = perform["subfolder"]
      file = self.get_env("audio_base_url") + "/" + perf + "/" + str(surah).zfill(3) + str(ayah).zfill(3) + ".mp3"
      return file
    return ""

  def get_image_filename(self, s: int, a: int) -> str:
    return self.get_env("quranic_images_file_path") + "/" + str(s) + "_" + str(a) + ".png"
