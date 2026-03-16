# Project Agent Notes

This file defines documentation ownership so the markdown files stay in their lanes.

## File Ownership

- `README.md`: project purpose, scope, and doc index only
- `IMPLEMENTATION_PLAN.md`: ordered work phases and delivery checkpoints
- `ARCHITECTURE.md`: system design, package structure, and pipeline boundaries
- `TESTING.md`: test policy, fixture policy, and verification gates
- `SOURCES.md`: source inventory, source classification, and source-specific notes
- `PROGRESS.md`: current status, dated decisions, open questions, and next step
- `AGENTS.md`: documentation maintenance rules only

## Update Rules

- Do not copy the same instructions across multiple markdown files.
- When a fact already belongs to another file, link to that file instead of repeating the content.
- Add source discoveries only to `SOURCES.md`.
- Add schedule or milestone changes only to `IMPLEMENTATION_PLAN.md` or `PROGRESS.md`, depending on whether the change is planned or completed.
- Add architectural changes only to `ARCHITECTURE.md`.
- Add test-process changes only to `TESTING.md`.
- Keep `README.md` concise and stable unless scope or top-level success criteria change.

## Cross-Reference Rule

- Prefer short references such as "see `TESTING.md`" instead of restating detailed instructions.
