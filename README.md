# BismillahBot

بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

BismillahBot is a bot on Telegram to explore the Holy Qur'an.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Usage](#usage)
- [Languages](#languages)
- [Installation](#installation)
    - [Configuration](#configuration)
    - [Running](#running)
    - [Updating](#updating)
- [License](#license)

<!-- markdown-toc end -->

# Usage

Use the bot by messaging [Bismillahbot][] on [Telegram][]. For every verse the
bot has an English translation from [Imam Ahmad Raza][], audio recitation
by [Shaykh Mahmoud Khalil al-Husary][], and exegesis (tafsir)
from [Tafsir al-Jalalayn][]. The translation, tafsir, rendered Arabic ayah and
audio recitation are all available anywhere on Telegram via [inline mode][], just
start a text with `@BismillahBot` (for example, type `@BismillahBot 1:1` in any
chat). A range works too — `@BismillahBot 59:22-24` covers all three ayahs, with
the recitation stitched into a single audio file — as does typing a reciter's name
instead of a reference (`@BismillahBot sudais`), which offers to switch your
recitation. A conversation looks like:
![example]

You can also read by the **page of the mushaf** rather than verse by verse. `/page
255` sends that whole page as one image — assembled from its ayahs, since
everyayah.com has no full-page image — under a 1–604 pager, with the page's
recitation one tap away rather than attached. `/juz 30` opens the page reader at the
start of that juz, and `/sajda` lists the fifteen verses of prostration. A bare
`/page` or `/juz` opens wherever you already are.

Pick your reciter with `/reciter`. The picker groups the ~80-entry catalog into
three labelled tabs, because they are not the same kind of recording:

- **Reciters** (68) — ordinary Arabic recitation.
- **Riwāyah** (3) — the Warsh reading, which *differs from the Ḥafṣ text* shown in
  the Arabic and translations here, so the audio will not always match the screen.
- **Meaning** (8) — not recitation at all, but the translated meaning read aloud.

Choosing from either of the last two tells you so at the moment you choose. Each tab
pages with Previous/Next, every button carries the recording's bitrate so you can
weigh audio quality against storage, and the search button jumps straight to a name
(`sudais 192` narrows to one entry).

**Your language never changes your audio.** `/language` and `/translation` set the
interface and the translation text; only `/reciter` decides what you hear, so the
Qur'an is always recited in Arabic unless you deliberately pick otherwise.

Also see [AudioQuranBot][], a bot that sends audio files of complete surahs.

[BismillahBot]: https://telegram.me/BismillahBot
[Telegram]: https://telegram.org/
[Imam Ahmad Raza]: https://en.wikipedia.org/wiki/Ahmed_Raza_Khan_Barelvi
[Shaykh Mahmoud Khalil al-Husary]: https://en.wikipedia.org/wiki/Mahmoud_Khalil_Al-Hussary
[Tafsir al-Jalalayn]: http://www.altafsir.com/Al-Jalalayn.asp
[inline mode]: https://telegram.org/blog/inline-bots
[example]: https://i.imgur.com/kITXcHz.png "Example conversation"
[AudioQuranBot]: https://github.com/rahiel/AudioQuranBot

# Languages

The bot is multilingual. Send `/language` to choose from 48 languages; the
menus, buttons, error messages, and the verse translation then follow that
choice. On first contact the interface auto-detects your Telegram language
(falling back to English), and you can change it any time.

Every one of the 48 languages has a complete UI string table in
`src/locales/<code>.py` — no language falls back to English for any interface
text. `python3 scripts/check_locales.py` verifies that: it checks each locale
defines every key, keeps the same `{placeholders}` as English, balances its
HTML tags, advertises every slash command in its `/start` message, and that each
localized button label still maps back to the right action.

The `/start` command list is not part of the translated text: `BOT_COMMANDS` in
`src/locales/__init__.py` is the single source of truth for both the `/start`
message and Telegram's command menu, so adding a command surfaces it in all 48
languages at once — a locale only translates the one-line description
(`cmd_*`). Telegram's per-language slash-command menu only accepts two-letter
ISO 639-1 codes, so `uz-Cyrl` and `ber` see the English command menu while the
rest of their interface is localized.

Uzbek is offered in both **Cyrillic** (Ўзбекча) and **Latin** (Oʻzbekcha)
scripts — the Latin text is produced by deterministic transliteration of the
Cyrillic edition. Translations are sourced from [tanzil.net][] via the
[alquran.cloud][] API and bundled under `translations/`; each edition and
translator is listed in [ATTRIBUTIONS.md](ATTRIBUTIONS.md) (review each
translation's licence before public distribution). The tafsir remains English.

Only English is parsed at startup; every other language is loaded on first use
and cached, keeping memory proportional to the languages actually used. To
refresh or extend the bundled set, edit `src/locales/languages.py` and run
`python3 scripts/bundle_translations.py`.

[tanzil.net]: https://tanzil.net
[alquran.cloud]: https://alquran.cloud

# Installation

You can run your own instance of BismillahBot. First request a
[bot username and token](https://core.telegram.org/bots#3-how-do-i-create-a-bot)
from the [BotFather](https://telegram.me/botfather), and disable group chats for
the bot with the `/setjoingroups` command. The bot is a
[FastAPI](https://fastapi.tiangolo.com/) app that receives updates over a
Telegram **webhook** (it never polls), so it needs a public HTTPS URL.

Get the code and install the dependencies in a virtualenv:

```bash
git clone https://github.com/rahiel/BismillahBot.git
cd BismillahBot/
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt --upgrade
```

## Configuration

Configuration is read from environment variables (loaded from a local `.env` in
development). Copy the template and fill it in:

```bash
cp .env.example .env
```

| Variable         | Purpose                                                              |
|------------------|---------------------------------------------------------------------|
| `TOKEN`          | Telegram bot token from the BotFather                               |
| `REDIS_HOST_URL` | Redis URL for user state + the media file-id cache (falls back to an in-memory store if unset) |
| `AUDIO_BASE_URL` | Base URL of the recitation mp3s (e.g. an everyayah.com mirror/CDN)  |
| `PHOTO_BASE_URL` | Base URL of the Arabic ayah images                                 |
| `PAGE_IMAGE_BASE_URL` | Base URL of the per-ayah images `/page` tiles into a page. Needs a **uniform-width** set (everyayah's `quranpngs`, all 1500px); falls back to `PHOTO_BASE_URL` |
| `WEBHOOK_URL`    | Public HTTPS base URL Telegram POSTs updates to; the webhook is registered as `WEBHOOK_URL` + `/webhook/` + `TOKEN`. Also where Telegram fetches stitched range recitations from (`/media/range.mp3`), so inline range audio is only offered when it is set |

Media (audio + images) is fetched from the configured CDN base URLs at runtime,
so no local media download is required. The Qur'an text corpora that ship in the
repo — `quran-data.xml` (surah metadata), `Al_Jalalain_Eng.txt` (tafsir), and
the per-language files under `translations/` — are all the bot needs on disk.

## Running

Run the webhook app with [uvicorn](https://www.uvicorn.org/) from the repo root
(the same command the `Procfile` and `Dockerfile` use):

```bash
uvicorn main:app --app-dir src --host 0.0.0.0 --port 8000
```

On startup the bot registers its webhook with Telegram and loads the corpora in
the background, so it starts serving `/` (health check) immediately. A container
image is also provided:

```bash
docker build -t quranayat-bot .
docker run --env-file .env -p 8000:8000 quranayat-bot
```

## Updating

The bot (and dependencies) can be updated by running the following in its
directory:

```bash
git pull
. venv/bin/activate
pip install -r requirements.txt -U
```

# License

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.
