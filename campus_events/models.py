from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime


@dataclass(slots=True)
class SourceRecord:
    id: str
    campus: str
    organisation: str
    governance: str
    url: str
    source_kind: str
    parser_family: str
    fixture_slug: str
    categories_hint: list[str]
    priority: str
    active: bool = True
    trust_level: str = "validated"

    def clone_with(self, **overrides: object) -> "SourceRecord":
        payload = {
            "id": self.id,
            "campus": self.campus,
            "organisation": self.organisation,
            "governance": self.governance,
            "url": self.url,
            "source_kind": self.source_kind,
            "parser_family": self.parser_family,
            "fixture_slug": self.fixture_slug,
            "categories_hint": self.categories_hint.copy(),
            "priority": self.priority,
            "active": self.active,
            "trust_level": self.trust_level,
        }
        payload.update(overrides)
        return SourceRecord(**payload)


@dataclass(slots=True)
class Event:
    title: str
    summary: str
    start: datetime | None
    end: datetime | None
    timezone: str
    venue: str
    campus: str
    institution: str
    organiser: str
    source_name: str
    source_url: str
    category: str
    audience_hint: str
    tags: list[str] = field(default_factory=list)

    def dedupe_key(self) -> tuple[str, date | None, str]:
        event_date = self.start.date() if self.start else None
        normalized_title = " ".join(self.title.lower().split())
        normalized_venue = " ".join(self.venue.lower().split())
        return normalized_title, event_date, normalized_venue

    def sort_key(self) -> tuple[datetime, str, str]:
        sort_start = self.start or datetime.max.replace(tzinfo=UTC)
        return sort_start, self.campus, self.title.lower()


@dataclass(slots=True)
class SourceAttempt:
    source_id: str
    source_url: str
    parser_family: str
    fetch_ok: bool = False
    parse_ok: bool = False
    fetch_error: str | None = None
    parse_error: str | None = None
    candidate_count: int = 0
    kept_count: int = 0


@dataclass(slots=True)
class RunReport:
    run_date: str
    mode: str
    recipient: str
    expected_recipient: str
    recipient_valid: bool
    duplicate_detected: bool
    digest_generated: bool
    digest_delivered: bool
    status: str
    subject: str
    validation_errors: list[str]
    source_attempts: list[SourceAttempt]
    candidate_count: int
    filtered_count: int
    deduped_count: int
    summary_path: str
    digest_path: str | None
    delivery_error: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
