import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from campus_events.delivery import DeliveryLedger
from campus_events.fetchers import FetchResult
from campus_events.models import Event
from campus_events.pipeline import run_pipeline


class PipelineTests(unittest.TestCase):
    def test_dry_run_blocks_when_no_events(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            with patch("campus_events.pipeline.fetch_source") as fetch_mock:
                fetch_mock.return_value.ok = False
                fetch_mock.return_value.content = None
                fetch_mock.return_value.error = "network blocked"
                report = run_pipeline(
                    registry_path="source_registry.yaml",
                    run_date=date(2026, 3, 16),
                    recipient="erichill27@gmail.com",
                    mode="dry-run",
                    output_root=str(Path(tmp_dir) / "runs"),
                    state_root=str(Path(tmp_dir) / "state"),
                )
        self.assertEqual(report.status, "blocked_validation")
        self.assertFalse(report.digest_generated)
        self.assertIn("no events remain", report.validation_errors[-1])

    def test_delivery_skips_duplicate(self) -> None:
        event = Event(
            title="Talk",
            summary="Summary",
            start=None,
            end=None,
            timezone="",
            venue="Venue",
            campus="NUS",
            institution="NUS",
            organiser="NUS",
            source_name="source",
            source_url="https://example.com",
            category="talks",
            audience_hint="public",
            tags=["talks"],
        )

        with TemporaryDirectory() as tmp_dir:
            state_root = Path(tmp_dir) / "state"
            ledger = DeliveryLedger(state_root / "delivery_ledger.json")
            ledger.record_delivery(
                "2026-03-16",
                "erichill27@gmail.com",
                "Campus Events Digest for 2026-03-16",
            )
            with patch("campus_events.pipeline.fetch_source") as fetch_mock, patch(
                "campus_events.pipeline.parse_source"
            ) as parse_mock:
                fetch_mock.return_value.ok = True
                fetch_mock.return_value.content = "<html></html>"
                fetch_mock.return_value.error = None
                parse_mock.return_value = [event]
                report = run_pipeline(
                    registry_path="source_registry.yaml",
                    run_date=date(2026, 3, 16),
                    recipient="erichill27@gmail.com",
                    mode="deliver",
                    output_root=str(Path(tmp_dir) / "runs"),
                    state_root=str(state_root),
                )
        self.assertEqual(report.status, "skipped_duplicate")
        self.assertTrue(report.digest_generated)
        self.assertTrue(report.duplicate_detected)

    def test_dry_run_generates_digest_from_saved_rss_fixture(self) -> None:
        fixture_path = Path("tests/fixtures/rsis_event_rss_sample_2026-03-16.xml")
        fixture_content = fixture_path.read_text(encoding="utf-8")

        def fake_fetch(source: object, timeout_seconds: int = 20) -> FetchResult:
            if getattr(source, "id", "") == "rsis_event_rss":
                return FetchResult(
                    ok=True,
                    content=fixture_content,
                    content_type="application/rss+xml",
                    error=None,
                )
            return FetchResult(
                ok=False,
                content=None,
                content_type=None,
                error="fixture not available for source",
            )

        with TemporaryDirectory() as tmp_dir:
            with patch("campus_events.pipeline.fetch_source", side_effect=fake_fetch):
                report = run_pipeline(
                    registry_path="source_registry.yaml",
                    run_date=date(2026, 3, 16),
                    recipient="erichill27@gmail.com",
                    mode="dry-run",
                    output_root=str(Path(tmp_dir) / "runs"),
                    state_root=str(Path(tmp_dir) / "state"),
                )

            self.assertEqual(report.status, "dry_run_valid")
            self.assertTrue(report.digest_generated)
            self.assertFalse(report.duplicate_detected)
            self.assertEqual(report.candidate_count, 3)
            self.assertEqual(report.filtered_count, 2)
            self.assertEqual(report.deduped_count, 1)
            self.assertIsNotNone(report.digest_path)
            digest_text = Path(report.digest_path).read_text(encoding="utf-8")
            self.assertIn("Regional Security Seminar: Maritime Futures", digest_text)
            self.assertNotIn("Lecture 3: Strategy and Defence", digest_text)

    def test_dry_run_generates_digest_from_rss_and_osa_fixtures(self) -> None:
        rss_fixture = Path("tests/fixtures/rsis_event_rss_sample_2026-03-16.xml").read_text(
            encoding="utf-8"
        )
        osa_fixture = Path("tests/fixtures/nus_osa_events_sample_2026-03-16.html").read_text(
            encoding="utf-8"
        )

        def fake_fetch(source: object, timeout_seconds: int = 20) -> FetchResult:
            source_id = getattr(source, "id", "")
            if source_id == "rsis_event_rss":
                return FetchResult(
                    ok=True,
                    content=rss_fixture,
                    content_type="application/rss+xml",
                    error=None,
                )
            if source_id == "nus_osa_events":
                return FetchResult(
                    ok=True,
                    content=osa_fixture,
                    content_type="text/html",
                    error=None,
                )
            return FetchResult(
                ok=False,
                content=None,
                content_type=None,
                error="fixture not available for source",
            )

        with TemporaryDirectory() as tmp_dir:
            with patch("campus_events.pipeline.fetch_source", side_effect=fake_fetch):
                report = run_pipeline(
                    registry_path="source_registry.yaml",
                    run_date=date(2026, 3, 16),
                    recipient="erichill27@gmail.com",
                    mode="dry-run",
                    output_root=str(Path(tmp_dir) / "runs"),
                    state_root=str(Path(tmp_dir) / "state"),
                )

            self.assertEqual(report.status, "dry_run_valid")
            self.assertEqual(report.candidate_count, 6)
            self.assertEqual(report.filtered_count, 4)
            self.assertEqual(report.deduped_count, 3)
            self.assertIsNotNone(report.digest_path)
            digest_text = Path(report.digest_path).read_text(encoding="utf-8")
            self.assertIn("Regional Security Seminar: Maritime Futures", digest_text)
            self.assertIn("Campus Open Mic: Night Shift", digest_text)
            self.assertIn("Sunset Fun Run", digest_text)
            self.assertNotIn("Inter-Hall Fitness Clinic", digest_text)

    def test_dry_run_generates_digest_from_rss_osa_and_museum_fixtures(self) -> None:
        rss_fixture = Path("tests/fixtures/rsis_event_rss_sample_2026-03-16.xml").read_text(
            encoding="utf-8"
        )
        osa_fixture = Path("tests/fixtures/nus_osa_events_sample_2026-03-16.html").read_text(
            encoding="utf-8"
        )
        museum_fixture = Path("tests/fixtures/nus_museum_sample_2026-03-16.html").read_text(
            encoding="utf-8"
        )

        def fake_fetch(source: object, timeout_seconds: int = 20) -> FetchResult:
            source_id = getattr(source, "id", "")
            if source_id == "rsis_event_rss":
                return FetchResult(
                    ok=True,
                    content=rss_fixture,
                    content_type="application/rss+xml",
                    error=None,
                )
            if source_id == "nus_osa_events":
                return FetchResult(
                    ok=True,
                    content=osa_fixture,
                    content_type="text/html",
                    error=None,
                )
            if source_id == "nus_museum":
                return FetchResult(
                    ok=True,
                    content=museum_fixture,
                    content_type="text/html",
                    error=None,
                )
            return FetchResult(
                ok=False,
                content=None,
                content_type=None,
                error="fixture not available for source",
            )

        with TemporaryDirectory() as tmp_dir:
            with patch("campus_events.pipeline.fetch_source", side_effect=fake_fetch):
                report = run_pipeline(
                    registry_path="source_registry.yaml",
                    run_date=date(2026, 3, 16),
                    recipient="erichill27@gmail.com",
                    mode="dry-run",
                    output_root=str(Path(tmp_dir) / "runs"),
                    state_root=str(Path(tmp_dir) / "state"),
                )

            self.assertEqual(report.status, "dry_run_valid")
            self.assertEqual(report.candidate_count, 8)
            self.assertEqual(report.filtered_count, 6)
            self.assertEqual(report.deduped_count, 5)
            self.assertIsNotNone(report.digest_path)
            digest_text = Path(report.digest_path).read_text(encoding="utf-8")
            self.assertIn("Regional Security Seminar: Maritime Futures", digest_text)
            self.assertIn("Campus Open Mic: Night Shift", digest_text)
            self.assertIn("Ink and Empire", digest_text)
            self.assertIn("Curator Tour: Material Worlds", digest_text)

    def test_dry_run_generates_digest_with_scelse_fixture(self) -> None:
        rss_fixture = Path("tests/fixtures/rsis_event_rss_sample_2026-03-16.xml").read_text(
            encoding="utf-8"
        )
        osa_fixture = Path("tests/fixtures/nus_osa_events_sample_2026-03-16.html").read_text(
            encoding="utf-8"
        )
        museum_fixture = Path("tests/fixtures/nus_museum_sample_2026-03-16.html").read_text(
            encoding="utf-8"
        )
        scelse_fixture = Path(
            "tests/fixtures/ntu_scelse_all_events_sample_2026-03-16.html"
        ).read_text(encoding="utf-8")

        def fake_fetch(source: object, timeout_seconds: int = 20) -> FetchResult:
            source_id = getattr(source, "id", "")
            fixtures = {
                "rsis_event_rss": (rss_fixture, "application/rss+xml"),
                "nus_osa_events": (osa_fixture, "text/html"),
                "nus_museum": (museum_fixture, "text/html"),
                "ntu_scelse_all_events": (scelse_fixture, "text/html"),
            }
            if source_id in fixtures:
                content, content_type = fixtures[source_id]
                return FetchResult(
                    ok=True,
                    content=content,
                    content_type=content_type,
                    error=None,
                )
            return FetchResult(
                ok=False,
                content=None,
                content_type=None,
                error="fixture not available for source",
            )

        with TemporaryDirectory() as tmp_dir:
            with patch("campus_events.pipeline.fetch_source", side_effect=fake_fetch):
                report = run_pipeline(
                    registry_path="source_registry.yaml",
                    run_date=date(2026, 3, 16),
                    recipient="erichill27@gmail.com",
                    mode="dry-run",
                    output_root=str(Path(tmp_dir) / "runs"),
                    state_root=str(Path(tmp_dir) / "state"),
                )

            self.assertEqual(report.status, "dry_run_valid")
            self.assertEqual(report.candidate_count, 11)
            self.assertEqual(report.filtered_count, 8)
            self.assertEqual(report.deduped_count, 7)
            self.assertIsNotNone(report.digest_path)
            digest_text = Path(report.digest_path).read_text(encoding="utf-8")
            self.assertIn("Microbial Cities Symposium", digest_text)
            self.assertIn("Lab Open House Guided Tour", digest_text)
            self.assertNotIn("Internal Instrument Training", digest_text)

    def test_dry_run_generates_digest_across_all_implemented_parser_families(self) -> None:
        fixture_paths = {
            "nus_coe_rss_directory": ("tests/fixtures/nus_coe_rss_directory_sample_2026-03-16.html", "text/html"),
            "rsis_event_rss": ("tests/fixtures/rsis_event_rss_sample_2026-03-16.xml", "application/rss+xml"),
            "nus_osa_events": ("tests/fixtures/nus_osa_events_sample_2026-03-16.html", "text/html"),
            "nus_museum": ("tests/fixtures/nus_museum_sample_2026-03-16.html", "text/html"),
            "ntu_scelse_all_events": ("tests/fixtures/ntu_scelse_all_events_sample_2026-03-16.html", "text/html"),
            "nus_arts_festival": ("tests/fixtures/nus_arts_festival_sample_2026-03-16.html", "text/html"),
            "nus_baba_house": ("tests/fixtures/nus_baba_house_sample_2026-03-16.html", "text/html"),
            "nus_fass_events": ("tests/fixtures/nus_fass_events_sample_2026-03-16.html", "text/html"),
            "nus_sph_events": ("tests/fixtures/nus_sph_events_sample_2026-03-16.html", "text/html"),
            "nus_math_events": ("tests/fixtures/nus_math_events_sample_2026-03-16.html", "text/html"),
            "nus_cqt_upcoming_events": ("tests/fixtures/nus_cqt_upcoming_events_sample_2026-03-16.html", "text/html"),
            "nus_mbi_seminar_series": ("tests/fixtures/nus_mbi_seminar_series_sample_2026-03-16.html", "text/html"),
            "ntu_main_events": ("tests/fixtures/ntu_main_events_sample_2026-03-16.html", "text/html"),
            "ntu_ias_events": ("tests/fixtures/ntu_event_detail_listing_sample_2026-03-16.html", "text/html"),
            "ntu_mae_events": ("tests/fixtures/ntu_event_detail_listing_sample_2026-03-16.html", "text/html"),
            "ntu_sbs_events": ("tests/fixtures/ntu_event_detail_listing_sample_2026-03-16.html", "text/html"),
            "ntu_cee_events": ("tests/fixtures/ntu_event_detail_listing_sample_2026-03-16.html", "text/html"),
            "ntu_museum_exhibitions": ("tests/fixtures/ntu_museum_exhibitions_sample_2026-03-16.html", "text/html"),
            "ntu_cceb_seminars": ("tests/fixtures/ntu_cceb_seminars_sample_2026-03-16.html", "text/html"),
            "ntu_erian_news_events": ("tests/fixtures/ntu_erian_news_events_sample_2026-03-16.html", "text/html"),
            "https://myaces.nus.edu.sg/CoE/jsp/coeGenRss.jsp?Cat=1": ("tests/fixtures/nus_coe_rss_arts_sample_2026-03-16.xml", "application/rss+xml"),
            "https://myaces.nus.edu.sg/CoE/jsp/coeGenRss.jsp?Cat=2": ("tests/fixtures/nus_coe_rss_seminars_sample_2026-03-16.xml", "application/rss+xml"),
            "https://myaces.nus.edu.sg/CoE/jsp/coeGenRss.jsp?Cat=3": ("tests/fixtures/nus_coe_rss_lectures_sample_2026-03-16.xml", "application/rss+xml"),
        }
        fixture_content = {
            key: (Path(path).read_text(encoding="utf-8"), content_type)
            for key, (path, content_type) in fixture_paths.items()
        }

        def fake_fetch(source: object, timeout_seconds: int = 20) -> FetchResult:
            source_id = getattr(source, "id", "")
            source_url = getattr(source, "url", "")
            key = source_id if source_id in fixture_content else source_url
            if key in fixture_content:
                content, content_type = fixture_content[key]
                return FetchResult(
                    ok=True,
                    content=content,
                    content_type=content_type,
                    error=None,
                )
            return FetchResult(
                ok=False,
                content=None,
                content_type=None,
                error="fixture not available for source",
            )

        with TemporaryDirectory() as tmp_dir:
            with patch("campus_events.pipeline.fetch_source", side_effect=fake_fetch):
                report = run_pipeline(
                    registry_path="source_registry.yaml",
                    run_date=date(2026, 3, 16),
                    recipient="erichill27@gmail.com",
                    mode="dry-run",
                    output_root=str(Path(tmp_dir) / "runs"),
                    state_root=str(Path(tmp_dir) / "state"),
                )

            self.assertEqual(report.status, "dry_run_valid")
            self.assertGreaterEqual(report.candidate_count, 25)
            self.assertGreaterEqual(report.filtered_count, 21)
            self.assertGreaterEqual(report.deduped_count, 18)
            self.assertIsNotNone(report.digest_path)
            digest_text = Path(report.digest_path).read_text(encoding="utf-8")
            self.assertIn("Energy Resilience Dialogue", digest_text)
            self.assertIn("NTU Innovation Day", digest_text)
            self.assertIn("Quantum Sensing Workshop", digest_text)
            self.assertIn("Campus Arts Festival Night", digest_text)
            self.assertIn("Campus Chamber Concert", digest_text)
