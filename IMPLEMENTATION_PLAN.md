# Implementation Plan

## Goal

Deliver a reliable weekday morning email digest for public-facing NTU and NUS campus events.

This file owns the ordered implementation phases only. Detailed architecture belongs in [ARCHITECTURE.md](/Users/scelsenus/Desktop/CampusEvents/ARCHITECTURE.md), and detailed testing policy belongs in [TESTING.md](/Users/scelsenus/Desktop/CampusEvents/TESTING.md).

## Phase Plan

### Phase 1: Scaffolding

- Create project documentation
- Choose stack and testing approach
- Capture known sources

Verification:

- Manual doc review

### Phase 2: Source Discovery and Validation

- Probe each seed and candidate source
- Classify source type: RSS, ICS, HTML, or unsupported
- Identify additional official event sources not already listed
- Store representative fixtures for parsers

Verification:

- `pytest` parser smoke tests over fixtures

### Phase 3: Data Model

- Define event schema
- Implement normalization helpers
- Normalize dates, campus, category, and links

Verification:

- `pytest` unit tests for schema and normalized outputs

### Phase 4: Filtering

- Exclude classes and student-only timetable-like items
- Score public relevance
- Remove stale events

Verification:

- `pytest` unit tests for filtering rules

### Phase 5: Deduplication

- Merge repeated events across portals
- Keep best canonical source link

Verification:

- `pytest` dedupe tests with overlapping fixtures

### Phase 6: Digest Rendering

- Sort events by date and campus
- Produce email-ready markdown or HTML

Verification:

- `pytest` rendering tests

### Phase 7: Delivery

- Add configuration and secret handling
- Implement email send path
- Configure the initial digest recipient as `erichill27@gmail.com`
- Add dry-run mode

Verification:

- `pytest` mocked delivery tests

### Phase 8: Scheduling

- Connect to weekday 7:00 AM automation
- Confirm idempotent daily execution

Verification:

- Manual smoke run
- One scheduled run verification if supported

## Notes for Future Work

- If a source exposes calendars or APIs behind landing pages, prefer the underlying machine-readable endpoint.
- If HTML pages are unstable, keep parser selectors narrowly scoped and backed by fixtures.
- Source discovery should continue throughout the project; record actual source findings in [SOURCES.md](/Users/scelsenus/Desktop/CampusEvents/SOURCES.md).
