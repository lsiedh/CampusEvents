from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


EXPECTED_INITIAL_RECIPIENT = "erichill27@gmail.com"
SINGAPORE_TIMEZONE = "Asia/Singapore"


@dataclass(slots=True)
class DeliveryConfig:
    smtp_host: str | None
    smtp_port: int
    smtp_username: str | None
    smtp_password: str | None
    smtp_from: str | None
    smtp_starttls: bool

    @property
    def configured(self) -> bool:
        return all(
            [
                self.smtp_host,
                self.smtp_username,
                self.smtp_password,
                self.smtp_from,
            ]
        )

    def missing_fields(self) -> list[str]:
        missing: list[str] = []
        if not self.smtp_host:
            missing.append("CAMPUS_EVENTS_SMTP_HOST")
        if not self.smtp_username:
            missing.append("CAMPUS_EVENTS_SMTP_USERNAME")
        if not self.smtp_password:
            missing.append("CAMPUS_EVENTS_SMTP_PASSWORD")
        if not self.smtp_from:
            missing.append("CAMPUS_EVENTS_SMTP_FROM")
        return missing


def load_delivery_config() -> DeliveryConfig:
    return DeliveryConfig(
        smtp_host=os.getenv("CAMPUS_EVENTS_SMTP_HOST"),
        smtp_port=int(os.getenv("CAMPUS_EVENTS_SMTP_PORT", "587")),
        smtp_username=os.getenv("CAMPUS_EVENTS_SMTP_USERNAME"),
        smtp_password=os.getenv("CAMPUS_EVENTS_SMTP_PASSWORD"),
        smtp_from=os.getenv("CAMPUS_EVENTS_SMTP_FROM"),
        smtp_starttls=os.getenv("CAMPUS_EVENTS_SMTP_STARTTLS", "true").lower()
        not in {"0", "false", "no"},
    )


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

