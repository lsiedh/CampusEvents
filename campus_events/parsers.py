from __future__ import annotations

import json
import re
from collections.abc import Iterable
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from html import unescape
from xml.etree import ElementTree

from campus_events.models import Event, SourceRecord


class ParseError(Exception):
    """Raised when a source body cannot be parsed into candidate events."""


HTML_STRUCTURED_DATA_FAMILIES = {
    "institute_news_events",
}

CARD_LAYOUT_SPECS = {
    "nus_arts_festival": {
        "card_class": "festival-event-card",
        "summary_class": "festival-event-summary",
        "venue_class": "festival-event-venue",
        "date_class": "festival-event-date",
        "taxonomy_class": "festival-event-taxonomy",
        "audience_mode": "public",
    },
    "heritage_programmes": {
        "card_class": "heritage-programme-card",
        "summary_class": "heritage-programme-summary",
        "venue_class": "heritage-programme-venue",
        "date_class": "heritage-programme-date",
        "taxonomy_class": "heritage-programme-taxonomy",
        "audience_mode": "public",
    },
    "taxonomy_events": {
        "card_class": "taxonomy-event-card",
        "summary_class": "taxonomy-event-summary",
        "venue_class": "taxonomy-event-venue",
        "date_class": "taxonomy-event-date",
        "taxonomy_class": "taxonomy-event-taxonomy",
        "audience_mode": "public",
    },
    "detail_cards": {
        "card_class": "detail-event-card",
        "summary_class": "detail-event-summary",
        "venue_class": "detail-event-venue",
        "date_class": "detail-event-date",
        "taxonomy_class": "detail-event-taxonomy",
        "audience_mode": "public",
    },
    "series_and_conference_index": {
        "card_class": "series-event-card",
        "summary_class": "series-event-summary",
        "venue_class": "series-event-venue",
        "date_class": "series-event-date",
        "taxonomy_class": "series-event-taxonomy",
        "audience_mode": "public",
    },
    "upcoming_events_listing": {
        "card_class": "upcoming-event-card",
        "summary_class": "upcoming-event-summary",
        "venue_class": "upcoming-event-venue",
        "date_class": "upcoming-event-date",
        "taxonomy_class": "upcoming-event-taxonomy",
        "audience_mode": "public",
    },
    "seminar_series_listing": {
        "card_class": "seminar-series-card",
        "summary_class": "seminar-series-summary",
        "venue_class": "seminar-series-venue",
        "date_class": "seminar-series-date",
        "taxonomy_class": "seminar-series-taxonomy",
        "audience_mode": "public",
    },
    "ntu_event_portal": {
        "card_class": "ntu-portal-event-card",
        "summary_class": "ntu-portal-event-summary",
        "venue_class": "ntu-portal-event-venue",
        "date_class": "ntu-portal-event-date",
        "taxonomy_class": "ntu-portal-event-taxonomy",
        "audience_mode": "public",
    },
    "ntu_event_detail_listing": {
        "card_class": "ntu-detail-event-card",
        "summary_class": "ntu-detail-event-summary",
        "venue_class": "ntu-detail-event-venue",
        "date_class": "ntu-detail-event-date",
        "taxonomy_class": "ntu-detail-event-taxonomy",
        "audience_mode": "public",
    },
    "museum_listing": {
        "card_class": "museum-listing-card",
        "summary_class": "museum-listing-summary",
        "venue_class": "museum-listing-venue",
        "date_class": "museum-listing-date",
        "taxonomy_class": "museum-listing-taxonomy",
        "audience_mode": "public",
    },
    "seminar_hub": {
        "card_class": "seminar-hub-card",
        "summary_class": "seminar-hub-summary",
        "venue_class": "seminar-hub-venue",
        "date_class": "seminar-hub-date",
        "taxonomy_class": "seminar-hub-taxonomy",
        "audience_mode": "public",
    },
}


def parse_source(source: SourceRecord, content: str) -> list[Event]:
    if source.parser_family == "generic_rss":
        return parse_generic_rss(source, content)
    if source.parser_family == "nus_osa_events":
        return parse_nus_osa_events(source, content)
    if source.parser_family == "museum_cards":
        return parse_museum_cards(source, content)
    if source.parser_family == "filtered_event_cards":
        return parse_filtered_event_cards(source, content)
    if source.parser_family in CARD_LAYOUT_SPECS:
        return parse_card_layout(source, content, CARD_LAYOUT_SPECS[source.parser_family])
    if source.parser_family == "nus_coe_rss_directory":
        raise ParseError(
            "rss directory expansion is not implemented yet; capture fixtures and "
            "promote downstream feeds before enabling this source"
        )
    if source.parser_family in HTML_STRUCTURED_DATA_FAMILIES:
        return parse_html_structured_events(source, content)
    raise ParseError(f"unsupported parser family: {source.parser_family}")


def parse_nus_coe_rss_directory(source: SourceRecord, content: str) -> list[SourceRecord]:
    matches = re.findall(
        r'<a\b[^>]*href=["\']([^"\']*coeGenRss\.jsp\?Cat=\d+)["\'][^>]*>(.*?)</a>',
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not matches:
        raise ParseError("nus_coe_rss_directory fixture has no downstream coeGenRss links")

    expanded: list[SourceRecord] = []
    for url, label in matches:
        title = _clean_html_text(label)
        if not title:
            continue
        slug = _slugify(title)
        absolute_url = url
        if absolute_url.startswith("/"):
            absolute_url = "https://myaces.nus.edu.sg" + absolute_url
        elif absolute_url.startswith("coeGenRss.jsp"):
            absolute_url = "https://myaces.nus.edu.sg/CoE/jsp/" + absolute_url
        expanded.append(
            source.clone_with(
                id=f"{source.id}:{slug}",
                url=absolute_url,
                source_kind="rss",
                parser_family="generic_rss",
                fixture_slug=f"{source.fixture_slug}_{slug}",
                categories_hint=[slug],
            )
        )
    if not expanded:
        raise ParseError("nus_coe_rss_directory yielded no usable downstream feeds")
    return expanded


def parse_generic_rss(source: SourceRecord, content: str) -> list[Event]:
    try:
        root = ElementTree.fromstring(content)
    except ElementTree.ParseError as exc:
        raise ParseError(f"invalid rss/xml: {exc}") from exc

    items = root.findall(".//item")
    if not items:
        items = root.findall(".//{http://www.w3.org/2005/Atom}entry")
    if not items:
        raise ParseError("no rss or atom items found")

    events: list[Event] = []
    for item in items:
        title = _find_text(
            item,
            "title",
            "{http://www.w3.org/2005/Atom}title",
        )
        link = _find_text(item, "link")
        if not link:
            atom_link = item.find("{http://www.w3.org/2005/Atom}link")
            if atom_link is not None:
                link = atom_link.attrib.get("href", "")
        summary = _find_text(
            item,
            "description",
            "{http://purl.org/rss/1.0/modules/content/}encoded",
            "{http://www.w3.org/2005/Atom}summary",
        )
        start = _parse_datetime(
            _find_text(item, "pubDate", "{http://www.w3.org/2005/Atom}updated")
        )
        events.append(
            Event(
                title=title or "(untitled event)",
                summary=summary or "",
                start=start,
                end=None,
                timezone=_format_timezone(start),
                venue="",
                campus=source.campus,
                institution=source.organisation,
                organiser=source.organisation,
                source_name=source.id,
                source_url=link or source.url,
                category=source.categories_hint[0] if source.categories_hint else "event",
                audience_hint="public",
                tags=source.categories_hint.copy(),
            )
        )
    return events


def parse_nus_osa_events(source: SourceRecord, content: str) -> list[Event]:
    cards = re.findall(
        r"<article\b[^>]*class=[\"'][^\"']*event-card[^\"']*[\"'][^>]*>(.*?)</article>",
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not cards:
        raise ParseError("nus_osa_events fixture has no event-card articles")

    events: list[Event] = []
    for card in cards:
        title, source_url = _extract_anchor(card)
        if not title:
            continue
        summary = _extract_class_text(card, "event-summary")
        venue = _extract_class_text(card, "event-venue")
        date_text = _extract_class_text(card, "event-date")
        tags = _extract_list_items(card, "event-taxonomy")
        category = _category_from_tags(tags, source.categories_hint)
        audience_hint = _audience_hint_from_tags(tags)
        start = _parse_dateish_datetime(date_text)
        events.append(
            Event(
                title=title,
                summary=summary,
                start=start,
                end=None,
                timezone=_format_timezone(start),
                venue=venue,
                campus=source.campus,
                institution=source.organisation,
                organiser=source.organisation,
                source_name=source.id,
                source_url=source_url or source.url,
                category=category,
                audience_hint=audience_hint,
                tags=tags or source.categories_hint.copy(),
            )
        )
    if not events:
        raise ParseError("nus_osa_events cards did not yield any events")
    return events


def parse_museum_cards(source: SourceRecord, content: str) -> list[Event]:
    cards = re.findall(
        r"<article\b[^>]*class=[\"'][^\"']*museum-event-card[^\"']*[\"'][^>]*>(.*?)</article>",
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not cards:
        raise ParseError("museum_cards fixture has no museum-event-card articles")

    events: list[Event] = []
    for card in cards:
        title, source_url = _extract_anchor(card)
        if not title:
            continue
        summary = _extract_class_text(card, "museum-event-summary")
        venue = _extract_class_text(card, "museum-event-venue")
        date_text = _extract_class_text(card, "museum-event-date")
        tags = _extract_list_items(card, "museum-event-taxonomy")
        category = _category_from_tags(tags, source.categories_hint)
        start = _parse_dateish_datetime(date_text)
        events.append(
            Event(
                title=title,
                summary=summary,
                start=start,
                end=None,
                timezone=_format_timezone(start),
                venue=venue,
                campus=source.campus,
                institution=source.organisation,
                organiser=source.organisation,
                source_name=source.id,
                source_url=source_url or source.url,
                category=category,
                audience_hint="public",
                tags=tags or source.categories_hint.copy(),
            )
        )
    if not events:
        raise ParseError("museum_cards entries did not yield any events")
    return events


def parse_filtered_event_cards(source: SourceRecord, content: str) -> list[Event]:
    cards = re.findall(
        r"<article\b[^>]*class=[\"'][^\"']*filtered-event-card[^\"']*[\"'][^>]*>(.*?)</article>",
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not cards:
        raise ParseError("filtered_event_cards fixture has no filtered-event-card articles")

    events: list[Event] = []
    for card in cards:
        title, source_url = _extract_anchor(card)
        if not title:
            continue
        summary = _extract_class_text(card, "filtered-event-summary")
        venue = _extract_class_text(card, "filtered-event-venue")
        date_text = _extract_class_text(card, "filtered-event-date")
        tags = _extract_list_items(card, "filtered-event-taxonomy")
        category = _category_from_tags(tags, source.categories_hint)
        audience_hint = _audience_hint_from_tags(tags)
        start = _parse_dateish_datetime(date_text)
        events.append(
            Event(
                title=title,
                summary=summary,
                start=start,
                end=None,
                timezone=_format_timezone(start),
                venue=venue,
                campus=source.campus,
                institution=source.organisation,
                organiser=source.organisation,
                source_name=source.id,
                source_url=source_url or source.url,
                category=category,
                audience_hint=audience_hint,
                tags=tags or source.categories_hint.copy(),
            )
        )
    if not events:
        raise ParseError("filtered_event_cards entries did not yield any events")
    return events


def parse_card_layout(
    source: SourceRecord,
    content: str,
    spec: dict[str, str],
) -> list[Event]:
    card_pattern = (
        r"<article\b[^>]*class=[\"'][^\"']*"
        + re.escape(spec["card_class"])
        + r"[^\"']*[\"'][^>]*>(.*?)</article>"
    )
    cards = re.findall(card_pattern, content, flags=re.IGNORECASE | re.DOTALL)
    if not cards:
        raise ParseError(
            f"{source.parser_family} fixture has no {spec['card_class']} articles"
        )

    events: list[Event] = []
    for card in cards:
        title, source_url = _extract_anchor(card)
        if not title:
            continue
        summary = _extract_class_text(card, spec["summary_class"])
        venue = _extract_class_text(card, spec["venue_class"])
        date_text = _extract_class_text(card, spec["date_class"])
        tags = _extract_list_items(card, spec["taxonomy_class"])
        category = _category_from_tags(tags, source.categories_hint)
        if spec.get("audience_mode") == "from_tags":
            audience_hint = _audience_hint_from_tags(tags)
        else:
            audience_hint = spec.get("audience_mode", "public")
        start = _parse_dateish_datetime(date_text)
        events.append(
            Event(
                title=title,
                summary=summary,
                start=start,
                end=None,
                timezone=_format_timezone(start),
                venue=venue,
                campus=source.campus,
                institution=source.organisation,
                organiser=source.organisation,
                source_name=source.id,
                source_url=source_url or source.url,
                category=category,
                audience_hint=audience_hint,
                tags=tags or source.categories_hint.copy(),
            )
        )
    if not events:
        raise ParseError(f"{source.parser_family} entries did not yield any events")
    return events


def parse_html_structured_events(source: SourceRecord, content: str) -> list[Event]:
    scripts = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not scripts:
        raise ParseError(
            f"{source.parser_family} has no structured Event data and needs a dedicated parser"
        )

    events: list[Event] = []
    for script in scripts:
        try:
            payload = json.loads(script.strip())
        except json.JSONDecodeError:
            continue
        for item in _walk_structured_items(payload):
            item_type = item.get("@type")
            if item_type == "Event" or (
                isinstance(item_type, list) and "Event" in item_type
            ):
                events.append(_event_from_json_ld(source, item))
    if not events:
        raise ParseError(
            f"{source.parser_family} found structured data but no Event records"
        )
    return events


def _walk_structured_items(payload: object) -> Iterable[dict[str, object]]:
    if isinstance(payload, dict):
        if "@graph" in payload and isinstance(payload["@graph"], list):
            for item in payload["@graph"]:
                yield from _walk_structured_items(item)
        yield payload
    elif isinstance(payload, list):
        for item in payload:
            yield from _walk_structured_items(item)


def _event_from_json_ld(source: SourceRecord, item: dict[str, object]) -> Event:
    location = item.get("location")
    venue = ""
    if isinstance(location, dict):
        venue = str(location.get("name", ""))
    elif isinstance(location, str):
        venue = location

    organiser = source.organisation
    organizer_payload = item.get("organizer")
    if isinstance(organizer_payload, dict):
        organiser = str(organizer_payload.get("name", organiser))
    elif isinstance(organizer_payload, str):
        organiser = organizer_payload

    source_url = str(item.get("url") or source.url)
    start = _parse_iso_datetime(item.get("startDate"))
    end = _parse_iso_datetime(item.get("endDate"))

    return Event(
        title=str(item.get("name") or "(untitled event)"),
        summary=str(item.get("description") or ""),
        start=start,
        end=end,
        timezone=_format_timezone(start),
        venue=venue,
        campus=source.campus,
        institution=source.organisation,
        organiser=organiser,
        source_name=source.id,
        source_url=source_url,
        category=source.categories_hint[0] if source.categories_hint else "event",
        audience_hint="public",
        tags=source.categories_hint.copy(),
    )


def _find_text(node: ElementTree.Element, *tags: str) -> str:
    for tag in tags:
        child = node.find(tag)
        if child is not None and child.text:
            return child.text.strip()
    return ""


def _parse_datetime(value: str) -> datetime | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return _parse_iso_datetime(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed


def _parse_iso_datetime(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed


def _parse_dateish_datetime(value: str) -> datetime | None:
    if not value:
        return None
    candidate = value.strip().split("|", 1)[0].strip()
    for splitter in [" to ", " – ", " — ", " - "]:
        if splitter in candidate:
            candidate = candidate.split(splitter, 1)[0].strip()
            break
    for pattern in ("%d %b %Y", "%d %B %Y", "%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(candidate, pattern).replace(tzinfo=UTC)
        except ValueError:
            continue
    return _parse_iso_datetime(candidate)


def _format_timezone(value: datetime | None) -> str:
    if value is None or value.tzinfo is None:
        return ""
    return value.tzname() or str(value.tzinfo)


def _extract_anchor(fragment: str) -> tuple[str, str]:
    match = re.search(
        r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
        fragment,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return "", ""
    return _clean_html_text(match.group(2)), unescape(match.group(1).strip())


def _extract_class_text(fragment: str, class_name: str) -> str:
    pattern = (
        r"<[^>]*class=[\"'][^\"']*"
        + re.escape(class_name)
        + r"[^\"']*[\"'][^>]*>(.*?)</[^>]+>"
    )
    match = re.search(pattern, fragment, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    return _clean_html_text(match.group(1))


def _extract_list_items(fragment: str, class_name: str) -> list[str]:
    pattern = (
        r"<ul\b[^>]*class=[\"'][^\"']*"
        + re.escape(class_name)
        + r"[^\"']*[\"'][^>]*>(.*?)</ul>"
    )
    match = re.search(pattern, fragment, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    return [
        _clean_html_text(item)
        for item in re.findall(r"<li[^>]*>(.*?)</li>", match.group(1), flags=re.DOTALL)
        if _clean_html_text(item)
    ]


def _clean_html_text(value: str) -> str:
    stripped = re.sub(r"<[^>]+>", " ", value)
    return " ".join(unescape(stripped).split())


def _audience_hint_from_tags(tags: list[str]) -> str:
    normalized = {tag.lower() for tag in tags}
    if "for public" in normalized or "public" in normalized:
        return "public"
    if "for nus community" in normalized or "nus community" in normalized:
        return "campus_only"
    return "unknown"


def _category_from_tags(tags: list[str], fallback: list[str]) -> str:
    audience_tags = {"for public", "public", "for nus community", "nus community"}
    for tag in tags:
        if tag.lower() not in audience_tags:
            return tag.lower().replace(" ", "_")
    if fallback:
        return fallback[0]
    return "event"


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "feed"
