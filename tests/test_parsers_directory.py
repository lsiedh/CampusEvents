import unittest
from pathlib import Path

from campus_events.models import SourceRecord
from campus_events.parsers import parse_nus_coe_rss_directory


class NusCoeDirectoryParserTests(unittest.TestCase):
    def test_parse_nus_coe_rss_directory_expands_downstream_feeds(self) -> None:
        content = Path("tests/fixtures/nus_coe_rss_directory_sample_2026-03-16.html").read_text(
            encoding="utf-8"
        )
        source = SourceRecord(
            id="nus_coe_rss_directory",
            campus="NUS",
            organisation="NUS Calendar of Events",
            governance="university",
            url="https://myaces.nus.edu.sg/CoE/jsp/coeRss.jsp",
            source_kind="rss_directory",
            parser_family="nus_coe_rss_directory",
            fixture_slug="nus_coe_rss_directory",
            categories_hint=["arts", "seminars", "lectures"],
            priority="high",
        )

        feeds = parse_nus_coe_rss_directory(source, content)

        self.assertEqual(len(feeds), 3)
        self.assertEqual(feeds[0].id, "nus_coe_rss_directory:arts")
        self.assertEqual(feeds[0].parser_family, "generic_rss")
        self.assertEqual(
            feeds[1].url,
            "https://myaces.nus.edu.sg/CoE/jsp/coeGenRss.jsp?Cat=2",
        )
