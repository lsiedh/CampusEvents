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
- live-source fetch handling now includes the NTU events JSON endpoint and the SCELSE WordPress AJAX endpoint, so those two sources no longer depend on brittle placeholder HTML fixtures
- live dry-run execution has been re-verified against the registry; Incapsula-blocked NUS pages are now logged explicitly as challenge-page failures rather than generic parser misses
- timezone-aware event timestamps from live feeds exposed and fixed a dedupe sort bug caused by mixing aware event datetimes with a naive fallback sentinel
- captured live NTU response snapshots are now stored under `tests/fixtures/` and covered by parser regression tests
- additional NTU sources now use their native `GetEvents` feeds or live `img-card` listings, bringing IAS, MAE, CCEB, ERI@N, and NTU Museum into the successful live parse set
- the validated registry now disables the two NTU sources whose canonical URLs return HTTP 404, and it disables the currently Incapsula-blocked NUS HTML sources so recurring automation runs only against fetchable sources
- the SBS and CEE NTU sources have now been corrected to working replacement URLs and re-enabled in the validated registry
- direct checks against likely alternate machine-readable paths for the remaining inactive NUS HTML sources did not yield a fetchable replacement; the blocker remains upstream Incapsula access rather than parser coverage
- the delivery path now sends rendered HTML email with plain-text fallback instead of raw markdown
- rendered `When` values now display in Singapore-local `MM/DD/YY HH:MM` format
- filtering now limits the digest to events from the run date through seven days later, inclusive, using Singapore-local dates and excluding undated events
- the CLI now auto-loads SMTP configuration from untracked `.env.local` or `.env` files for local delivery runs
- dry-run validation for `2026-03-17` succeeded against the current live safe source set and produced a digest with 12 deduped events in the one-week window
- a tracked SMTP password placeholder mistake in `.env.example` was corrected and the leaked value was removed from GitHub history

## Milestones

| Phase | Name | Status | Exit Criteria |
| --- | --- | --- | --- |
| 1 | Scaffolding | Completed | Core markdown files exist and reflect current understanding |
| 2 | Source inventory | In progress | High-confidence source list with parse strategy per source |
| 3 | Normalization model | In progress | Unified event schema and parser outputs established |
| 4 | Filtering and dedupe | In progress | Non-class filters and duplicate handling covered by tests |
| 5 | Digest rendering | Completed | Deterministic digest output produced from normalized events |
| 6 | Email delivery | In progress | Send path configured, HTML email supported, and local SMTP delivery validated |
| 7 | Automation scheduling | Not started | Weekday 7:00 AM run configured |
| 8 | Hardening | In progress | Logging, docs, and regression checks complete |

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
- Decided to use source-specific live fetch paths when a registry source is JS-backed but still exposes a stable machine-readable endpoint, rather than scraping the shell page.
- Decided to reduce the active NUS source set for automation until a documented alternate public feed exists for the Incapsula-blocked HTML pages.
- Decided that digest delivery should use rendered HTML email with plain-text fallback while still saving markdown artifacts under `runs/`.
- Decided that the delivery digest window should include only events from the run date through the next seven days, inclusive, based on Singapore-local dates.
- Decided that local SMTP configuration should be loadable from untracked `.env.local` or `.env` files.

## Open Questions

- Which event categories require custom exclusion rules to avoid class-like listings?
- Which sources are public enough to rely on without authentication?
- Which campus-based non-department organisations have stable event pages worth ingesting?
- Which remaining NTU HTML source families need dedicated live selectors beyond the representative fixture layouts?

## Next Step

Commit and push the current local code changes that added `.env.local` loading, then configure the weekday 7:00 AM Singapore automation to run with the current automation-safe source set.
