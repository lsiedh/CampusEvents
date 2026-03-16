import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

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
