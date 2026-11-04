#!/usr/bin/env python3
"""Draw the Telegram description picture: the WhatsApp profile mark on the left,
the bot's name and what it does on the right, in the same green and gold.

    python3 scripts/make_telegram_banner.py [out.png]

Writes assets/telegram/description.png (640x360, the size Telegram recommends
for the picture above a bot's description) unless given a path. Reads the mark
from assets/whatsapp/avatar.png (scripts/make_whatsapp_avatar.py), so the two
platforms share one design. The text uses Pillow's bundled font (Aileron).
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), "..")
AVATAR = os.path.join(ROOT, "assets", "whatsapp", "avatar.png")
OUT = os.path.join(ROOT, "assets", "telegram", "description.png")

W, H, S = 640, 360, 3  # size, and supersampling for smooth text
GREEN = (14, 107, 85)
GREEN_DARK = (9, 74, 59)
GOLD = (226, 189, 112)
CREAM = (247, 243, 234)

TITLE = "Quran Ayah Bot"
TAGLINE = "The Holy Qur'an, one ayah at a time"
FEATURES = ("Ayat & translations", "Recitations", "Verse of the day", "Hifz plans")

img = Image.new("RGB", (W * S, H * S), GREEN_DARK)
d = ImageDraw.Draw(img)

# the mark, on the same radial shading the avatar has (radius 0.72 of its side,
# dark green beyond), so its square edges vanish into the background
side = int(H * S * 0.86)
cx, cy = W * S * 0.25, H * S * 0.5
for i in range(60):
    r = side * 0.72 * (1 - i / 60)
    shade = tuple(int(GREEN_DARK[k] + (GREEN[k] - GREEN_DARK[k]) * (i / 60)) for k in range(3))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=shade)
mark = Image.open(AVATAR).convert("RGB").resize((side, side), Image.LANCZOS)
img.paste(mark, (int(cx - side / 2), int(cy - side / 2)))

x = int(W * S * 0.50)
title = ImageFont.load_default(size=38 * S)
tagline = ImageFont.load_default(size=17 * S)
feature = ImageFont.load_default(size=16 * S)
d.text((x, 96 * S), TITLE, font=title, fill=CREAM)
d.line([(x, 152 * S), (x + 60 * S, 152 * S)], fill=GOLD, width=3 * S)
d.text((x, 166 * S), TAGLINE, font=tagline, fill=GOLD)
for n, line in enumerate(FEATURES):
    y = 206 * S + n * 26 * S
    d.ellipse([x, y + 6 * S, x + 7 * S, y + 13 * S], fill=GOLD)
    d.text((x + 16 * S, y), line, font=feature, fill=CREAM)

out = sys.argv[1] if len(sys.argv) > 1 else OUT
os.makedirs(os.path.dirname(out), exist_ok=True)
img.resize((W, H), Image.LANCZOS).save(out, optimize=True)
