from __future__ import annotations

import re
from datetime import date, timedelta
from zoneinfo import ZoneInfo

from campus_events.config import SINGAPORE_TIMEZONE
from campus_events.models import Event


EXCLUDED_TITLE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bmodule\b",
        r"\bclass\b",
        r"\blecture\s+\d+\b",
        r"\btutorial\b",
        r"\blab session\b",
        r"\bexam\b",
        r"\bmidterm\b",
        r"\binternal meeting\b",
    ]
]


def filter_events(events: list[Event], run_date: date) -> list[Event]:
    kept: list[Event] = []
    window_end = run_date + timedelta(days=7)
    singapore_tz = ZoneInfo(SINGAPORE_TIMEZONE)
    for event in events:
        title = event.title.strip()
        if not title:
            continue
        if any(pattern.search(title) for pattern in EXCLUDED_TITLE_PATTERNS):
            continue
        if event.audience_hint == "campus_only":
            continue
        if event.start is None:
            continue
        event_date = event.start.astimezone(singapore_tz).date()
        if event_date < run_date or event_date > window_end:
            continue
        kept.append(event)
    return kept
