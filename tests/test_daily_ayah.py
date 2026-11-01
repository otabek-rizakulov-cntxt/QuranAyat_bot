"""The verse-of-the-day list and its rotation (MULTI_PLATFORM_PLAN P2.5)."""

from datetime import date, timedelta

from domain.daily_ayah import DAILY_AYAT, ayah_for
from domain.quran import Quran


def test_every_entry_is_a_real_ayah():
    missing = [ref for ref in DAILY_AYAT if not Quran.exists(*ref)]
    assert not missing


def test_no_duplicates():
    assert len(set(DAILY_AYAT)) == len(DAILY_AYAT)


def test_same_date_same_ayah():
    assert ayah_for(date(2026, 11, 2)) == ayah_for(date(2026, 11, 2))


def test_nothing_repeats_within_one_cycle():
    start = date(2026, 1, 1)
    picks = [ayah_for(start + timedelta(days=n)) for n in range(len(DAILY_AYAT))]
    assert sorted(picks) == sorted(DAILY_AYAT)
