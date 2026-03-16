import unittest
from pathlib import Path

from campus_events.models import SourceRecord
from campus_events.parsers import parse_generic_rss


FIXTURE_PATH = Path("tests/fixtures/rsis_event_rss_sample_2026-03-16.xml")


class GenericRssParserTests(unittest.TestCase):
    def test_parse_generic_rss_from_saved_fixture(self) -> None:
        content = FIXTURE_PATH.read_text(encoding="utf-8")
        source = SourceRecord(
            id="rsis_event_rss",
            campus="NTU",
            organisation="RSIS",
            governance="hosted_institute",
            url="http://www.rsis.edu.sg/feed/?post_type=event",
            source_kind="rss",
            parser_family="generic_rss",
            fixture_slug="rsis_event_rss",
            categories_hint=["talks", "seminars", "conferences"],
            priority="high",
        )

        events = parse_generic_rss(source, content)

        self.assertEqual(len(events), 3)
        self.assertEqual(events[0].title, "Regional Security Seminar: Maritime Futures")
        self.assertEqual(
            events[0].source_url,
            "https://www.rsis.edu.sg/event/regional-security-seminar-maritime-futures/",
        )
        self.assertEqual(events[0].campus, "NTU")
        self.assertEqual(events[0].timezone, "UTC+08:00")
        self.assertIn("maritime strategy", events[0].summary.lower())
