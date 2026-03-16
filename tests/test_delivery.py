import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from campus_events.config import DeliveryConfig
from campus_events.delivery import DeliveryLedger, validate_recipient


class DeliveryTests(unittest.TestCase):
    def test_validate_recipient_requires_expected_address(self) -> None:
        errors = validate_recipient("someone@example.com", "erichill27@gmail.com")
        self.assertTrue(errors)
        self.assertIn("configured initial recipient", errors[0])

    def test_delivery_ledger_detects_duplicate(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            ledger = DeliveryLedger(Path(tmp_dir) / "ledger.json")
            self.assertFalse(
                ledger.has_delivery("2026-03-16", "erichill27@gmail.com", "subject")
            )
            ledger.record_delivery("2026-03-16", "erichill27@gmail.com", "subject")
            self.assertTrue(
                ledger.has_delivery("2026-03-16", "erichill27@gmail.com", "subject")
            )

    def test_send_via_smtp_adds_html_alternative(self) -> None:
        from campus_events.delivery import send_via_smtp

        config = DeliveryConfig(
            smtp_host="smtp.gmail.com",
            smtp_port=587,
            smtp_username="erichill27@gmail.com",
            smtp_password="secret",
            smtp_from="erichill27@gmail.com",
            smtp_starttls=True,
        )

        with patch("campus_events.delivery.smtplib.SMTP") as smtp_cls:
            send_via_smtp(
                config,
                "erichill27@gmail.com",
                "Campus Events Digest for 2026-03-16",
                "Plain text body",
                html_body="<html><body><h1>Campus Events Digest</h1></body></html>",
            )

        smtp = smtp_cls.return_value.__enter__.return_value
        smtp.starttls.assert_called_once()
        smtp.login.assert_called_once_with("erichill27@gmail.com", "secret")
        message = smtp.send_message.call_args.args[0]
        self.assertEqual(message.get_content_type(), "multipart/alternative")
        payloads = message.get_payload()
        self.assertEqual(payloads[0].get_content_type(), "text/plain")
        self.assertEqual(payloads[1].get_content_type(), "text/html")
