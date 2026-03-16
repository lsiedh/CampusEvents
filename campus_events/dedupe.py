from __future__ import annotations

from campus_events.models import Event


def dedupe_events(events: list[Event]) -> list[Event]:
    best_by_key: dict[tuple[str, object, str], Event] = {}
    for event in sorted(events, key=lambda item: item.sort_key()):
        key = event.dedupe_key()
        existing = best_by_key.get(key)
        if existing is None or _score(event) > _score(existing):
            best_by_key[key] = event
    return sorted(best_by_key.values(), key=lambda item: item.sort_key())


def _score(event: Event) -> int:
    score = 0
    if event.start:
        score += 2
    if event.venue:
        score += 1
    if event.summary:
        score += 1
    if event.organiser:
        score += 1
    return score

