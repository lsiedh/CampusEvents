import unittest
from pathlib import Path

from campus_events.models import SourceRecord
from campus_events.parsers import parse_museum_cards


FIXTURE_PATH = Path("tests/fixtures/nus_museum_sample_2026-03-16.html")


class MuseumCardsParserTests(unittest.TestCase):
    def test_parse_museum_cards_from_saved_fixture(self) -> None:
        content = FIXTURE_PATH.read_text(encoding="utf-8")
        source = SourceRecord(
            id="nus_museum",
            campus="NUS",
            organisation="NUS Museum",
            governance="university",
            url="https://museum.nus.edu.sg/",
            source_kind="html",
            parser_family="museum_cards",
            fixture_slug="nus_museum",
            categories_hint=["exhibitions", "gallery_events", "talks"],
            priority="high",
        )

        events = parse_museum_cards(source, content)

        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].title, "Ink and Empire")
        self.assertEqual(events[0].category, "exhibitions")
        self.assertEqual(events[1].category, "talks")
        self.assertIn("curatorial team", events[1].summary.lower())
