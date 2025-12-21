---
title: Architecture Decision Records (ADR)
date_created: 2025-12-16
owner: Personal Blog Project Team
---

# Architecture Decisions

This document records significant architectural decisions for the Personal Blog project.

## ADR-001: Filesystem-based Persistence

- **Status**: Accepted
- **Context**: The project is a small personal blog. Using a full RDBMS (PostgreSQL/MySQL) requires infrastructure management. SQLite is simpler but still requires database migrations and schema management.
- **Decision**: We will store Articles as individual JSON files in the `data/` directory.
- **Consequences**:
  - (+) Zero external dependencies; easy to backup (git/zip); human-readable.
  - (-) Difficult to query complex relationships; concurrency limited by filesystem locking.
  - **Mitigation**: Use `atomic_write` pattern to prevent write corruption.

## ADR-002: Atomic File Strategy

- **Status**: Accepted
- **Context**: Writing directly to a file (`open(path, 'w')`) can corrupt data if the process crashes mid-write.
- **Decision**: Implement an `atomic_write` utility that writes to `{filename}.tmp` first, then uses `pathlib.Path.replace()` to atomically swap it into place.
- **Consequences**:
  - (+) Guarantees file integrity; readers never see partial files.
  - (-) Slight IO overhead (double write/rename).

## ADR-003: Session-Based Authentication

- **Status**: Accepted
- **Context**: We need to protect admin routes. JWTs are stateless but require client-side storage management and are complex to invalidate.
- **Decision**: Use Flask's built-in server-side signed sessions ("Secure Cookies").
- **Consequences**:
  - (+) Simple `session['user_id']` decorator checks; automatic handling by browser.
  - (-) Requires `SECRET_KEY` management; scaling horizontally requires sticky sessions or shared session store (Redis) later.

## ADR-004: Explicit CSRF Tokens

- **Status**: Accepted
- **Context**: Flask-WTF is standard but heavy for this minimal scope.
- **Decision**: Implement a lightweight "Synchronizer Token Pattern" manually in `routes/admin.py`.
- **Consequences**:
  - (+) No extra dependency; clear understanding of security flow.
  - (-) Must manually inject `csrf_token` into every POST form and verify in every POST route.
