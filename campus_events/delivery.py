from __future__ import annotations

import json
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path

from campus_events.config import DeliveryConfig, ensure_directory


@dataclass(slots=True)
class DeliveryLedger:
    path: Path

    def _load(self) -> dict[str, list[dict[str, str]]]:
        if not self.path.exists():
            return {"deliveries": []}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def has_delivery(self, run_date: str, recipient: str, subject: str) -> bool:
        payload = self._load()
        for entry in payload.get("deliveries", []):
            if (
                entry.get("run_date") == run_date
                and entry.get("recipient") == recipient
                and entry.get("subject") == subject
            ):
                return True
        return False

    def record_delivery(self, run_date: str, recipient: str, subject: str) -> None:
        payload = self._load()
        payload.setdefault("deliveries", []).append(
            {"run_date": run_date, "recipient": recipient, "subject": subject}
        )
        ensure_directory(self.path.parent)
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def validate_recipient(recipient: str, expected: str) -> list[str]:
    if recipient != expected:
        return [
            f"recipient {recipient} is not the configured initial recipient {expected}"
        ]
    return []


def send_via_smtp(
    config: DeliveryConfig,
    recipient: str,
    subject: str,
    body: str,
) -> None:
    if not config.configured:
        missing = ", ".join(config.missing_fields())
        raise ValueError(f"smtp delivery is not configured; missing {missing}")

    message = EmailMessage()
    message["From"] = config.smtp_from
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=30) as smtp:
        if config.smtp_starttls:
            smtp.starttls()
        smtp.login(config.smtp_username, config.smtp_password)
        smtp.send_message(message)

