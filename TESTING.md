# Testing

## Testing Philosophy

Every implementation phase must end with a runnable verification step before the next phase begins.

This file owns test process and verification standards. It should not duplicate source inventory from [SOURCES.md](/Users/scelsenus/Desktop/CampusEvents/SOURCES.md) or implementation sequencing from [IMPLEMENTATION_PLAN.md](/Users/scelsenus/Desktop/CampusEvents/IMPLEMENTATION_PLAN.md).

Primary goals:

- catch parser breakage early
- keep source-specific logic isolated
- avoid dependence on live websites during routine development
- make regressions easy to diagnose

## Default Test Stack

- test runner: `pytest`
- assertion style: native `pytest` asserts
- fixtures: saved RSS, ICS, and HTML samples under `tests/fixtures/`
- optional helpers: `pytest-mock`, `freezegun`, and snapshot-style string assertions if needed

Recommended local invocation:

- create or reuse the workspace virtualenv at `.venv`
- run tests with `./.venv/bin/pytest`

## Phase-Based Test Gates

### Phase 1: Documentation and Scaffolding

Verification:

- manual review of docs

### Phase 2: Source Discovery and Parsing

Verification:

- parser smoke tests over saved fixtures
- one test file per parser family where practical

Examples:

- RSS feeds produce at least one event candidate
- HTML parsers extract title, date, and URL from representative pages
- unsupported pages fail clearly rather than silently

### Phase 3: Normalization

Verification:

- unit tests for date normalization
- unit tests for campus and organiser mapping
- unit tests for missing-field handling

### Phase 4: Filtering

Verification:

- items that look like classes are excluded
- seminars, lectures, sports, talks, performances, concerts, plays, exhibitions, and art displays are retained when public-facing
- stale items are removed based on the run date

### Phase 5: Deduplication

Verification:

- overlapping events collapse into one canonical event
- clearly distinct events are not merged
- richer metadata survives merge resolution

### Phase 6: Rendering

Verification:

- digest output is deterministic for a fixed run date
- items render in the expected order
- empty sections are handled gracefully

### Phase 7: Email Delivery

Verification:

- transport is mocked
- subject and payload are asserted
- failures raise clear errors and are logged

### Phase 8: Automation

Verification:

- manual dry run succeeds
- one scheduled smoke test if the platform supports it

## Fixture Policy

- Save representative samples for each source family.
- Name fixtures clearly by source and date.
- Keep raw fixtures close to the original response body.
- Prefer multiple small fixtures over one giant archive.
- Add a fixture whenever a source-specific bug is fixed.

Important:

- include fixtures for campus-based institutes and agencies such as SCELSE-like sources, not only central university pages

## Recommended Test Categories

### Parser Tests

Assert extraction correctness from raw source content.

### Model Tests

Assert canonical event validation and normalization.

### Filter Tests

Assert inclusion and exclusion policy.

### Dedupe Tests

Assert merge behavior across overlapping sources.

### Render Tests

Assert final digest formatting and ordering.

### Integration-Smoke Tests

Run a local end-to-end flow over fixtures without network access.

## What Not To Test Live By Default

- live RSS availability
- current HTML structure of every source
- actual email sending
- real scheduler execution

Those are operational checks, not the core regression suite.

## Minimum Bar Before Advancing A Phase

- all relevant `pytest` tests pass
- new source adapters have fixture coverage
- affected docs are updated
- any unresolved gaps are logged in [PROGRESS.md](/Users/scelsenus/Desktop/CampusEvents/PROGRESS.md)
