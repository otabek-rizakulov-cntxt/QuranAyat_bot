"""Fixed-offset local time (`lib.localtime`).

The hifz platform has no IANA zones: a user's timezone is a fixed UTC offset
stored as TEXT, so "what date is it for this user" is one addition and needs no
tzdata. What that model must still get exactly right is the **day boundary** —
the streak's unit — and the next-reminder instant, because those are what a
wrong answer costs a user their streak over.
"""

from datetime import date, datetime, time, timedelta, timezone

import pytest

from lib.localtime import (
    DEFAULT_OFFSET,
    MAX_OFFSET_MINUTES,
    MIN_OFFSET_MINUTES,
    OFFSET_CHOICES,
    format_offset,
    is_valid_offset,
    local_date,
    local_now,
    local_time,
    next_due_utc,
    normalize_offset,
    offset_options,
    parse_offset,
    to_utc,
    week_bounds,
)


def _utc(*args) -> datetime:
    return datetime(*args, tzinfo=timezone.utc)


class TestParseOffset:
    def test_canonical_form(self):
        assert parse_offset("+05:00") == timedelta(hours=5)
        assert parse_offset("-03:30") == timedelta(hours=-3, minutes=-30)

    def test_accepts_the_forms_a_user_might_type(self):
        five = timedelta(hours=5)
        for text in ("+05:00", "+0500", "+5", "UTC+5", "utc+05:00", "GMT+5"):
            assert parse_offset(text) == five, text

    def test_zero_spellings(self):
        for text in ("Z", "UTC", "GMT", "+00:00", "-00:00"):
            assert parse_offset(text) == timedelta(0), text

    def test_unicode_minus_is_accepted(self):
        # iOS smart-punctuation turns a typed "-" into U+2212 often enough to matter
        assert parse_offset("−03:00") == timedelta(hours=-3)

    def test_half_and_quarter_hour_offsets(self):
        assert parse_offset("+05:45") == timedelta(hours=5, minutes=45)
        assert parse_offset("+09:30") == timedelta(hours=9, minutes=30)

    @pytest.mark.parametrize("bad", ["", "   ", "abc", "+99:00", "-13:00", "+15:00",
                                     "Asia/Tashkent", "+05:99", "five"])
    def test_rejects_junk_and_out_of_range(self, bad):
        with pytest.raises(ValueError):
            parse_offset(bad)

    def test_none_raises_rather_than_defaulting(self):
        with pytest.raises(ValueError):
            parse_offset(None)

    def test_extremes_of_the_real_world_are_in_range(self):
        assert parse_offset("-12:00") == timedelta(minutes=MIN_OFFSET_MINUTES)
        assert parse_offset("+14:00") == timedelta(minutes=MAX_OFFSET_MINUTES)

    def test_is_valid_offset_never_raises(self):
        assert is_valid_offset("+05:00") is True
        assert is_valid_offset("Asia/Tashkent") is False
        assert is_valid_offset(None) is False


class TestFormatOffset:
    def test_canonical_output(self):
        assert format_offset(timedelta(hours=5)) == "+05:00"
        assert format_offset(timedelta(hours=-3, minutes=-30)) == "-03:30"
        assert format_offset(timedelta(0)) == "+00:00"

    def test_round_trips_every_picker_choice(self):
        for choice in OFFSET_CHOICES:
            assert format_offset(parse_offset(choice)) == choice

    def test_normalize_collapses_spellings_to_storage_form(self):
        for text in ("+5", "UTC+5", "+0500", "+05:00"):
            assert normalize_offset(text) == "+05:00"

    def test_default_offset_is_canonical(self):
        assert normalize_offset(DEFAULT_OFFSET) == DEFAULT_OFFSET


class TestLocalDate:
    """The streak's unit. G1's acceptance criterion lives here."""

    def test_offset_shifts_the_wall_clock(self):
        assert local_now(_utc(2026, 7, 31, 12, 0), "+05:00") == datetime(2026, 7, 31, 17, 0)
        assert local_time(_utc(2026, 7, 31, 12, 0), "+05:00") == time(17, 0)

    def test_2359_and_0001_local_are_different_dates(self):
        # G1: "a session at 23:59 followed by one at 00:01 local ticks it twice"
        before = _utc(2026, 7, 31, 18, 59)   # 23:59 local at +05:00
        after = _utc(2026, 7, 31, 19, 1)     # 00:01 local, next day
        assert local_time(before, "+05:00") == time(23, 59)
        assert local_time(after, "+05:00") == time(0, 1)
        assert local_date(before, "+05:00") == date(2026, 7, 31)
        assert local_date(after, "+05:00") == date(2026, 8, 1)
        assert local_date(before, "+05:00") != local_date(after, "+05:00")

    def test_same_instant_is_two_dates_for_two_users(self):
        instant = _utc(2026, 7, 31, 22, 0)
        assert local_date(instant, "+05:00") == date(2026, 8, 1)   # already tomorrow
        assert local_date(instant, "-05:00") == date(2026, 7, 31)  # still today

    def test_negative_offset_can_roll_backwards(self):
        assert local_date(_utc(2026, 8, 1, 2, 0), "-05:00") == date(2026, 7, 31)

    def test_naive_datetime_is_assumed_utc(self):
        naive = datetime(2026, 7, 31, 18, 59)
        assert local_date(naive, "+05:00") == local_date(_utc(2026, 7, 31, 18, 59), "+05:00")

    def test_to_utc_round_trips(self):
        instant = _utc(2026, 7, 31, 18, 59)
        assert to_utc(local_now(instant, "+05:00"), "+05:00") == instant


class TestNextDueUtc:
    def test_later_today(self):
        # 10:00 local at +05:00 == 05:00 UTC; asking at 00:00 UTC gets today's
        after = _utc(2026, 7, 31, 0, 0)
        assert next_due_utc(time(10, 0), "+05:00", after) == _utc(2026, 7, 31, 5, 0)

    def test_rolls_to_tomorrow_once_passed(self):
        after = _utc(2026, 7, 31, 6, 0)      # 11:00 local, reminder already gone
        assert next_due_utc(time(10, 0), "+05:00", after) == _utc(2026, 8, 1, 5, 0)

    def test_strictly_after_so_rescheduling_on_fire_advances_a_day(self):
        # Otherwise a scheduler that re-enqueues the moment it fires loops forever.
        fired_at = _utc(2026, 7, 31, 5, 0)
        assert next_due_utc(time(10, 0), "+05:00", fired_at) == _utc(2026, 8, 1, 5, 0)

    def test_offset_moves_the_instant(self):
        after = _utc(2026, 7, 31, 0, 0)
        at_utc = next_due_utc(time(10, 0), "+00:00", after)
        at_plus5 = next_due_utc(time(10, 0), "+05:00", after)
        assert at_utc - at_plus5 == timedelta(hours=5)

    def test_changing_timezone_shifts_the_next_push(self):
        # B3's acceptance: "changing the timezone shifts the next scheduled push".
        # The two instants differ, and each one reads 07:00 on its own wall clock.
        # They are not simply three hours apart: at +08:00 07:00 local has already
        # passed at this instant, so that one correctly rolls to the next day.
        after = _utc(2026, 7, 31, 0, 0)
        before_change = next_due_utc(time(7, 0), "+05:00", after)
        after_change = next_due_utc(time(7, 0), "+08:00", after)
        assert after_change != before_change
        assert local_time(before_change, "+05:00") == time(7, 0)
        assert local_time(after_change, "+08:00") == time(7, 0)
        assert before_change > after and after_change > after

    def test_every_picker_offset_yields_a_due_instant_reading_the_wall_clock(self):
        after = _utc(2026, 7, 31, 9, 17)
        for offset in OFFSET_CHOICES:
            due = next_due_utc(time(6, 30), offset, after)
            assert due > after, offset
            assert local_time(due, offset) == time(6, 30), offset
            assert due - after <= timedelta(days=1), offset

    def test_midnight_reminder(self):
        after = _utc(2026, 7, 31, 12, 0)
        due = next_due_utc(time(0, 0), "+05:00", after)
        assert local_time(due, "+05:00") == time(0, 0)
        assert due > after


class TestWeekBounds:
    def test_monday_to_sunday_inclusive(self):
        # 2026-07-31 is a Friday
        start, end = week_bounds(date(2026, 7, 31))
        assert start == date(2026, 7, 27)
        assert end == date(2026, 8, 2)
        assert start.weekday() == 0 and end.weekday() == 6
        assert (end - start).days == 6

    def test_monday_is_its_own_week_start(self):
        assert week_bounds(date(2026, 7, 27))[0] == date(2026, 7, 27)

    def test_sunday_stays_in_the_week_that_began_that_monday(self):
        assert week_bounds(date(2026, 8, 2)) == (date(2026, 7, 27), date(2026, 8, 2))

    def test_every_day_of_a_week_agrees_on_its_bounds(self):
        monday = date(2026, 7, 27)
        expected = (monday, monday + timedelta(days=6))
        for offset in range(7):
            assert week_bounds(monday + timedelta(days=offset)) == expected

    def test_spans_a_month_boundary(self):
        assert week_bounds(date(2026, 8, 1)) == (date(2026, 7, 27), date(2026, 8, 2))


class TestPicker:
    def test_choices_are_ascending_and_unique(self):
        minutes = [parse_offset(c).total_seconds() for c in OFFSET_CHOICES]
        assert minutes == sorted(minutes)
        assert len(set(OFFSET_CHOICES)) == len(OFFSET_CHOICES)

    def test_choices_stay_inside_the_real_world(self):
        for choice in OFFSET_CHOICES:
            total = parse_offset(choice).total_seconds() / 60
            assert MIN_OFFSET_MINUTES <= total <= MAX_OFFSET_MINUTES

    def test_utc_is_offered(self):
        assert "+00:00" in OFFSET_CHOICES

    def test_offset_options_returns_a_mutable_copy(self):
        options = offset_options()
        options.append("nonsense")
        assert "nonsense" not in OFFSET_CHOICES

    def test_labels_need_no_translation(self):
        # half the reason for the fixed-offset model: the picker has no strings
        for choice in OFFSET_CHOICES:
            assert choice[0] in "+-" and ":" in choice
