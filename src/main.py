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
import sys
import asyncio
import telegram
from time import sleep, time
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.error import NetworkError, TelegramError, Forbidden
from modules import Quran, make_index
from lib.utils import File
from modules import Bot

update_id = None

async def send_file(bot, filename, quran_type, **kwargs):
    """Tries to send file from Telegram's cache, only uploads from disk if necessary.
    Always saves the Telegram cache file_id in Redis and returns it.
    """
    file = File()
    async def upload(f):
        if quran_type == "arabic":
            result = await bot.send_photo(photo=f, **kwargs)
            v = result["photo"][-1]["file_id"]
        elif quran_type == "audio":
            result = await bot.send_audio(audio=f, **kwargs)
            await bot.get_updates()

            v = result["audio"]["file_id"]
        file.save_file(filename, v)
        return v

    async def upload_from_disk():
        with open(filename, "rb") as f:
            return await upload(f)

    f = file.get_file(filename)["file"]
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
    bot = Bot.get_instance()

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
        except Forbidden:  # user has removed or blocked the bot
            update_id += 1
        except TelegramError as e:
            if "Invalid server response" in str(e):
                sleep(3)
            else:
                print("Error ", e)


async def serve(bot, data):
    global update_id
    file = File()
    async def send_quran(surah: int, ayah: int, quran_type: str, chat_id: int, performer: str, reply_markup=None):
        if quran_type in ("english", "tafsir"):
            text = data[quran_type].get_ayah(surah, ayah)
            await bot.send_message(chat_id=chat_id, text=text[:4096],
                            reply_markup=reply_markup)
        elif quran_type == "arabic":
            await bot.send_chat_action(chat_id=chat_id,
                                action=telegram.constants.ChatAction.UPLOAD_PHOTO)
            image = file.get_image_filename(surah, ayah)
            await send_file(bot, image, quran_type, chat_id=chat_id,
                      caption="Quran %d:%d" % (surah, ayah),
                      reply_markup=reply_markup)
        elif quran_type == "audio":
            await bot.send_chat_action(chat_id=chat_id,
                                action=telegram.constants.ChatAction.UPLOAD_DOCUMENT)
            audio = file.get_audio_filename(surah, ayah, performer)
            await send_file(bot, audio, quran_type, chat_id=chat_id,
                      performer="Shaykh Mahmoud Khalil al-Husary",
                      title="Quran %d:%d" % (surah, ayah),
                      reply_markup=reply_markup)
        file.save_user(chat_id, (surah, ayah, quran_type))

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

        chat_id = update.message.chat.id
        message = update.message.text.lower()
        state = file.get_user(chat_id)
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
            await send_quran(surah, ayah, message, chat_id, "Husary_128kbps")
            continue
        elif message in ("next", "previous", "random", "/random"):
            if message == "next":
                surah, ayah = Quran.get_next_ayah(surah, ayah)
            elif message == "previous":
                surah, ayah = Quran.get_previous_ayah(surah, ayah)
            elif message in ("random", "/random"):
                surah, ayah = Quran.get_random_ayah()
            await send_quran(surah, ayah, quran_type, chat_id, "Husary_128kbps")
            continue

        surah, ayah = parse_ayah(message)
        if surah:
            if Quran.exists(surah, ayah):
                await send_quran(surah, ayah, quran_type, chat_id, "Husary_128kbps", reply_markup=data["interface"])
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