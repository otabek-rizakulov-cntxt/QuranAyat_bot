"""Which ayah is the verse of the day (docs/MULTI_PLATFORM_PLAN.md P2.5).

Everyone gets the same ayah on the same local date: shareable ("did you see
today's verse?"), and one cached image and recitation serve every reader. The
list rotates in order rather than at random, so nothing repeats until the whole
list has been shown. It is a hand-picked set of ayat that stand on their own —
widely recited and quoted ones — rather than all 6,236, many of which begin
mid-sentence. Extend it freely; `tests/test_daily_ayah.py` checks every entry.
"""

from datetime import date
from typing import Tuple

DAILY_AYAT: Tuple[Tuple[int, int], ...] = (
    (2, 255), (94, 5), (13, 28), (39, 53), (2, 286), (65, 3), (3, 190), (2, 152),
    (40, 60), (2, 186), (94, 6), (3, 8), (14, 7), (65, 2), (2, 153), (49, 13),
    (3, 139), (17, 23), (2, 201), (21, 87), (51, 56), (3, 159), (29, 69), (16, 97),
    (2, 216), (59, 22), (3, 185), (25, 63), (8, 46), (33, 41), (2, 155), (17, 24),
    (3, 173), (9, 51), (13, 11), (67, 2), (2, 156), (93, 5), (31, 17), (20, 114),
    (59, 23), (49, 10), (3, 191), (7, 23), (21, 83), (25, 74), (28, 24), (29, 45),
    (2, 256), (15, 9), (3, 103), (6, 162), (17, 80), (17, 82), (18, 10), (18, 46),
    (24, 35), (33, 56), (55, 13), (59, 24), (103, 2), (112, 1), (9, 129), (10, 62),
    (7, 56), (3, 26), (16, 128), (1, 2),
)  # fmt: skip


def ayah_for(day: date) -> Tuple[int, int]:
    """(surah, ayah) for a local calendar date."""
    return DAILY_AYAT[day.toordinal() % len(DAILY_AYAT)]
