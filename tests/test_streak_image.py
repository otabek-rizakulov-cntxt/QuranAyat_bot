"""The 12-week contribution graph.

Most of this file asserts on `build_grid`, which is the layout as data — the PNG
tests exist to prove the two things that only bite in production: that Pillow
produces a decodable image with **no font file anywhere in the process**, and
that a brand-new user with no history renders rather than crashing.
"""

from datetime import date, datetime, timedelta, timezone
from io import BytesIO

from lib.store import get_store
from lib.store.sessions import KIND_DRILL
from lib.streak_image import (
    CELL,
    EMPTY,
    FUTURE,
    GAP,
    GRID_HEIGHT,
    GRID_WEEKS,
    GRID_WIDTH,
    LEGEND_CELL,
    LEVELS,
    PADDING,
    build_grid,
    cache_key,
    draw_contribution_graph,
    level_for,
    render_streak_graph,
)

WEDNESDAY = date(2026, 3, 18)
MONDAY = date(2026, 3, 16)


def open_png(buf: BytesIO):
    from PIL import Image

    buf.seek(0)
    image = Image.open(buf)
    image.load()
    return image


class TestLevels:
    def test_no_sessions_is_level_zero(self):
        assert level_for(0) == 0

    def test_each_session_count_maps_to_a_shade(self):
        assert [level_for(n) for n in (1, 2, 3, 4)] == [1, 2, 3, 4]

    def test_the_scale_saturates(self):
        assert level_for(50) == len(LEVELS)


class TestGrid:
    def test_the_grid_is_twelve_columns_of_seven_days(self):
        grid = build_grid([], WEDNESDAY)
        assert len(grid.columns) == GRID_WEEKS
        assert all(len(column) == 7 for column in grid.columns)

    def test_the_last_column_is_the_current_week_and_starts_on_a_monday(self):
        grid = build_grid([], WEDNESDAY)
        assert grid.start.weekday() == 0
        assert grid.start == MONDAY - timedelta(weeks=GRID_WEEKS - 1)

    def test_an_empty_history_is_all_empty_cells(self):
        grid = build_grid([], WEDNESDAY)
        levels = {level for column in grid.columns for level in column}
        assert levels == {0, None}

    def test_days_later_this_week_are_future_not_missed(self):
        grid = build_grid([], WEDNESDAY)
        last = grid.columns[-1]
        assert last[:3] == (0, 0, 0)             # Mon-Wed have happened
        assert last[3:] == (None,) * 4           # Thu-Sun have not

    def test_an_active_day_lands_in_the_right_cell(self):
        grid = build_grid([WEDNESDAY], WEDNESDAY)
        assert grid.columns[-1][2] == 1          # Wednesday is row 2 of the last week
        assert grid.columns[-1][1] == 0

    def test_repeated_dates_deepen_the_shade(self):
        grid = build_grid([WEDNESDAY, WEDNESDAY, WEDNESDAY], WEDNESDAY)
        assert grid.columns[-1][2] == 3

    def test_a_count_mapping_is_accepted_too(self):
        grid = build_grid({WEDNESDAY: 4}, WEDNESDAY)
        assert grid.columns[-1][2] == 4

    def test_days_older_than_the_window_are_ignored(self):
        stale = WEDNESDAY - timedelta(weeks=GRID_WEEKS + 2)
        grid = build_grid([stale, WEDNESDAY], WEDNESDAY)
        assert sum(1 for column in grid.columns for level in column if level) == 1

    def test_the_window_is_configurable(self):
        assert len(build_grid([], WEDNESDAY, weeks=4).columns) == 4


class TestRendering:
    def test_an_empty_history_renders_a_valid_png(self):
        image = open_png(draw_contribution_graph([], WEDNESDAY))
        assert image.format == "PNG"
        assert image.size == (GRID_WIDTH, GRID_HEIGHT)

    def test_no_font_file_is_ever_opened(self, monkeypatch):
        """The slim runtime image has no system fonts.

        Anything that reaches for a .ttf works on a laptop and crashes only in
        production, so make the attempt itself an error for the duration of a
        render.
        """
        from PIL import ImageFont

        def explode(*args, **kwargs):
            raise AssertionError("the graph must not load a font file")

        monkeypatch.setattr(ImageFont, "truetype", explode)
        monkeypatch.setattr(ImageFont, "load_path", explode)
        image = open_png(draw_contribution_graph([WEDNESDAY], WEDNESDAY))
        assert image.size == (GRID_WIDTH, GRID_HEIGHT)

    def test_active_days_are_actually_coloured(self):
        from PIL import ImageColor

        active = [WEDNESDAY - timedelta(days=n) for n in range(5)]
        image = open_png(draw_contribution_graph(active, WEDNESDAY)).convert("RGB")
        colours = {colour for _, colour in image.getcolors(maxcolors=64)}
        assert ImageColor.getrgb(LEVELS[0]) in colours
        assert ImageColor.getrgb(EMPTY) in colours
        assert ImageColor.getrgb(FUTURE) in colours

    def test_an_empty_graph_has_no_green_in_its_grid(self):
        # The legend always shows the whole scale, so only the grid area above it
        # is allowed to be colourless.
        from PIL import ImageColor

        image = open_png(draw_contribution_graph([], WEDNESDAY)).convert("RGB")
        grid = image.crop((0, 0, image.width, GRID_HEIGHT - PADDING - LEGEND_CELL))
        colours = {colour for _, colour in grid.getcolors(maxcolors=64)}
        assert not any(ImageColor.getrgb(level) in colours for level in LEVELS)

    def test_the_card_stays_small(self):
        # A dense year of activity is still a tiny upload; this is the ceiling
        # the 512 MB instance was worried about.
        active = [WEDNESDAY - timedelta(days=n) for n in range(84)]
        buf = draw_contribution_graph(active, WEDNESDAY)
        assert buf.getbuffer().nbytes < 20 * 1024

    def test_a_shorter_window_renders_a_narrower_card(self):
        image = open_png(draw_contribution_graph([], WEDNESDAY, weeks=4))
        assert image.height == GRID_HEIGHT
        assert image.width < GRID_WIDTH


class TestRenderStreakGraph:
    async def test_a_user_with_no_history_still_gets_a_graph(self):
        buf = await render_streak_graph(
            1, utc_now=datetime(2026, 3, 18, 12, 0, tzinfo=timezone.utc))
        assert buf.name == "streak.png"
        assert open_png(buf).size == (GRID_WIDTH, GRID_HEIGHT)

    async def test_the_graph_reflects_logged_sessions(self):
        from PIL import ImageColor

        store = await get_store()
        await store.profiles.set_timezone(1, "+05:00")
        for n in range(3):
            await store.sessions.log_session(1, WEDNESDAY - timedelta(days=n), KIND_DRILL)
        buf = await render_streak_graph(
            1, utc_now=datetime(2026, 3, 18, 12, 0, tzinfo=timezone.utc))
        image = open_png(buf).convert("RGB")
        colours = {colour for _, colour in image.getcolors(maxcolors=64)}
        assert ImageColor.getrgb(LEVELS[0]) in colours

    async def test_the_day_is_the_users_local_day(self):
        # 20:00 UTC on Wednesday is already Thursday at UTC+5, so Thursday's cell
        # in the last column stops being a future cell — the same instant leaves
        # it in the future for a UTC user.
        from PIL import ImageColor

        store = await get_store()
        await store.profiles.set_timezone(1, "+05:00")
        await store.profiles.set_timezone(2, "+00:00")
        instant = datetime(2026, 3, 18, 20, 0, tzinfo=timezone.utc)

        # Centre of the last column, Thursday's row.
        pixel = (GRID_WIDTH - PADDING - CELL // 2, PADDING + 3 * (CELL + GAP) + CELL // 2)
        east = open_png(await render_streak_graph(1, utc_now=instant)).convert("RGB")
        utc = open_png(await render_streak_graph(2, utc_now=instant)).convert("RGB")
        assert east.getpixel(pixel) == ImageColor.getrgb(EMPTY)
        assert utc.getpixel(pixel) == ImageColor.getrgb(FUTURE)

    async def test_concurrent_renders_all_complete(self):
        # The loop-aware semaphore must not deadlock or leak across event loops.
        import asyncio

        buffers = await asyncio.gather(*(
            render_streak_graph(user_id,
                                utc_now=datetime(2026, 3, 18, 12, 0, tzinfo=timezone.utc))
            for user_id in range(5)))
        assert all(open_png(buf).size == (GRID_WIDTH, GRID_HEIGHT) for buf in buffers)


class TestCacheKey:
    def test_the_key_is_per_user_and_per_local_day(self):
        assert cache_key(7, WEDNESDAY) == "streak_graph_v1_7_2026-03-18"
        assert cache_key(7, WEDNESDAY) != cache_key(7, WEDNESDAY + timedelta(days=1))
        assert cache_key(7, WEDNESDAY) != cache_key(8, WEDNESDAY)
