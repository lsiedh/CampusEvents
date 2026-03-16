import unittest
from pathlib import Path

from campus_events.models import SourceRecord
from campus_events.parsers import parse_nus_osa_events


FIXTURE_PATH = Path("tests/fixtures/nus_osa_events_sample_2026-03-16.html")


class NusOsaParserTests(unittest.TestCase):
    def test_parse_nus_osa_events_from_saved_fixture(self) -> None:
        content = FIXTURE_PATH.read_text(encoding="utf-8")
        source = SourceRecord(
            id="nus_osa_events",
            campus="NUS",
            organisation="Office of Student Affairs",
            governance="university",
            url="https://osa.nus.edu.sg/events/",
            source_kind="html",
            parser_family="nus_osa_events",
            fixture_slug="nus_osa_events",
            categories_hint=["arts", "sports", "public_events"],
            priority="high",
        )

        events = parse_nus_osa_events(source, content)

        self.assertEqual(len(events), 3)
        self.assertEqual(events[0].title, "Campus Open Mic: Night Shift")
        self.assertEqual(events[0].venue, "UTown Green")
        self.assertEqual(events[0].category, "arts")
        self.assertEqual(events[0].audience_hint, "public")
        self.assertEqual(events[1].audience_hint, "campus_only")
        self.assertIn("beginner and family-friendly routes", events[2].summary.lower())
