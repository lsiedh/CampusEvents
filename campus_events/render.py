from __future__ import annotations

from datetime import date
from html import escape
from zoneinfo import ZoneInfo

from campus_events.config import SINGAPORE_TIMEZONE
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


def render_digest_text(events: list[Event], run_date: date) -> str:
    lines = [
        digest_subject(run_date),
        "",
        f"Generated for {run_date.isoformat()}",
        "",
    ]
    for campus, items in _grouped_events(events).items():
        if not items:
            continue
        lines.append(campus)
        lines.append("-" * len(campus))
        for event in items:
            lines.extend(_render_event_text(event))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_digest_html(events: list[Event], run_date: date) -> str:
    sections: list[str] = []
    for campus, items in _grouped_events(events).items():
        if not items:
            continue
        cards = "\n".join(_render_event_html(event) for event in items)
        sections.append(
            f"""
            <section class="campus-section">
              <h2>{escape(campus)}</h2>
              {cards}
            </section>
            """.strip()
        )

    sections_html = "\n".join(sections)
    title = escape(digest_subject(run_date))
    run_date_text = escape(run_date.isoformat())
    return f"""\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
      body {{
        margin: 0;
        padding: 24px 0;
        background: #f4f1ea;
        color: #182028;
        font-family: Georgia, "Times New Roman", serif;
      }}
      .container {{
        max-width: 760px;
        margin: 0 auto;
        background: #fffdf8;
        border: 1px solid #dfd7c8;
        box-shadow: 0 8px 24px rgba(24, 32, 40, 0.08);
      }}
      .header {{
        padding: 28px 32px 20px;
        background: linear-gradient(135deg, #0f3b66, #1b6b73);
        color: #f8f4ec;
      }}
      .header h1 {{
        margin: 0 0 8px;
        font-size: 32px;
        line-height: 1.15;
      }}
      .header p {{
        margin: 0;
        font-size: 15px;
        opacity: 0.9;
      }}
      .content {{
        padding: 24px 32px 32px;
      }}
      .campus-section {{
        margin-top: 24px;
      }}
      .campus-section h2 {{
        margin: 0 0 14px;
        padding-bottom: 8px;
        border-bottom: 2px solid #d6c8a8;
        color: #0f3b66;
        font-size: 22px;
      }}
      .event-card {{
        margin: 0 0 18px;
        padding: 16px 18px;
        background: #fff;
        border: 1px solid #e6ddcf;
        border-left: 4px solid #ba6a2d;
      }}
      .event-card h3 {{
        margin: 0 0 10px;
        font-size: 20px;
        line-height: 1.25;
      }}
      .meta {{
        margin: 0 0 12px;
        padding: 0;
        list-style: none;
      }}
      .meta li {{
        margin: 0 0 4px;
        font-size: 14px;
      }}
      .label {{
        font-weight: 700;
      }}
      .summary {{
        margin: 0 0 10px;
        font-size: 15px;
        line-height: 1.55;
      }}
      .link a {{
        color: #0f5ea8;
        text-decoration: none;
      }}
      @media only screen and (max-width: 640px) {{
        body {{ padding: 0; }}
        .container {{ border: 0; box-shadow: none; }}
        .header, .content {{ padding: 20px; }}
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h1>{title}</h1>
        <p>Generated for {run_date_text}</p>
      </div>
      <div class="content">
        {sections_html}
      </div>
    </div>
  </body>
</html>
"""


def _render_event(event: Event) -> list[str]:
    start_text = _format_event_start(event)
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


def _render_event_text(event: Event) -> list[str]:
    start_text = _format_event_start(event)
    venue = event.venue or "venue unavailable"
    summary = event.summary.strip() or "No summary available."
    return [
        event.title,
        f"  When: {start_text}",
        f"  Where: {venue}",
        f"  Organiser: {event.organiser or event.institution}",
        f"  Link: {event.source_url}",
        f"  Summary: {summary}",
        "",
    ]


def _render_event_html(event: Event) -> str:
    start_text = escape(_format_event_start(event))
    venue = escape(event.venue or "venue unavailable")
    organiser = escape(event.organiser or event.institution)
    summary = escape(event.summary.strip() or "No summary available.")
    title = escape(event.title)
    link = escape(event.source_url, quote=True)
    return f"""\
<article class="event-card">
  <h3>{title}</h3>
  <ul class="meta">
    <li><span class="label">When:</span> {start_text}</li>
    <li><span class="label">Where:</span> {venue}</li>
    <li><span class="label">Organiser:</span> {organiser}</li>
  </ul>
  <p class="summary">{summary}</p>
  <p class="link"><a href="{link}">Open event page</a></p>
</article>
"""


def _grouped_events(events: list[Event]) -> dict[str, list[Event]]:
    grouped: dict[str, list[Event]] = {"NUS": [], "NTU": [], "Other": []}
    for event in events:
        campus = event.campus if event.campus in grouped else "Other"
        grouped[campus].append(event)
    return grouped


def _format_event_start(event: Event) -> str:
    if event.start is None:
        return "time unavailable"
    localized = event.start.astimezone(ZoneInfo(SINGAPORE_TIMEZONE))
    return localized.strftime("%m/%d/%y %H:%M")
