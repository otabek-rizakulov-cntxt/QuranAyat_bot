# BismillahBot -- Explore the Holy Qur'an on Telegram
# Copyright (C) 1436-1438 AH  Rahiel Kasim
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from dotenv import load_dotenv
load_dotenv()
import re
import os
import sys
import asyncio
import telegram
import ujson as json
from time import sleep, time
from typing import Tuple
from redis import StrictRedis
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.constants import MessageLimit
from telegram.error import NetworkError, TelegramError, Forbidden, Conflict
from bismillahbot import Quran, make_index

TOKEN = os.getenv("TOKEN")
REDIS_HOST_URL = os.getenv("REDIS_HOST_URL")

r = StrictRedis.from_url(REDIS_HOST_URL)

redis_namespace = ""
update_id = None

def message_to_dict(message):
    if isinstance(message, str):
        return { 'message': message }
    return {
        'audio': {
            'duration': message.audio.duration,
            'file_id': message.audio.file_id,
            'file_name': message.audio.file_name,
            'file_size': message.audio.file_size,
            'file_unique_id': message.audio.file_unique_id,
            'mime_type': message.audio.mime_type,
            'performer': message.audio.performer,
            'title': message.audio.title
            },
        'channel_chat_created': message.channel_chat_created,
        'chat': {
            'first_name': message.chat.first_name,
            'id': message.chat.id,
            'type': message.chat.type,
            'username': message.chat.username
            },
        'date': message.date.isoformat(),
        'delete_chat_photo': message.delete_chat_photo,
        'from_user': {
            'first_name': message.from_user.first_name,
            'id': message.from_user.id,
            'is_bot': message.from_user.is_bot,
            'username': message.from_user.username
            },
        'group_chat_created': message.group_chat_created,
        'message_id': message.message_id,
        'supergroup_chat_created': message.supergroup_chat_created
    } # Convert the Message object to a dictionary message_dict = message_to_dict(message)

def save_user(chat_id: int, state: Tuple[int, int, str]):
    """State is a tuple: (surah, ayah, type)"""
    r.set(redis_namespace + str(chat_id),
          json.dumps(state), ex=60 * 60 * 24 * 2)  # keep state for two days for making it month add 31 instead of 2


def get_user(chat_id: int):
    v = r.get(redis_namespace + str(chat_id))
    if v is not None:
        return json.loads(v)


def save_file(filename: str, file_id: str):
    message = ''
    try:
        message = message_to_dict(file_id)
    except Exception as err:
        message = ''
        print("Error on save file", err)
    r.set(redis_namespace + "file:" + filename,
          json.dumps(message), ex=60 * 60 * 24 * 2)  # keep for 2 days for making it month add 31 instead of 2


def get_file(filename: str):
    f = r.get(redis_namespace + "file:" + filename)
    if f is not None:
        return json.loads(f)


def get_audio_filename(performer: str, surah: int, ayah: int) -> str:
    return 'Husary/' + str(surah).zfill(3) + str(ayah).zfill(3) + ".mp3"


def get_image_filename(surah: int, ayah: int) -> str:
    return "quranic_images/" + str(surah) + "_" + str(ayah) + ".png"


async def send_file(bot, filename, quran_type, **kwargs):
    """Tries to send file from Telegram's cache, only uploads from disk if necessary.
    Always saves the Telegram cache file_id in Redis and returns it.
    """

    async def upload(f):
        if quran_type == "arabic":
            result = await bot.send_photo(photo=f, **kwargs)
            v = result["photo"][-1]["file_id"]
        elif quran_type == "audio":
            result = await bot.send_audio(audio=f, **kwargs)
            await bot.get_updates()

            v = result["audio"]["file_id"]
        save_file(filename, v)
        return v

    async def upload_from_disk():
        with open(filename, "rb") as f:
            return await upload(f)

    f = get_file(filename) 
    # or "https://www.everyayah.com/data/Husary_128kbps/001001.mp3"
    if f is not None:
        try:
            return await upload(f)
        except telegram.error.TelegramError as e:
            if "file_id" in e.message:
                return await upload_from_disk()
            else:
                raise e
    else:
        return await upload_from_disk()


def get_default_query_results(quran: Quran):
    results = []
    ayat = [
        (13, 28), (33, 56), (2, 62), (10, 31), (17, 36), (5, 32), (39, 9), (17, 44), (28, 88), (17, 84), (33, 6),
        (7, 57), (3, 7), (2, 255), (63, 9), (57, 20), (49, 12), (16, 125), (24, 35), (73, 8), (4, 103)
    ]
    for s, a in ayat:
        ayah = "%d:%d" % (s, a)
        english = quran.get_ayah(s, a)
        results.append(InlineQueryResultArticle(
            ayah + "def", title=ayah,
            description=english[:120],
            input_message_content=InputTextMessageContent(english))
        )
    return results



async def main():
    global update_id
    bot = telegram.Bot(token=TOKEN)

    try:
        result = await bot.get_updates()
        update_id = result[0].update_id
    except IndexError:
        update_id = None

    interface = telegram.ReplyKeyboardMarkup(
        [["Arabic", "Audio", "English", "Tafsir"],
         ["Previous", "Random", "Next"]],
        resize_keyboard=True)

    data = {
        "english": Quran("translation"),
        "tafsir": Quran("tafsir"),
        "index": make_index(),
        "interface": interface
    }
    data["default_query_results"] = get_default_query_results(data["english"])

    while True:
        try:
            await serve(bot, data)
        except NetworkError:
            sleep(1)
        except Conflict as e:
            print(f"Conflict error: {e}. Retrying in 5 seconds...")
            sleep(5)
        except Forbidden:  # user has removed or blocked the bot
            print('is forbidden ')
            update_id += 1
        except TelegramError as e:
            if "Invalid server response" in str(e):
                sleep(3)
            else:
                print("Error in main ", e)
                raise e


async def serve(bot, data):
    global update_id

    async def send_quran(performer: str, surah: int, ayah: int, quran_type: str, chat_id: int, reply_markup=None):
        if quran_type in ("english", "tafsir"):
            text = data[quran_type].get_ayah(surah, ayah)
            await bot.send_message(chat_id=chat_id, text=text[:4096],
                             reply_markup=reply_markup)
        elif quran_type == "arabic":
            await bot.send_chat_action(chat_id=chat_id,
                                 action=telegram.constants.ChatAction.UPLOAD_PHOTO)
            image = get_image_filename(surah, ayah)
            await send_file(bot, image, quran_type, chat_id=chat_id,
                      caption="Quran %d:%d" % (surah, ayah),
                      reply_markup=reply_markup)
        elif quran_type == "audio":
            await bot.send_chat_action(chat_id=chat_id,
                                 action=telegram.constants.ChatAction.UPLOAD_DOCUMENT)
            audio = get_audio_filename(performer, surah, ayah)
            await send_file(bot, audio, quran_type, chat_id=chat_id,
                      performer="Shaykh Mahmoud Khalil al-Husary",
                      title="Quran %d:%d" % (surah, ayah),
                      reply_markup=reply_markup)
        save_user(chat_id, (surah, ayah, quran_type))

    for update in await bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.inline_query:
            query_id = update.inline_query.id
            query = update.inline_query.query
            results = []
            cache_time = 66 * (60 ** 2 * 24)
            surah, ayah = parse_ayah(query)
            if surah is not None and Quran.exists(surah, ayah):
                ayah = "%d:%d" % (surah, ayah)
                english = data["english"].get_ayah(surah, ayah)
                tafsir = data["tafsir"].get_ayah(surah, ayah)
                results.append(InlineQueryResultArticle(
                    ayah + "english", title="English",
                    description=english[:120],
                    input_message_content=InputTextMessageContent(english))
                )
                results.append(InlineQueryResultArticle(
                    ayah + "tafsir", title="Tafsir",
                    description=tafsir[:120],
                    input_message_content=InputTextMessageContent(tafsir))
                )
            else:
                results = data["default_query_results"]
            bot.answer_inline_query(inline_query_id=query_id, cache_time=cache_time, results=results)
            continue

        if not update.message or not update.message.text:  # updates without text
            continue

        chat_id = update.message.chat_id
        message = update.message.text.lower()
        state = get_user(chat_id)
        if state is not None:
            surah, ayah, quran_type = state
        else:
            surah, ayah, quran_type = 1, 1, "english"

        print("%d:%.3f:%s" % (chat_id, time(), message.replace("\n", " ")))

        if chat_id < 0:
            continue            # bot should not be in a group

        if message.startswith("/"):
            command = message[1:]
            if command in ("start", "help"):
                text = ("Send me the numbers of a surah and ayah, for example:"
                        " <b>2:255</b>. Then I respond with that ayah from the Holy "
                        "Quran. Type /index to see all Surahs or try /random. "
                        "I'm available in any chat on Telegram, just type: <b>@BismillahBot</b>\n\n"
                        "For audio tracks of complete Surahs, talk to @AudioQuranBot.")
            elif command == "about":
                text = ("The English translation is by Imam Ahmed Raza from "
                        "tanzil.net/trans/. The audio is a recitation by "
                        "Shaykh Mahmoud Khalil al-Husary from everyayah.com. "
                        "The tafsir is Tafsir al-Jalalayn from altafsir.com."
                        "The source code of BismillahBot is available at: "
                        "https://github.com/rahiel/BismillahBot.")
            elif command == "index":
                text = data["index"]
            else:
                text = None  # "Invalid command"

            if text:
                await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
                continue

        if message in ("english", "tafsir", "audio", "arabic"):
            await send_quran("performer", surah, ayah, message, chat_id)
            continue
        elif message in ("next", "previous", "random", "/random"):
            if message == "next":
                surah, ayah = Quran.get_next_ayah(surah, ayah)
            elif message == "previous":
                surah, ayah = Quran.get_previous_ayah(surah, ayah)
            elif message in ("random", "/random"):
                surah, ayah = Quran.get_random_ayah()
            await send_quran("performer", surah, ayah, quran_type, chat_id)
            continue

        surah, ayah = parse_ayah(message)
        if surah:
            if Quran.exists(surah, ayah):
                await send_quran("performer", surah, ayah, quran_type, chat_id, reply_markup=data["interface"])
            else:
                await bot.send_message(chat_id=chat_id, text="Ayah does not exist!")

    sys.stdout.flush()


def parse_ayah(message: str):
    match = re.match("/?(\d+)[ :\-;.,]*(\d*)", message)
    if match is not None:
        surah = int(match.group(1))
        ayah = int(match.group(2)) if match.group(2) else 1
        return surah, ayah
    else:
        return None, None


if __name__ == "__main__":
    print("Server has been started")
    try:
        asyncio.run(main())
    except Exception as e:
        print("Error occurred", e)
        raise e