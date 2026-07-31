# The 12-week contribution graph: one small PNG of the user's last 84 days.
#
# G2's spec said an emoji grid; this is the approved override. An emoji grid
# renders differently on every client (and wraps at the worst possible column on
# a narrow phone), where a PNG is one image that looks the same everywhere and
# is the thing people actually screenshot and send to their circle.
#
# The memory objection behind assumption 1 is answered by the size: a 12-week
# grid is ~201x144 px, roughly 29k pixels, where a stitched mushaf page is tens
# of millions. It is an order of magnitude cheaper than work this same instance
# already does per /page. It is still bounded — the same loop-aware semaphore as
# `lib/page_image.py`, because on a 512 MB box the rule is that nothing
# unbounded ever runs, not that this particular thing is small.
#
# Two production constraints shape the drawing:
#
#   * The slim runtime image ships **no system fonts**. Nothing here opens a
#     .ttf; the graph is deliberately label-free. A font path would work on every
#     developer's laptop and crash only in production.
#   * The pure drawing function is synchronous and free of I/O, so it is unit
#     testable without an event loop — the same shape as `page_image.stitch_images`.
#
# Wave 2C caches the resulting Telegram file_id per (user, local date) via
# `File.save_file` / `File.get_file`; `cache_key` below is that key, and the
# graph is a pure function of exactly those two things.

import asyncio
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from io import BytesIO
from typing import Iterable, Mapping, Optional, Union

from lib.localtime import week_bounds
from lib.store import get_store
from lib.streaks import user_today

__all__ = [
    "GRID_WEEKS", "GRID_WIDTH", "GRID_HEIGHT", "BACKGROUND", "EMPTY", "FUTURE", "LEVELS",
    "CELL", "GAP", "PADDING", "LEGEND_CELL", "LEGEND_GAP", "LEGEND_MARGIN",
    "Grid", "build_grid", "level_for", "draw_contribution_graph",
    "render_streak_graph", "cache_key",
]

GRID_WEEKS = 12                 # 12 columns x 7 rows = 84 days, one quarter

CELL = 12                       # a square day
GAP = 3                         # between squares
PADDING = 12                    # around the whole card
LEGEND_CELL = 8
LEGEND_GAP = 3
LEGEND_MARGIN = 10              # between the grid and the legend strip

GRID_WIDTH = 2 * PADDING + GRID_WEEKS * CELL + (GRID_WEEKS - 1) * GAP          # 201
GRID_HEIGHT = (2 * PADDING + 7 * CELL + 6 * GAP
               + LEGEND_MARGIN + LEGEND_CELL)                                   # 144

# A five-step scale, light card. Chosen to survive Telegram's JPEG-ish preview
# scaling and to stay legible against both light and dark chat wallpapers, which
# is why the card has an opaque background instead of transparency.
BACKGROUND = "#ffffff"
EMPTY = "#ebedf0"               # a day with no session
FUTURE = "#f6f8fa"              # a day that has not happened yet this week
LEVELS = ("#9be9a8", "#40c463", "#30a14e", "#216e39")

# Sessions per day at which each shade kicks in. Four sessions is a heavy day;
# beyond that the colour saturates rather than inventing new shades.
LEVEL_THRESHOLDS = (1, 2, 3, 4)

Activity = Union[Mapping[date, int], Iterable[date]]


@dataclass(frozen=True)
class Grid:
    """The graph as data — `weeks` columns of 7 levels, Monday at the top.

    Each cell is 0 (no session), 1-4 (a shade), or None (a future day in the
    current week). Separated from the drawing so the layout can be asserted in a
    test without decoding a PNG, and so a text fallback stays possible.
    """

    start: date                 # the Monday of the leftmost column
    today: date
    columns: tuple              # tuple of 7-tuples, one per week


def level_for(count: int) -> int:
    """Shade index (0-4) for a day with `count` sessions."""
    if count <= 0:
        return 0
    for index, threshold in enumerate(LEVEL_THRESHOLDS):
        if count < threshold:
            return index
    return len(LEVELS)


def _counts(activity: Activity) -> Mapping[date, int]:
    """Accept either {date: sessions} or a bare iterable of active dates.

    `list_active_dates` gives the latter (one shade, every active day equal);
    `list_sessions` counted per day gives the former, which is what makes the
    scale worth having. Both are legitimate inputs, so both are accepted.
    """
    if isinstance(activity, Mapping):
        return activity
    counts = {}
    for day in activity:
        counts[day] = counts.get(day, 0) + 1
    return counts


def build_grid(activity: Activity, today: date, weeks: int = GRID_WEEKS) -> Grid:
    """Lay the last `weeks` weeks out in columns, ending with the current week.

    Columns are Monday→Sunday to match the leaderboard week, so the two features
    cut the calendar the same way. Days later this week than `today` are None
    rather than 0: they are not yet missed, and colouring them as misses reads as
    an accusation about a day that has not happened.
    """
    counts = _counts(activity)
    monday, _ = week_bounds(today)
    start = monday - timedelta(weeks=weeks - 1)

    columns = []
    for week in range(weeks):
        column = []
        for weekday in range(7):
            day = start + timedelta(weeks=week, days=weekday)
            column.append(None if day > today else level_for(counts.get(day, 0)))
        columns.append(tuple(column))
    return Grid(start, today, tuple(columns))


def draw_contribution_graph(activity: Activity, today: date,
                            weeks: int = GRID_WEEKS) -> BytesIO:
    """Render the grid to a PNG. Synchronous, no I/O, no font file.

    PNG rather than JPEG (the choice `page_image` makes for scanned text): this
    is flat colour on flat colour, where PNG is both smaller and free of the
    ringing JPEG puts around hard edges. A 12-week card lands around 1 kB.

    An empty history is a perfectly valid graph — an all-grey card is the honest
    picture of a user who has not started, and a first-run crash on a brand new
    user is not an option.
    """
    from PIL import Image, ImageDraw

    grid = build_grid(activity, today, weeks)
    width = 2 * PADDING + weeks * CELL + (weeks - 1) * GAP
    height = 2 * PADDING + 7 * CELL + 6 * GAP + LEGEND_MARGIN + LEGEND_CELL

    canvas = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(canvas)

    for week, column in enumerate(grid.columns):
        x = PADDING + week * (CELL + GAP)
        for weekday, level in enumerate(column):
            y = PADDING + weekday * (CELL + GAP)
            colour = FUTURE if level is None else (EMPTY if level == 0 else LEVELS[level - 1])
            draw.rectangle((x, y, x + CELL - 1, y + CELL - 1), fill=colour)

    # Legend: the scale itself, right-aligned under the grid. Label-free by
    # necessity (no fonts) and by preference — everyone already reads this shape.
    swatches = (EMPTY,) + LEVELS
    legend_width = len(swatches) * LEGEND_CELL + (len(swatches) - 1) * LEGEND_GAP
    x = width - PADDING - legend_width
    y = PADDING + 7 * CELL + 6 * GAP + LEGEND_MARGIN
    for colour in swatches:
        draw.rectangle((x, y, x + LEGEND_CELL - 1, y + LEGEND_CELL - 1), fill=colour)
        x += LEGEND_CELL + LEGEND_GAP

    out = BytesIO()
    canvas.save(out, format="PNG", optimize=True)
    out.seek(0)
    return out


# Same reasoning as `page_image._stitch_semaphore`: an asyncio primitive binds to
# the loop it is first awaited in, so a module-level semaphore breaks the moment
# a second loop appears (one loop in production, one per test under pytest).
# Rebuild it whenever the running loop changes.
_RENDER_CONCURRENCY = 2
_render_semaphore = None
_render_semaphore_loop = None


def _semaphore() -> asyncio.Semaphore:
    global _render_semaphore, _render_semaphore_loop
    loop = asyncio.get_running_loop()
    if _render_semaphore is None or _render_semaphore_loop is not loop:
        _render_semaphore = asyncio.Semaphore(_RENDER_CONCURRENCY)
        _render_semaphore_loop = loop
    return _render_semaphore


def cache_key(user_id: int, today: date) -> str:
    """The `File.save_file` / `File.get_file` key for a user's graph.

    The graph changes only when the day changes or a session lands, and a session
    lands at most a handful of times a day — so keying on (user, local date) and
    letting the last write win is exactly right. `v1` is here so a palette or
    layout change can invalidate every cached file_id by bumping one character.
    """
    return "streak_graph_v1_%d_%s" % (user_id, today.isoformat())


async def render_streak_graph(user_id: int, today: Optional[date] = None,
                              utc_now: Optional[datetime] = None,
                              weeks: int = GRID_WEEKS) -> BytesIO:
    """Read the user's last `weeks` weeks and render their graph.

    Pillow runs in a worker thread: it is CPU-bound, and however small this
    canvas is, it must not be the thing that stalls every other user's update.

    Reads `list_sessions` rather than `list_active_dates` so the shades mean
    something — the window is bounded to 84 days, so it is a small indexed read.
    """
    store = await get_store()
    if today is None:
        today = await user_today(user_id, utc_now)

    monday, _ = week_bounds(today)
    start = monday - timedelta(weeks=weeks - 1)
    rows = await store.sessions.list_sessions(user_id, start=start, end=today)

    counts: dict = {}
    for row in rows:
        counts[row.local_date] = counts.get(row.local_date, 0) + 1

    async with _semaphore():
        buf = await asyncio.to_thread(draw_contribution_graph, counts, today, weeks)
    buf.name = "streak.png"
    return buf
