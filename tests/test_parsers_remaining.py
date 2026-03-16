import unittest
from pathlib import Path

from campus_events.models import SourceRecord
from campus_events.parsers import parse_source


CASES = [
    (
        "nus_arts_festival",
        "tests/fixtures/nus_arts_festival_sample_2026-03-16.html",
        "Campus Arts Festival Night",
        "performances",
    ),
    (
        "heritage_programmes",
        "tests/fixtures/nus_baba_house_sample_2026-03-16.html",
        "Peranakan Storytelling Evening",
        "cultural_programmes",
    ),
    (
        "taxonomy_events",
        "tests/fixtures/nus_fass_events_sample_2026-03-16.html",
        "Cities and Memory Forum",
        "talks",
    ),
    (
        "detail_cards",
        "tests/fixtures/nus_sph_events_sample_2026-03-16.html",
        "Global Health Policy Roundtable",
        "conferences",
    ),
    (
        "series_and_conference_index",
        "tests/fixtures/nus_math_events_sample_2026-03-16.html",
        "Probability Colloquium",
        "lectures",
    ),
    (
        "upcoming_events_listing",
        "tests/fixtures/nus_cqt_upcoming_events_sample_2026-03-16.html",
        "Quantum Sensing Workshop",
        "workshops",
    ),
    (
        "seminar_series_listing",
        "tests/fixtures/nus_mbi_seminar_series_sample_2026-03-16.html",
        "Cell Mechanics Seminar",
        "seminars",
    ),
    (
        "ntu_event_portal",
        "tests/fixtures/ntu_main_events_sample_2026-03-16.html",
        "NTU Innovation Day",
        "campus_events",
    ),
    (
        "ntu_event_detail_listing",
        "tests/fixtures/ntu_event_detail_listing_sample_2026-03-16.html",
        "Advanced Manufacturing Lecture",
        "lectures",
    ),
    (
        "museum_listing",
        "tests/fixtures/ntu_museum_exhibitions_sample_2026-03-16.html",
        "Tropic Light Exhibition",
        "exhibitions",
    ),
    (
        "seminar_hub",
        "tests/fixtures/ntu_cceb_seminars_sample_2026-03-16.html",
        "Catalysis Frontiers Seminar",
        "lecture_series",
    ),
    (
        "institute_news_events",
        "tests/fixtures/ntu_erian_news_events_sample_2026-03-16.html",
        "Energy Resilience Dialogue",
        "talks",
    ),
]


class RemainingParserFamilyTests(unittest.TestCase):
    def test_remaining_parser_families_from_saved_fixtures(self) -> None:
        for parser_family, fixture_path, expected_title, expected_category in CASES:
            with self.subTest(parser_family=parser_family):
                content = Path(fixture_path).read_text(encoding="utf-8")
                source = SourceRecord(
                    id=f"{parser_family}_source",
                    campus="NUS" if parser_family.startswith("nus_") else "NTU",
                    organisation=parser_family.replace("_", " ").title(),
                    governance="university",
                    url="https://example.com/source",
                    source_kind="html",
                    parser_family=parser_family,
                    fixture_slug="fixture",
                    categories_hint=[expected_category],
                    priority="high",
                )
                events = parse_source(source, content)
                self.assertEqual(len(events), 1)
                self.assertEqual(events[0].title, expected_title)
                self.assertEqual(events[0].category, expected_category)
