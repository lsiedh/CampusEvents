# Campus Events Automation

This repository will produce a weekday 7:00 AM email digest of public-facing campus events at NUS and NTU in Singapore.

## Scope

The digest should include:

- lectures
- seminars
- conferences
- talks and speaking events
- sports and recreation events
- theatre and play performances
- musical performances and concerts
- exhibitions, art displays, and gallery events
- community events when they are campus-based and publicly relevant

The digest should exclude:

- classes and course sessions intended for enrolled students
- private/internal administrative meetings
- obviously stale or duplicate listings

## Project Map

- [IMPLEMENTATION_PLAN.md](/Users/scelsenus/Desktop/CampusEvents/IMPLEMENTATION_PLAN.md): delivery phases and checkpoints
- [ARCHITECTURE.md](/Users/scelsenus/Desktop/CampusEvents/ARCHITECTURE.md): technical design and pipeline boundaries
- [TESTING.md](/Users/scelsenus/Desktop/CampusEvents/TESTING.md): test strategy and phase gates
- [SOURCES.md](/Users/scelsenus/Desktop/CampusEvents/SOURCES.md): source inventory and source-specific notes
- [PROGRESS.md](/Users/scelsenus/Desktop/CampusEvents/PROGRESS.md): current status, decisions, and next step
- [AGENTS.md](/Users/scelsenus/Desktop/CampusEvents/AGENTS.md): documentation ownership rules for future updates

## Success Criteria

- Pulls events from validated NTU and NUS sources
- Includes more than the seed RSS list when useful sources are found
- Produces a readable digest for a target date
- Sends on weekdays at 7:00 AM Singapore time
- Has `pytest` coverage for parser, filter, dedupe, and render logic
- Keeps the project docs current in their assigned lanes
