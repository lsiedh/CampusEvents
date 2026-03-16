import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from campus_events.config import load_local_env


class ConfigTests(unittest.TestCase):
    def test_load_local_env_populates_missing_values_from_env_local(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            env_path = Path(tmp_dir) / ".env.local"
            env_path.write_text(
                "\n".join(
                    [
                        "CAMPUS_EVENTS_SMTP_HOST=smtp.gmail.com",
                        "CAMPUS_EVENTS_SMTP_USERNAME=erichill27@gmail.com",
                    ]
                ),
                encoding="utf-8",
            )
            with patch.dict(os.environ, {}, clear=True):
                load_local_env(tmp_dir)
                self.assertEqual(os.environ["CAMPUS_EVENTS_SMTP_HOST"], "smtp.gmail.com")
                self.assertEqual(
                    os.environ["CAMPUS_EVENTS_SMTP_USERNAME"], "erichill27@gmail.com"
                )

    def test_load_local_env_does_not_override_existing_values(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            env_path = Path(tmp_dir) / ".env.local"
            env_path.write_text("CAMPUS_EVENTS_SMTP_HOST=smtp.gmail.com\n", encoding="utf-8")
            with patch.dict(
                os.environ, {"CAMPUS_EVENTS_SMTP_HOST": "smtp.example.com"}, clear=True
            ):
                load_local_env(tmp_dir)
                self.assertEqual(os.environ["CAMPUS_EVENTS_SMTP_HOST"], "smtp.example.com")
