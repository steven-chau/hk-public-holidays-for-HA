"""Parsing of the Hong Kong public holiday iCal-JSON data."""

from __future__ import annotations

from typing import Any


def _start_date(event: dict[str, Any]) -> str | None:
    """Return the "YYYYMMDD" start date of an event, if any."""
    dtstart = event.get("dtstart")
    if isinstance(dtstart, list) and dtstart and isinstance(dtstart[0], str):
        return dtstart[0][:8]
    if isinstance(dtstart, str):
        return dtstart[:8]
    return None


def parse_holidays(payload: Any) -> dict[str, str]:
    """Extract a mapping of dates ("YYYYMMDD") to holiday names."""
    calendars = payload.get("vcalendar") if isinstance(payload, dict) else None
    if not isinstance(calendars, list):
        raise ValueError("Unexpected holiday data structure")
    holidays: dict[str, str] = {}
    for calendar in calendars:
        if not isinstance(calendar, dict):
            continue
        for event in calendar.get("vevent") or []:
            if not isinstance(event, dict):
                continue
            if (start := _start_date(event)) is not None:
                holidays[start] = event.get("summary", "")
    if not holidays:
        raise ValueError("Holiday data does not contain any events")
    return holidays
