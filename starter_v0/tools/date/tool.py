from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

# ponytail: fixed UTC+7 (Vietnam has no DST); add a timezone arg if users ask about other cities.
VN_TZ = timezone(timedelta(hours=7), "UTC+07:00")
# Bilingual on purpose: Vietnamese-only names made gpt-4o-mini answer English questions half in Vietnamese.
WEEKDAYS = ["Thứ Hai / Monday", "Thứ Ba / Tuesday", "Thứ Tư / Wednesday", "Thứ Năm / Thursday",
            "Thứ Sáu / Friday", "Thứ Bảy / Saturday", "Chủ Nhật / Sunday"]
MAX_OFFSET_DAYS = 3660  # ~10 years; keeps date arithmetic far from OverflowError


def _week(monday) -> list[str]:
    return [f"{WEEKDAYS[i]} {(monday + timedelta(days=i)).isoformat()}" for i in range(7)]


def get_date(offset_days: int = 0) -> dict[str, Any]:
    """Today in Vietnam plus last/this/next week (always, so 'last week' needs no offset),
    and today + offset_days with Monday..Sunday of that date's week."""
    try:
        days = int(offset_days)
        if isinstance(offset_days, bool) or days != float(offset_days) or abs(days) > MAX_OFFSET_DAYS:
            raise ValueError
    except (TypeError, ValueError):
        return {
            "tool": "date",
            "error": "invalid_input",
            "message": f"offset_days phải là số nguyên trong [-{MAX_OFFSET_DAYS}, {MAX_OFFSET_DAYS}], nhận {offset_days!r}.",
        }
    now = datetime.now(VN_TZ)
    today = now.date()
    this_monday = today - timedelta(days=today.weekday())
    target = today + timedelta(days=days)
    return {
        "tool": "date",
        "now": now.isoformat(timespec="minutes"),
        "today": f"{WEEKDAYS[today.weekday()]} {today.isoformat()}",
        "last_week": _week(this_monday - timedelta(days=7)),
        "this_week": _week(this_monday),
        "next_week": _week(this_monday + timedelta(days=7)),
        "offset_days": days,
        "date": target.isoformat(),
        "weekday": WEEKDAYS[target.weekday()],
        "week_of_date": _week(target - timedelta(days=target.weekday())),
    }
