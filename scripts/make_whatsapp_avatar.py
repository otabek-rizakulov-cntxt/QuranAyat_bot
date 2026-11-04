#!/usr/bin/env python3
"""Draw the WhatsApp profile picture: a Rub el Hizb star (the mark that divides
the mushaf into sections) around an open book, in the app's green and gold.

    python3 scripts/make_whatsapp_avatar.py [out.png] [circle-preview.png]

Writes assets/whatsapp/avatar.png (640x640, what scripts/whatsapp_setup.py
uploads) unless given a path. WhatsApp crops the picture to a circle, so
everything sits well inside it; the optional second path is that crop, to look
at. Drawn at 4x and downsampled for smooth edges. No text: Pillow here has no
Arabic shaping, and a profile picture is shown far too small for words.
"""

import math
import os
import sys

from PIL import Image, ImageDraw

SIZE = 640
S = 4  # supersampling
N = SIZE * S
C = N / 2

GREEN = (14, 107, 85)
GREEN_DARK = (9, 74, 59)
GOLD = (226, 189, 112)
CREAM = (247, 243, 234)


def square(cx, cy, r, angle):
    return [
        (cx + r * math.cos(angle + k * math.pi / 2), cy + r * math.sin(angle + k * math.pi / 2))
        for k in range(4)
    ]


def star(r):
    """The 8-pointed star: two squares, one turned 45 degrees."""
    return square(C, C, r, math.pi / 4), square(C, C, r, 0)


img = Image.new("RGB", (N, N), GREEN)
d = ImageDraw.Draw(img)

# soft radial vignette for depth
for i in range(60):
    r = N * 0.72 * (1 - i / 60)
    shade = tuple(int(GREEN_DARK[k] + (GREEN[k] - GREEN_DARK[k]) * (i / 60)) for k in range(3))
    d.ellipse([C - r, C - r, C + r, C + r], fill=shade)

# the star: gold outline, then a green inset so it reads as a frame
R = N * 0.37
for sq in star(R):
    d.polygon(sq, fill=GOLD)
for sq in star(R - 14 * S):
    d.polygon(sq, fill=GREEN)
d.ellipse([C - R * 0.62, C - R * 0.62, C + R * 0.62, C + R * 0.62], outline=GOLD, width=5 * S)

# open book in the middle
w = R * 0.50  # half width of the book
h = R * 0.40  # page height
top = C - h * 0.55
sag = h * 0.16  # pages dip towards the spine
spine_bottom = top + h + sag * 0.4
left = [
    (C, top + sag),
    (C - w * 0.5, top - sag * 0.3),
    (C - w, top),
    (C - w, top + h),
    (C - w * 0.5, top + h - sag * 0.3),
    (C, spine_bottom),
]
right = [(2 * C - x, y) for x, y in left]
d.polygon(left, fill=CREAM)
d.polygon(right, fill=CREAM)
d.line([(C, top + sag), (C, spine_bottom)], fill=GOLD, width=4 * S)
# lines of text on each page
for k in range(1, 5):
    y = top + h * k / 5.2 + sag * 0.15
    for sign in (-1, 1):
        x0, x1 = C + sign * w * 0.18, C + sign * w * 0.85
        d.line([(x0, y + sag * 0.25), (x1, y)], fill=GREEN, width=int(3.2 * S))

# small crescent above the book
cr = R * 0.12
cx, cy = C, top - R * 0.24
d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=GOLD)
d.ellipse([cx - cr * 0.55, cy - cr * 1.05, cx + cr * 1.25, cy + cr * 0.75], fill=GREEN)

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "whatsapp", "avatar.png")
img.resize((SIZE, SIZE), Image.LANCZOS).save(
    sys.argv[1] if len(sys.argv) > 1 else OUT, optimize=True
)
if len(sys.argv) < 3:
    sys.exit(0)

# preview of how WhatsApp shows it (circle crop)
mask = Image.new("L", (N, N), 0)
ImageDraw.Draw(mask).ellipse([0, 0, N, N], fill=255)
preview = Image.new("RGB", (N, N), (255, 255, 255))
preview.paste(img, mask=mask)
preview.resize((SIZE, SIZE), Image.LANCZOS).save(sys.argv[2])
