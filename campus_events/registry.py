from __future__ import annotations

from pathlib import Path

import yaml

from campus_events.models import SourceRecord


REQUIRED_SOURCE_KEYS = {
    "id",
    "campus",
    "organisation",
    "governance",
    "url",
    "source_kind",
    "parser_family",
    "fixture_slug",
    "categories_hint",
    "priority",
}


def load_registry(path: str | Path) -> list[SourceRecord]:
    registry_path = Path(path)
    payload = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Registry {registry_path} did not parse into a mapping")

    raw_sources = payload.get("sources")
    if not isinstance(raw_sources, list):
        raise ValueError(f"Registry {registry_path} is missing a top-level sources list")

    sources: list[SourceRecord] = []
    for raw_source in raw_sources:
        if not isinstance(raw_source, dict):
            raise ValueError("Each registry entry must be a mapping")
        missing = sorted(REQUIRED_SOURCE_KEYS - raw_source.keys())
        if missing:
            raise ValueError(
                f"Registry source {raw_source.get('id', '<unknown>')} is missing keys: "
                f"{', '.join(missing)}"
            )
        source = SourceRecord(
            id=str(raw_source["id"]),
            campus=str(raw_source["campus"]),
            organisation=str(raw_source["organisation"]),
            governance=str(raw_source["governance"]),
            url=str(raw_source["url"]),
            source_kind=str(raw_source["source_kind"]),
            parser_family=str(raw_source["parser_family"]),
            fixture_slug=str(raw_source["fixture_slug"]),
            categories_hint=[str(value) for value in raw_source["categories_hint"]],
            priority=str(raw_source["priority"]),
            active=bool(raw_source.get("active", True)),
            trust_level=str(raw_source.get("trust_level", "validated")),
        )
        sources.append(source)
    return sources

