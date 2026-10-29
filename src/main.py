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
"""Webhook entrypoint: Telegram pushes updates to us; we never poll.

Run with: uvicorn main:app --host 0.0.0.0 --port 8000

Required env vars (see .env.example):
  TOKEN                  Telegram bot token
  REDIS_HOST_URL         Redis connection URL (nav state + media file-id cache)
  DATABASE_URL           Postgres connection URL (durable per-user settings)
  AUDIO_BASE_URL         base URL for recitation mp3s
  PHOTO_BASE_URL         base URL/path for Arabic ayah images
  WEBHOOK_URL            public HTTPS base URL Telegram should POST updates to;
                         the webhook is registered as WEBHOOK_URL + "/webhook/" + TOKEN
"""

from dotenv import load_dotenv

from config.logging import setup_logging

# Before anything reads the environment or logs.
load_dotenv()
setup_logging()

from app.factory import create_app  # noqa: E402

app = create_app()


# --- Compatibility re-exports (refactor step 1.6 removes this block) ----------
# Tests still reach these through `main`; they move to the new module paths in
# one mechanical commit once every slice is out of this file.
from app.lifespan import _COMMAND_MENU_LANGS, build_data  # noqa: E402, F401
from app.routes.health import health  # noqa: E402, F401
from app.routes.media import range_audio  # noqa: E402, F401
from bot.dispatch import handle_update  # noqa: E402, F401
from bot.inline import INLINE_MAX_PHOTOS, INLINE_PERSONAL_CACHE_TIME  # noqa: E402, F401
from bot.keyboards.language import (  # noqa: E402, F401
    language_keyboard,
    translation_language_keyboard,
)
from bot.keyboards.page import page_keyboard  # noqa: E402, F401
from bot.keyboards.reciter import (  # noqa: E402, F401  # noqa: E402, F401
    RECITER_PAGE_SIZE,
    reciter_keyboard,
    reciter_label,
    reciter_page_count,
    reciter_page_of,
    reciter_set_confirmation,
)
from bot.keyboards.verse import verse_keyboard  # noqa: E402, F401
from bot.limits import (
    MAX_RANGE_AYAHS,  # noqa: E402, F401
    REPEAT_COUNT,  # noqa: E402, F401
)
from bot.media import send_page, send_page_audio, send_repeated_audio  # noqa: E402, F401
from bot.text import build_verse_text  # noqa: E402, F401
from bot.text import reference as _reference  # noqa: E402, F401
from domain.parsing import as_int as _as_int  # noqa: E402, F401
from domain.parsing import (
    parse_ayah,  # noqa: E402, F401
    parse_ayah_range,  # noqa: E402, F401
)
from infra.audio import download_combined_audio as _download_combined_audio  # noqa: E402, F401
from locales import t, welcome_text  # noqa: E402, F401
from services.reciters import (  # noqa: E402, F401
    _RECITER_SHORTLIST,
    RECITER_KINDS,
    reciter_catalog,
    reciter_group,
    reciter_kind,
)
