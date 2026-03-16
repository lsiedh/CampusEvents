import unittest
from pathlib import Path

from campus_events.models import SourceRecord
from campus_events.parsers import parse_filtered_event_cards


FIXTURE_PATH = Path("tests/fixtures/ntu_scelse_all_events_sample_2026-03-16.html")


class FilteredEventCardsParserTests(unittest.TestCase):
    def test_parse_filtered_event_cards_from_saved_fixture(self) -> None:
        content = FIXTURE_PATH.read_text(encoding="utf-8")
        source = SourceRecord(
            id="ntu_scelse_all_events",
            campus="NTU",
            organisation="SCELSE",
            governance="hosted_institute",
            url="https://scelse.sg/news-events/all-events/",
            source_kind="html",
            parser_family="filtered_event_cards",
            fixture_slug="ntu_scelse_all_events",
            categories_hint=["conferences", "seminars", "talks", "outreach", "webinars"],
            priority="high",
        )

        events = parse_filtered_event_cards(source, content)

        self.assertEqual(len(events), 3)
        self.assertEqual(events[0].title, "Microbial Cities Symposium")
        self.assertEqual(events[0].category, "conferences")
        self.assertEqual(events[0].audience_hint, "public")
        self.assertEqual(events[1].category, "outreach")
        self.assertEqual(events[2].audience_hint, "campus_only")
