import unittest
from pathlib import Path

from campus_events.models import SourceRecord
from campus_events.parsers import parse_source


CASES = [
    (
        "ntu_main_events",
        "ntu_event_portal",
        "tests/fixtures/ntu_main_events_live_2026-03-16.json",
        ["talks", "seminars", "campus_events"],
        "On the Cusp",
    ),
    (
        "ntu_ias_events",
        "ntu_event_detail_listing",
        "tests/fixtures/ntu_ias_events_live_2026-03-16.json",
        ["lectures", "seminars", "conferences"],
        "Does an Isolated Quantum System Relax? Probing the Emergence of the Classical World by Prof Jörg Schmeidmayer",
    ),
    (
        "ntu_mae_events",
        "ntu_event_detail_listing",
        "tests/fixtures/ntu_mae_events_live_2026-03-16.json",
        ["seminars", "lectures", "school_events"],
        "MAE Speaker Series Seminar on Building with liquids in weightlessness",
    ),
    (
        "ntu_sbs_events",
        "ntu_event_detail_listing",
        "tests/fixtures/ntu_sbs_events_live_2026-03-16.html",
        ["seminars", "symposia", "workshops"],
        "4th Annual Symposium",
    ),
    (
        "ntu_erian_news_events",
        "institute_news_events",
        "tests/fixtures/ntu_erian_events_live_2026-03-16.json",
        ["talks"],
        "World Hydrogen Energy Conference 2026",
    ),
    (
        "ntu_cceb_seminars",
        "seminar_hub",
        "tests/fixtures/ntu_cceb_events_live_2026-03-16.json",
        ["seminars", "lecture_series"],
        "Vascular Nanomedicine Delivery: Fortuitous Homing vs Cognizant Targeting",
    ),
    (
        "ntu_museum_exhibitions",
        "museum_listing",
        "tests/fixtures/ntu_museum_exhibitions_live_2026-03-16.html",
        ["exhibitions", "workshops", "gallery_events"],
        "On the cusp",
    ),
]


class LiveFixtureParserTests(unittest.TestCase):
    def test_live_fixture_snapshots_parse(self) -> None:
        for source_id, parser_family, fixture_path, categories_hint, expected_title in CASES:
            with self.subTest(source_id=source_id):
                source = SourceRecord(
                    id=source_id,
                    campus="NTU",
                    organisation="NTU",
                    governance="university",
                    url="https://example.com",
                    source_kind="html",
                    parser_family=parser_family,
                    fixture_slug="fixture",
                    categories_hint=categories_hint,
                    priority="high",
                )
                content = Path(fixture_path).read_text(encoding="utf-8")
                events = parse_source(source, content)
                self.assertGreaterEqual(len(events), 1)
                titles = [event.title for event in events]
                self.assertTrue(
                    any(expected_title in title for title in titles),
                    msg=f"{expected_title!r} not found in {titles!r}",
                )
