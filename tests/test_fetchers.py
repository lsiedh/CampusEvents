import unittest
from unittest.mock import MagicMock, patch

from campus_events.fetchers import fetch_source
from campus_events.models import SourceRecord


class FetcherRequestShapeTests(unittest.TestCase):
    def test_ntu_event_portal_uses_json_endpoint(self) -> None:
        source = SourceRecord(
            id="ntu_main_events",
            campus="NTU",
            organisation="NTU",
            governance="university",
            url="https://www.ntu.edu.sg/events",
            source_kind="html",
            parser_family="ntu_event_portal",
            fixture_slug="ntu_main_events",
            categories_hint=["talks"],
            priority="high",
        )
        response = MagicMock()
        response.read.return_value = b'{"items":[]}'
        response.headers.get_content_type.return_value = "application/json"
        context = MagicMock()
        context.__enter__.return_value = response
        context.__exit__.return_value = None

        with patch("campus_events.fetchers.request.urlopen", return_value=context) as open_mock:
            fetch_source(source)

        request_obj = open_mock.call_args.args[0]
        self.assertEqual(request_obj.full_url, "https://www.ntu.edu.sg/events/GetEvents/")
        self.assertEqual(request_obj.get_method(), "GET")

    def test_scelse_uses_ajax_post_endpoint(self) -> None:
        source = SourceRecord(
            id="ntu_scelse_all_events",
            campus="NTU",
            organisation="SCELSE",
            governance="hosted_institute",
            url="https://scelse.sg/news-events/all-events/",
            source_kind="html",
            parser_family="filtered_event_cards",
            fixture_slug="ntu_scelse_all_events",
            categories_hint=["talks"],
            priority="high",
        )
        response = MagicMock()
        response.read.return_value = b'{"status":"success","results":""}'
        response.headers.get_content_type.return_value = "application/json"
        context = MagicMock()
        context.__enter__.return_value = response
        context.__exit__.return_value = None

        with patch("campus_events.fetchers.request.urlopen", return_value=context) as open_mock:
            fetch_source(source)

        request_obj = open_mock.call_args.args[0]
        self.assertEqual(request_obj.full_url, "https://scelse.sg/wp-admin/admin-ajax.php")
        self.assertEqual(request_obj.get_method(), "POST")
        self.assertIn(b"action=get_all_posts_by_page", request_obj.data)
        self.assertIn(b"post_type=event", request_obj.data)

    def test_ntu_event_detail_listing_uses_derived_json_endpoint(self) -> None:
        source = SourceRecord(
            id="ntu_ias_events",
            campus="NTU",
            organisation="Institute of Advanced Studies",
            governance="institute",
            url="https://www.ntu.edu.sg/ias/news-events/events",
            source_kind="html",
            parser_family="ntu_event_detail_listing",
            fixture_slug="ntu_ias_events",
            categories_hint=["lectures"],
            priority="high",
        )
        response = MagicMock()
        response.read.return_value = b'{"items":[]}'
        response.headers.get_content_type.return_value = "application/json"
        context = MagicMock()
        context.__enter__.return_value = response
        context.__exit__.return_value = None

        with patch("campus_events.fetchers.request.urlopen", return_value=context) as open_mock:
            fetch_source(source)

        request_obj = open_mock.call_args.args[0]
        self.assertEqual(
            request_obj.full_url,
            "https://www.ntu.edu.sg/ias/news-events/events/GetEvents/",
        )

    def test_ntu_event_detail_listing_strips_query_when_deriving_endpoint(self) -> None:
        source = SourceRecord(
            id="ntu_cee_events",
            campus="NTU",
            organisation="School of Civil and Environmental Engineering",
            governance="school",
            url="https://www.ntu.edu.sg/cee/news-events/events?listingKeyword=&categories=all&interests=all&audiences=all&page=1",
            source_kind="html",
            parser_family="ntu_event_detail_listing",
            fixture_slug="ntu_cee_events",
            categories_hint=["lectures"],
            priority="high",
        )
        response = MagicMock()
        response.read.return_value = b'{"items":[]}'
        response.headers.get_content_type.return_value = "application/json"
        context = MagicMock()
        context.__enter__.return_value = response
        context.__exit__.return_value = None

        with patch("campus_events.fetchers.request.urlopen", return_value=context) as open_mock:
            fetch_source(source)

        request_obj = open_mock.call_args.args[0]
        self.assertEqual(
            request_obj.full_url,
            "https://www.ntu.edu.sg/cee/news-events/events/GetEvents/",
        )

    def test_ntu_sbs_events_stays_on_html_listing_page(self) -> None:
        source = SourceRecord(
            id="ntu_sbs_events",
            campus="NTU",
            organisation="School of Biological Sciences",
            governance="school",
            url="https://www.ntu.edu.sg/sbs/news-and-events/events",
            source_kind="html",
            parser_family="ntu_event_detail_listing",
            fixture_slug="ntu_sbs_events",
            categories_hint=["seminars"],
            priority="medium",
        )
        response = MagicMock()
        response.read.return_value = b"<html></html>"
        response.headers.get_content_type.return_value = "text/html"
        context = MagicMock()
        context.__enter__.return_value = response
        context.__exit__.return_value = None

        with patch("campus_events.fetchers.request.urlopen", return_value=context) as open_mock:
            fetch_source(source)

        request_obj = open_mock.call_args.args[0]
        self.assertEqual(
            request_obj.full_url,
            "https://www.ntu.edu.sg/sbs/news-and-events/events",
        )

    def test_ntu_special_index_sources_use_event_endpoints(self) -> None:
        response = MagicMock()
        response.read.return_value = b'{"items":[]}'
        response.headers.get_content_type.return_value = "application/json"
        context = MagicMock()
        context.__enter__.return_value = response
        context.__exit__.return_value = None

        cases = [
            (
                "ntu_erian_news_events",
                "institute_news_events",
                "https://www.ntu.edu.sg/erian/news-events",
                "https://www.ntu.edu.sg/erian/news-events/events/GetEvents/",
            ),
            (
                "ntu_cceb_seminars",
                "seminar_hub",
                "https://www.ntu.edu.sg/cceb/news-and-events/seminars-and-lecture-series",
                "https://www.ntu.edu.sg/cceb/news-and-events/events/GetEvents/",
            ),
        ]

        for source_id, parser_family, url, expected in cases:
            source = SourceRecord(
                id=source_id,
                campus="NTU",
                organisation="NTU",
                governance="institute",
                url=url,
                source_kind="html",
                parser_family=parser_family,
                fixture_slug="fixture",
                categories_hint=["seminars"],
                priority="high",
            )
            with self.subTest(source_id=source_id):
                with patch("campus_events.fetchers.request.urlopen", return_value=context) as open_mock:
                    fetch_source(source)
                request_obj = open_mock.call_args.args[0]
                self.assertEqual(request_obj.full_url, expected)
