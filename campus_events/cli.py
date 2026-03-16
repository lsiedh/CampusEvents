from __future__ import annotations

import argparse
import sys
from datetime import date

from campus_events.config import EXPECTED_INITIAL_RECIPIENT, load_local_env
from campus_events.pipeline import default_run_date, report_to_console_text, run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Campus events digest pipeline")
    parser.add_argument(
        "--registry",
        default="source_registry.yaml",
        help="Path to the source registry file",
    )
    parser.add_argument(
        "--recipient",
        default=EXPECTED_INITIAL_RECIPIENT,
        help="Target recipient for the digest",
    )
    parser.add_argument(
        "--run-date",
        type=date.fromisoformat,
        default=default_run_date(),
        help="Run date in YYYY-MM-DD (defaults to Singapore current date)",
    )
    parser.add_argument(
        "--deliver",
        action="store_true",
        help="Attempt SMTP delivery after validation",
    )
    parser.add_argument(
        "--output-root",
        default="runs",
        help="Directory for digest artifacts",
    )
    parser.add_argument(
        "--state-root",
        default=".state",
        help="Directory for duplicate-suppression state",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=20,
        help="HTTP fetch timeout for each source",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    load_local_env()
    parser = build_parser()
    args = parser.parse_args(argv)
    mode = "deliver" if args.deliver else "dry-run"
    report = run_pipeline(
        registry_path=args.registry,
        run_date=args.run_date,
        recipient=args.recipient,
        mode=mode,
        output_root=args.output_root,
        state_root=args.state_root,
        timeout_seconds=args.timeout_seconds,
    )
    print(report_to_console_text(report))
    if report.status in {"blocked_validation", "blocked_delivery"}:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
