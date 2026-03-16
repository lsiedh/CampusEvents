import unittest

from campus_events.models import SourceRecord
from campus_events.parsers import ParseError, parse_source


class LivePayloadParserTests(unittest.TestCase):
    def test_parse_ntu_event_portal_json_payload(self) -> None:
        source = SourceRecord(
            id="ntu_main_events",
            campus="NTU",
            organisation="NTU",
            governance="university",
            url="https://www.ntu.edu.sg/events",
            source_kind="html",
            parser_family="ntu_event_portal",
            fixture_slug="ntu_main_events",
            categories_hint=["talks", "seminars", "campus_events"],
            priority="high",
        )
        payload = """
        {
          "totalPages": 1,
          "totalItems": 1,
          "items": [
            {
              "title": "Professor Chen Charng Ning Distinguished Lecture 2026",
              "url": "https://www.ntu.edu.sg/events/detail/2026/03/17/default-calendar/professor-chen-charng-ning-distinguished-lecture-2026",
              "tag": "Conferences & Seminars",
              "description": "A distinguished annual lecture.",
              "date": "17 Mar 2026",
              "location": "Auditorium, NTU@one-north",
              "eventstart": "20260317T183000",
              "eventend": "20260317T205000"
            }
          ]
        }
        """

        events = parse_source(source, payload)

        self.assertEqual(len(events), 1)
        self.assertEqual(
            events[0].title,
            "Professor Chen Charng Ning Distinguished Lecture 2026",
        )
        self.assertEqual(events[0].category, "conferences_&_seminars")
        self.assertEqual(events[0].venue, "Auditorium, NTU@one-north")
        self.assertEqual(events[0].start.isoformat(), "2026-03-17T18:30:00+00:00")

    def test_parse_scelse_ajax_json_payload(self) -> None:
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
        payload = r"""
        {
          "status": "success",
          "results": "<div class=\"et_pb_column\"><div class=\"team-wrapper\"><div class=\"team-content-wrapper\"><div class=\"team-clip\"><a href=\"https:\/\/scelse.sg\/event\/qmra\/\"><div class=\"team-container\"><div class=\"newsTag 2\">Talks &amp; Presentation<\/div><div class=\"team-title\"><h3>Quantitative microbial risk assessment<\/h3><\/div><div class=\"newsPost_date\">Tuesday, 20 Jan 2026, 10am-11am, SBS TR+5 (SBS-01N-25)<\/div><\/div><\/a><\/div><\/div><\/div><\/div>"
        }
        """

        events = parse_source(source, payload)

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].title, "Quantitative microbial risk assessment")
        self.assertEqual(events[0].category, "talks_&_presentation")
        self.assertEqual(events[0].venue, "SBS TR+5 (SBS-01N-25)")
        self.assertEqual(events[0].start.isoformat(), "2026-01-20T00:00:00+00:00")

    def test_detect_incapsula_block_page(self) -> None:
        source = SourceRecord(
            id="nus_osa_events",
            campus="NUS",
            organisation="Office of Student Affairs",
            governance="university",
            url="https://osa.nus.edu.sg/events/",
            source_kind="html",
            parser_family="nus_osa_events",
            fixture_slug="nus_osa_events",
            categories_hint=["arts", "sports"],
            priority="high",
        )

        with self.assertRaisesRegex(ParseError, "Incapsula"):
            parse_source(
                source,
                '<html><script src="/_Incapsula_Resource"></script>'
                "Incapsula incident ID"
                "</html>",
            )

    def test_ntu_event_detail_listing_can_parse_json_payload(self) -> None:
        source = SourceRecord(
            id="ntu_ias_events",
            campus="NTU",
            organisation="Institute of Advanced Studies",
            governance="institute",
            url="https://www.ntu.edu.sg/ias/news-events/events",
            source_kind="html",
            parser_family="ntu_event_detail_listing",
            fixture_slug="ntu_ias_events",
            categories_hint=["lectures", "seminars", "conferences"],
            priority="high",
        )
        payload = """
        {
          "totalPages": 1,
          "totalItems": 1,
          "items": [
            {
              "title": "Does an Isolated Quantum System Relax?",
              "url": "https://www.ntu.edu.sg/ias/news-events/events/detail/2026/03/23/default-calendar/does-an-isolated-quantum-system-relax",
              "tag": "Conferences & Seminars",
              "description": "IAS Frontiers Seminars.",
              "date": "23 Mar 2026",
              "time": "11.00 AM - 12.00 PM",
              "location": "Executive Classroom 2 (SPMS)",
              "eventstart": "20260323T110000",
              "eventend": "20260323T120000"
            }
          ]
        }
        """

        events = parse_source(source, payload)

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].title, "Does an Isolated Quantum System Relax?")
        self.assertEqual(events[0].venue, "Executive Classroom 2 (SPMS)")
        self.assertEqual(events[0].category, "conferences_&_seminars")

    def test_museum_listing_can_parse_live_img_card_html(self) -> None:
        source = SourceRecord(
            id="ntu_museum_exhibitions",
            campus="NTU",
            organisation="NTU Museum",
            governance="university",
            url="https://www.ntu.edu.sg/life-at-ntu/museum/exhibitions",
            source_kind="html",
            parser_family="museum_listing",
            fixture_slug="ntu_museum_exhibitions",
            categories_hint=["exhibitions", "workshops", "gallery_events"],
            priority="high",
        )
        html = """
        <div class="card-grids">
          <a class="img-card" href="/life-at-ntu/museum/exhibitions/featured/on-the-cusp">
            <div class="img-card__body">
              <h3 class="img-card__title">On the cusp</h3>
              <p class="img-card__desc">An exhibition on memory, connection and identity.</p>
            </div>
          </a>
        </div>
        """

        events = parse_source(source, html)

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].title, "On the cusp")
        self.assertEqual(events[0].venue, "NTU Museum")
        self.assertEqual(events[0].category, "exhibitions")

    def test_ntu_event_detail_listing_can_parse_live_img_card_html(self) -> None:
        source = SourceRecord(
            id="ntu_sbs_events",
            campus="NTU",
            organisation="School of Biological Sciences",
            governance="school",
            url="https://www.ntu.edu.sg/sbs/news-and-events/events",
            source_kind="html",
            parser_family="ntu_event_detail_listing",
            fixture_slug="ntu_sbs_events",
            categories_hint=["seminars", "symposia", "workshops"],
            priority="medium",
        )
        html = """
        <div class="img-card img-card--horizontal">
          <a href="/sbs/news-and-events/events/detail/2026/05/25/default-calendar/4th-annual-symposium" class="img-card__link"></a>
          <div class="img-card__body">
            <span class="img-card__subtitle">Conferences &amp; Seminars</span>
            <h3 class="img-card__title">4th Annual Symposium - Mycobacteria 2026</h3>
            <button class="calendar-button" type="button"
              data-title="4th Annual Symposium - Mycobacteria 2026"
              data-location=""
              data-all-day="1"
              data-start="2026-05-25"
              data-end="2026-05-27"
              data-description="<p>Symposium description.</p>"></button>
          </div>
        </div>
        """

        events = parse_source(source, html)

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].title, "4th Annual Symposium - Mycobacteria 2026")
        self.assertEqual(events[0].category, "conferences_&_seminars")
        self.assertEqual(events[0].start.isoformat(), "2026-05-25T00:00:00+00:00")
