"""Unit tests for the `date` tool. Clock is frozen at 2026-11-09 20:30 UTC = Tuesday 2026-11-10 03:30 in Vietnam."""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

import tools.date.tool as date_tool
from tools import TOOL_FUNCTIONS


class FrozenDatetime(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime(2026, 11, 9, 20, 30, tzinfo=timezone.utc).astimezone(tz)


@pytest.fixture
def date(monkeypatch):
    monkeypatch.setattr(date_tool, "datetime", FrozenDatetime)
    return TOOL_FUNCTIONS["date"]


def test_today_uses_vietnam_time_not_utc(date) -> None:
    result = date()
    assert result["date"] == "2026-11-10"  # UTC is still Nov 9
    assert result["weekday"] == "Thứ Ba / Tuesday"
    assert result["today"] == "Thứ Ba / Tuesday 2026-11-10"
    assert result["now"] == "2026-11-10T03:30+07:00"


def test_last_and_next_week_come_without_offset(date) -> None:
    # gpt-4o-mini answered "last week" from a single date() call, so offset 0 must already carry it.
    result = date()
    assert result["last_week"][0] == "Thứ Hai / Monday 2026-11-02"
    assert result["last_week"][-1] == "Chủ Nhật / Sunday 2026-11-08"
    assert result["this_week"][0] == "Thứ Hai / Monday 2026-11-09"
    assert result["next_week"][4] == "Thứ Sáu / Friday 2026-11-20"


def test_offset_moves_date_and_its_week_but_not_today(date) -> None:
    result = date(offset_days=-14)
    assert result["date"] == "2026-10-27"
    assert result["weekday"] == "Thứ Ba / Tuesday"
    assert result["week_of_date"][0] == "Thứ Hai / Monday 2026-10-26"
    assert result["today"] == "Thứ Ba / Tuesday 2026-11-10"
    assert result["last_week"][0] == "Thứ Hai / Monday 2026-11-02"  # still relative to today


def test_yesterday_accepts_numeric_string_from_model(date) -> None:
    assert date(offset_days="-1")["date"] == "2026-11-09"


@pytest.mark.parametrize("bad", ["abc", "", None, 2.5, True, 10**6, [7]])
def test_bad_offset_returns_error_dict(date, bad) -> None:
    result = date(offset_days=bad)
    assert result["error"] == "invalid_input"
    assert "date" not in result
