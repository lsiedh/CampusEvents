# Progress

This file tracks project state and decisions only. It should not become a duplicate source inventory or architecture document.

## Current Status

Phase: 1 - Repository scaffolding

Status:

- project scope documented
- default implementation language chosen: Python
- default test framework chosen: `pytest`
- initial source inventory captured from the seed file
- first source validation pass completed for seed feeds, central portals, arts pages, museums, and major institute sources
- machine-readable source registry created from the validated set
- fixture capture plan created for initial parser work
- repository operating rules documented
- minimal Python pipeline scaffold implemented with registry loading, fetch, parse dispatch, filtering, dedupe, rendering, SMTP-gated delivery, and duplicate-suppression ledger
- local dry-run command implemented and exercised against the validated registry, with per-source failure logging and artifact output under `runs/`
- workspace virtualenv created at `.venv`, `pytest` installed there, and local verification now runs through `./.venv/bin/pytest`
- first fixture-backed parser coverage added for the `generic_rss` family using a representative saved RSS sample and an offline dry-run integration test
- first dedicated HTML parser family added for `nus_osa_events`, including a representative saved fixture and offline dry-run coverage alongside RSS
- reusable `museum_cards` parser family added with representative fixture coverage and offline dry-run coverage across RSS, OSA, and museum sources
- reusable `filtered_event_cards` parser family added for SCELSE-style institute listings, with representative fixture coverage and offline dry-run coverage across NTU and NUS sources
- remaining validated HTML parser families now have representative saved fixtures and parser coverage, with an aggregate offline dry-run test spanning the implemented parser set
- `nus_coe_rss_directory` now expands downstream RSS feeds in the pipeline, with representative directory and feed fixtures plus offline coverage for the expansion path

## Milestones

| Phase | Name | Status | Exit Criteria |
| --- | --- | --- | --- |
| 1 | Scaffolding | Completed | Core markdown files exist and reflect current understanding |
| 2 | Source inventory | In progress | High-confidence source list with parse strategy per source |
| 3 | Normalization model | Not started | Unified event schema and parser outputs established |
| 4 | Filtering and dedupe | Not started | Non-class filters and duplicate handling covered by tests |
| 5 | Digest rendering | Not started | Deterministic digest output produced from normalized events |
| 6 | Email delivery | Not started | Send path configured and tested with mocks |
| 7 | Automation scheduling | Not started | Weekday 7:00 AM run configured |
| 8 | Hardening | Not started | Logging, docs, and regression checks complete |

## Decisions Log

### 2026-03-16

- Decided to start with Python for ingestion and normalization speed.
- Decided to require a test gate after each implementation phase.
- Decided to maintain a dedicated `SOURCES.md` file from the start.
- Decided to keep documentation live and revise it as discovery work proceeds.
- Decided that source discovery must include campus-hosted institutes and agencies beyond the university departmental structure.
- Decided that the event scope includes public performances, concerts, plays, exhibitions, art displays, and sporting events.
- Decided to distinguish between direct ingestion sources, discovery-only pages, and rejected sources during validation.
- Decided to maintain a machine-readable validated source registry separately from the broader source inventory.
- Decided that the initial digest recipient should be `erichill27@gmail.com`.
- Decided that automation-safe runs should always write a summary artifact and use a persisted delivery ledger before SMTP delivery.
- Decided that the default local test command for this workspace is `./.venv/bin/pytest`.

## Open Questions

- Which email transport is most practical for the final delivery path?
- Which NUS and NTU sources expose machine-readable feeds versus HTML-only pages?
- Which event categories require custom exclusion rules to avoid class-like listings?
- Which sources are public enough to rely on without authentication?
- Which campus-based non-department organisations have stable event pages worth ingesting?
- Which HTML source families need dedicated selectors beyond structured-data extraction?

## Next Step

Capture raw Phase 1 fixtures from the validated registry to replace the representative samples, then decide whether the expanded NUS CoE downstream feeds should remain dynamic or be promoted into explicit registry records for clearer per-feed control.
