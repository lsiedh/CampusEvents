from __future__ import annotations

from datetime import date

from campus_events.models import Event


def digest_subject(run_date: date) -> str:
    return f"Campus Events Digest for {run_date.isoformat()}"


def render_digest(events: list[Event], run_date: date) -> str:
    lines = [
        f"# {digest_subject(run_date)}",
        "",
        f"Generated for {run_date.isoformat()}",
        "",
    ]
    grouped: dict[str, list[Event]] = {"NUS": [], "NTU": [], "Other": []}
    for event in events:
        campus = event.campus if event.campus in grouped else "Other"
        grouped[campus].append(event)

    for campus in ["NUS", "NTU", "Other"]:
        items = grouped[campus]
        if not items:
            continue
        lines.append(f"## {campus}")
        lines.append("")
        for event in items:
            lines.extend(_render_event(event))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _render_event(event: Event) -> list[str]:
    start_text = event.start.isoformat() if event.start else "time unavailable"
    venue = event.venue or "venue unavailable"
    summary = event.summary.strip() or "No summary available."
    return [
        f"### {event.title}",
        f"- When: {start_text}",
        f"- Where: {venue}",
        f"- Organiser: {event.organiser or event.institution}",
        f"- Link: {event.source_url}",
        f"- Summary: {summary}",
        "",
    ]

