# Architecture

## System Goal

Generate a weekday 7:00 AM Singapore-time email digest of public-facing NTU and NUS campus events, including relevant events from campus-based institutes and partner organisations hosted on those campuses.

This file owns the technical design. It should not duplicate milestone tracking from [PROGRESS.md](/Users/scelsenus/Desktop/CampusEvents/PROGRESS.md) or testing process details from [TESTING.md](/Users/scelsenus/Desktop/CampusEvents/TESTING.md).

## Design Principles

- Prefer official sources over aggregators.
- Prefer machine-readable feeds over HTML scraping.
- Keep each source adapter isolated.
- Make every stage testable without live network access.
- Preserve source provenance on every event.
- Treat campus-based institutes and agencies as first-class sources, not edge cases.

## Pipeline

### 1. Source Registry

Maintain a registry of source definitions. Each source record should include:

- source name
- institution or host campus
- governance type: university, hosted institute, partner institute, national centre, or other
- source kind: RSS, Atom, ICS, HTML, API
- parser adapter name
- expected event categories
- trust level
- active or inactive flag

The registry should cover:

- NUS university and faculty sources
- NTU university and school sources
- campus-based institutes such as SCELSE, NERI, CQT, SMART, ERI@N, and similar organisations discovered later

### 2. Fetch Layer

Fetch raw content from the registered sources.

Responsibilities:

- retrieve feed or page content
- apply timeouts and retry policy
- record fetch metadata
- hand raw content to the matching parser

This layer should be thin. It should not contain business rules.

### 3. Parser Adapters

Each source type or site family gets a dedicated adapter.

Examples:

- generic RSS parser
- generic ICS parser
- NUS portal HTML parser
- NTU portal HTML parser
- independent institute HTML parser

Responsibilities:

- extract event candidates
- map raw fields into a preliminary event object
- preserve original source URL and any unique identifiers

### 4. Normalization Layer

Convert parsed candidates into a canonical event model.

Canonical fields should include:

- title
- summary
- start datetime
- end datetime
- timezone
- venue
- campus
- institution
- organiser
- source name
- source URL
- category
- audience hint
- tags

This layer should also normalize:

- date and time formatting
- campus naming
- duplicate whitespace and markup noise
- category labels across inconsistent source taxonomies

Core event categories should include:

- lectures
- seminars
- talks
- conferences
- sports events
- theatre and play performances
- concerts and musical performances
- exhibitions and art displays

### 5. Filtering Layer

Remove items that do not belong in the digest.

Primary exclusions:

- classes and course sessions
- closed internal meetings
- student timetable items
- events outside the current digest window
- undated events
- non-event announcements

Special handling:

- some campus-based institutes may publish both research seminars and internal notices; filters must distinguish the two

Current digest window:

- include events whose Singapore-local start date is the run date through seven days after the run date, inclusive
- exclude events with no start datetime because they cannot be placed safely into the delivery window

### 6. Deduplication Layer

Merge repeated events across overlapping sources.

Common overlap cases:

- a faculty page and a central university page list the same talk
- a hosted institute and a university portal both list the same symposium
- a performance venue or arts page and a central campus events portal list the same concert or exhibition
- one source publishes a richer description while another has cleaner dates

Deduplication should favor:

- best title quality
- most precise datetime
- most direct source URL
- richest venue and organiser metadata

### 7. Ranking And Selection

Order events for digest presentation.

Suggested ranking factors:

- event date proximity
- campus
- event significance
- confidence in parsing quality
- public relevance

### 8. Rendering Layer

Render the final digest as markdown plus email-ready plain text and HTML content.

Digest sections should likely include:

- today at NTU
- today at NUS
- upcoming later this week
- notable campus-institute events

Each item should show:

- title
- date and time
- venue
- organiser
- brief summary
- original link

Current rendering behavior:

- persist the digest artifact as markdown under `runs/<run-date>/digest.md`
- send email as multipart alternative with plain text fallback and rendered HTML body
- display event times in Singapore time using `MM/DD/YY HH:MM` 24-hour formatting

### 9. Delivery Layer

Send the digest through an email transport.

Requirements:

- environment-driven configuration
- allow local development configuration from untracked `.env.local` or `.env` files without overriding already-exported environment variables
- support a configured recipient list, with the initial digest recipient set to `erichill27@gmail.com`
- dry-run mode
- failure logging
- deterministic subject line for the run date
- HTML-capable delivery so email clients do not receive raw markdown

### 10. Automation Layer

The automation should:

- run every weekday at 7:00 AM Singapore time
- execute a dry-run-capable command
- emit logs for source failures
- avoid sending duplicate digests for the same run date

Operational state for automation safety should include:

- a persisted delivery ledger keyed by run date, recipient, and deterministic subject
- per-run artifact output such as the rendered digest and machine-readable summary report

## Suggested Package Layout

```text
campus_events/
  config.py
  models.py
  registry.py
  fetchers/
  parsers/
  filters/
  dedupe/
  render/
  delivery/
  cli.py
tests/
  fixtures/
  parsers/
  filters/
  dedupe/
  render/
```

## Source Strategy Note

Do not limit discovery to pages under `nus.edu.sg` or `ntu.edu.sg`.

Also include:

- hosted research centres of excellence
- CREATE or cross-institution research entities on campus
- partner institutes with their own domains
- national or corporate labs physically based on campus

These sources should be explicit in the registry so they can be maintained independently from faculty and department sites.
