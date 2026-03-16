from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from campus_events.config import (
    EXPECTED_INITIAL_RECIPIENT,
    SINGAPORE_TIMEZONE,
    ensure_directory,
    load_delivery_config,
)
from campus_events.dedupe import dedupe_events
from campus_events.delivery import DeliveryLedger, send_via_smtp, validate_recipient
from campus_events.fetchers import fetch_source
from campus_events.filters import filter_events
from campus_events.models import Event, RunReport, SourceAttempt
from campus_events.parsers import ParseError, parse_source
from campus_events.parsers import parse_nus_coe_rss_directory
from campus_events.registry import load_registry
from campus_events.render import digest_subject, render_digest


def default_run_date() -> date:
    return datetime.now(ZoneInfo(SINGAPORE_TIMEZONE)).date()


def run_pipeline(
    *,
    registry_path: str,
    run_date: date,
    recipient: str,
    mode: str,
    output_root: str,
    state_root: str,
    timeout_seconds: int = 20,
) -> RunReport:
    sources = [source for source in load_registry(registry_path) if source.active]
    attempts: list[SourceAttempt] = []
    filtered_events: list[Event] = []
    candidate_count = 0

    for source in sources:
        attempt = SourceAttempt(
            source_id=source.id,
            source_url=source.url,
            parser_family=source.parser_family,
        )
        attempts.append(attempt)

        fetch_result = fetch_source(source, timeout_seconds=timeout_seconds)
        if not fetch_result.ok or fetch_result.content is None:
            attempt.fetch_error = fetch_result.error or "unknown fetch error"
            continue
        attempt.fetch_ok = True

        if source.parser_family == "nus_coe_rss_directory":
            try:
                expanded_sources = parse_nus_coe_rss_directory(source, fetch_result.content)
            except ParseError as exc:
                attempt.parse_error = str(exc)
                continue
            attempt.parse_ok = True
            attempt.candidate_count = len(expanded_sources)

            for child_source in expanded_sources:
                child_attempt = SourceAttempt(
                    source_id=child_source.id,
                    source_url=child_source.url,
                    parser_family=child_source.parser_family,
                )
                attempts.append(child_attempt)
                child_fetch = fetch_source(child_source, timeout_seconds=timeout_seconds)
                if not child_fetch.ok or child_fetch.content is None:
                    child_attempt.fetch_error = child_fetch.error or "unknown fetch error"
                    continue
                child_attempt.fetch_ok = True
                try:
                    parsed_events = parse_source(child_source, child_fetch.content)
                except ParseError as exc:
                    child_attempt.parse_error = str(exc)
                    continue

                child_attempt.parse_ok = True
                child_attempt.candidate_count = len(parsed_events)
                candidate_count += len(parsed_events)
                kept_events = filter_events(parsed_events, run_date)
                child_attempt.kept_count = len(kept_events)
                filtered_events.extend(kept_events)
            continue

        try:
            parsed_events = parse_source(source, fetch_result.content)
        except ParseError as exc:
            attempt.parse_error = str(exc)
            continue

        attempt.parse_ok = True
        attempt.candidate_count = len(parsed_events)
        candidate_count += len(parsed_events)

        kept_events = filter_events(parsed_events, run_date)
        attempt.kept_count = len(kept_events)
        filtered_events.extend(kept_events)

    deduped_events = dedupe_events(filtered_events)
    subject = digest_subject(run_date)
    ledger = DeliveryLedger(Path(state_root) / "delivery_ledger.json")
    duplicate_detected = ledger.has_delivery(run_date.isoformat(), recipient, subject)

    validation_errors = validate_recipient(recipient, EXPECTED_INITIAL_RECIPIENT)
    if not deduped_events:
        validation_errors.append("no events remain after fetch, parse, filter, and dedupe")

    output_dir = ensure_directory(Path(output_root) / run_date.isoformat())
    digest_path: Path | None = None
    digest_body = ""
    if deduped_events:
        digest_body = render_digest(deduped_events, run_date)
        digest_path = output_dir / "digest.md"
        digest_path.write_text(digest_body, encoding="utf-8")

    summary_path = output_dir / "summary.json"
    delivery_error: str | None = None
    digest_delivered = False

    if validation_errors:
        status = "blocked_validation"
    elif duplicate_detected:
        status = "skipped_duplicate"
    elif mode == "dry-run":
        status = "dry_run_valid"
    else:
        try:
            send_via_smtp(load_delivery_config(), recipient, subject, digest_body)
        except Exception as exc:
            delivery_error = str(exc)
            status = "blocked_delivery"
        else:
            digest_delivered = True
            ledger.record_delivery(run_date.isoformat(), recipient, subject)
            status = "delivered"

    report = RunReport(
        run_date=run_date.isoformat(),
        mode=mode,
        recipient=recipient,
        expected_recipient=EXPECTED_INITIAL_RECIPIENT,
        recipient_valid=not validate_recipient(recipient, EXPECTED_INITIAL_RECIPIENT),
        duplicate_detected=duplicate_detected,
        digest_generated=bool(digest_path),
        digest_delivered=digest_delivered,
        status=status,
        subject=subject,
        validation_errors=validation_errors,
        source_attempts=attempts,
        candidate_count=candidate_count,
        filtered_count=len(filtered_events),
        deduped_count=len(deduped_events),
        summary_path=str(summary_path),
        digest_path=str(digest_path) if digest_path else None,
        delivery_error=delivery_error,
    )
    summary_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    return report


def report_to_console_text(report: RunReport) -> str:
    lines = [
        f"status: {report.status}",
        f"run_date: {report.run_date}",
        f"mode: {report.mode}",
        f"recipient: {report.recipient}",
        f"expected_recipient: {report.expected_recipient}",
        f"recipient_valid: {str(report.recipient_valid).lower()}",
        f"duplicate_detected: {str(report.duplicate_detected).lower()}",
        f"digest_generated: {str(report.digest_generated).lower()}",
        f"digest_delivered: {str(report.digest_delivered).lower()}",
        f"candidate_count: {report.candidate_count}",
        f"filtered_count: {report.filtered_count}",
        f"deduped_count: {report.deduped_count}",
        f"summary_path: {report.summary_path}",
    ]
    if report.digest_path:
        lines.append(f"digest_path: {report.digest_path}")
    if report.validation_errors:
        lines.append("validation_errors:")
        lines.extend(f"  - {error}" for error in report.validation_errors)
    if report.delivery_error:
        lines.append(f"delivery_error: {report.delivery_error}")

    lines.append("source_results:")
    for attempt in report.source_attempts:
        fetch_status = "ok" if attempt.fetch_ok else f"failed ({attempt.fetch_error})"
        if attempt.parse_ok:
            parse_status = "ok"
        elif not attempt.fetch_ok:
            parse_status = "skipped (fetch failed)"
        else:
            parse_status = f"failed ({attempt.parse_error})"
        lines.append(
            "  - "
            f"{attempt.source_id}: fetch={fetch_status}; parse={parse_status}; "
            f"candidates={attempt.candidate_count}; kept={attempt.kept_count}"
        )
    return "\n".join(lines)
