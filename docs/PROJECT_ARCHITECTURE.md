---
title: Project Architecture Blueprint
version: 1.0
date_created: 2025-12-16
last_updated: 2025-12-16
owner: Personal Blog Project Team
---
# Project Architecture Blueprint — Personal Blog (filesystem-first)

Scope

- Project type: web app (monolithic Flask application)
- Scale: small (guest + single admin users)
- Objective: provide a concise, actionable architecture blueprint that aligns with `docs/project-specification.md`, `docs/DEVELOPMENT_WORKFLOW.md`, and `AGENT.md`.

Notes on alignment: this blueprint consolidates guidance from the referenced docs and records two decisions made during Phase 2 review:

- Test coverage target: standardized to **90%** across PRD, CI workflow, and `ai-coding-assistant.json`.
- Content versioning policy: chosen **Option A — track content**. `data/` and `data/*.json` are tracked in the repository; guidance for maintainers is provided in `data/README.md`.

---

## 1. Architecture Detection and Analysis

- Language & framework: Python 3.8+ with Flask 3.0+. Confirmed by `DEVELOPMENT_WORKFLOW.md` and `AGENT.md`.
- Storage: Filesystem-based JSON articles under `data/` (REQ-001). No external DB dependency (CON-002).
- Organization pattern: Monolithic MVC-style app using Blueprints for separation (`routes/guest.py`, `routes/admin.py`), models in `models.py`, utilities under `utils/` and templates under `templates/`.
- CI / quality tools: pytest, pytest-cov, flake8, mypy called out in docs.

Conclusion: architecture is a small, layered monolith with clear separation of web/controller, model (file persistence), templates, and utilities. This suits a small-scale web app and keeps deployment simple.

---

## 2. Architectural Overview

- Guiding principles:

  - Simplicity and portability: No DB, filesystem-first for easy backups/versioning.
  - Clear separation of concerns: routes/controllers, models (file I/O), utils, templates.
  - Security-by-default: session auth, CSRF, input validation and markdown sanitization required.
  - Testability: high unit/integration coverage expected (PRD: 90%).
- Boundaries:

  - Public boundary: guest routes and rendered HTML (read-only access to published articles).
  - Admin boundary: session-protected routes for CRUD operations that mutate `data/`.
  - Persistence boundary: file system access encapsulated in `models.Article` and file helper utilities.

---

## 3. Architecture Visualization (Mermaid)

```
ASCII Architecture Diagram:

  [Guest Browser]        [Admin Browser]
        |                     |
   HTTP GET             HTTP (Auth)
        |                     |
    +---------------------------+
    |      Flask App Layer      |
    |  +---------+  +---------+ |
    |  |guest_bp |  |admin_bp | |
    |  +----+----+  +----+----+ |
    |       |           |       |
    |    +--+-----------+--+    |
    |    | app factory &  |     |
    |    |   config      |      |
    +----+----------------+-----+
                |
                v
    +-------------------------------+
    |   Service & Models Layer       |
    | +---------------------------+ |
    | | Article Model (models.py) | |
    | +---------------------------+ |
    | | Markdown Renderer         | |
    | | (markdown2 + sanitizer)   | |
    | +---------------------------+ |
    | | Validators & Utils        | |
    | +---------------------------+ |
    +-------------------------------+
                |
                v
        [Filesystem: data/]
```

Notes: diagram intentionally simple — aim is to reflect runtime interactions and component responsibilities.

---

## 4. Core Architectural Components

1. App Factory (`app.py`)

   - Purpose: create and configure Flask app, register blueprints, configure secret keys, and environment-specific settings.
   - Responsibilities: read `.env`, set `SECRET_KEY`, register `guest_bp` and `admin_bp`, apply error handlers and template filters (date, markdown).
2. Routes / Controllers (`routes/guest.py`, `routes/admin.py`)

   - Purpose: HTTP interface layer; validate input, enforce auth for admin routes, orchestrate model operations.
   - Patterns: use Blueprints; keep handlers thin and delegate to `models` and `utils`.
3. Models / Persistence (`models.py`)

   - Purpose: single point-of-truth for article representation and file I/O.
   - API: `Article.to_dict()`, `Article.from_dict()`, `save()`, `load(slug)`, `delete()`, `all()`, `published_articles()`.
   - Implementation notes: use `pathlib.Path`, JSON write with `indent=2`, atomic write (write temp + rename), robust error handling for `JSONDecodeError`.
4. Utilities (`utils/validators.py`, `utils/auth.py`, `utils/file_ops.py`)

   - Validators: slug generation/validation, length and content constraints.
   - Auth: session helpers and `login_required` decorator.
   - File ops: atomic write helper, backup/restore helpers for corrupted JSON.
5. Markdown pipeline

   - Use `markdown2` for Markdown->HTML; pass through sanitizer (`bleach` recommended) to remove risky tags/attributes.
   - Provide a preview endpoint that applies the same sanitization rules.
6. Templates & Static (`templates/`, `static/`)

   - Templates: `base.html` (guest), `admin/base.html`, pages under `guest/` and `admin/`.
   - Static: CSS split between `guest.css` and `admin.css`.

---

## 5. Architectural Layers and Dependency Rules

- Layer map:

  - Presentation: Blueprints + Jinja templates
  - Application/Orchestration: route handlers, forms, flash messages
  - Domain: `Article` model and business rules (validation, published flag semantics)
  - Persistence: filesystem helpers
  - Cross-cutting: utils (auth, validators), config, logging
- Rules:

  - Presentation may call Application/Domain but must not access Persistence directly — always go through model API.
  - Domain layer must not import presentation modules.
  - Utils can be used by all layers but remain implementation-agnostic.

---

## 6. Data Architecture

- Article JSON schema (canon from `docs/project-specification.md`):

```json
{
  "slug": "string",
  "title": "string",
  "content": "string (Markdown)",
  "excerpt": "string",
  "author": "string",
  "created_at": "ISO 8601 string",
  "updated_at": "ISO 8601 string",
  "published": true,
  "tags": ["string"]
}
```

- Storage considerations:
  - Filenames: `{slug}.json` under `data/`.
  - Atomic writes and backups: write to `{slug}.json.tmp` and rename to reduce corruption risk.
  - Optional: maintain `data/index.json` (cache) with summaries for faster listing; regenerate on writes.

---

## 7. Cross-Cutting Concerns

Authentication & Authorization

- Session-based admin login (per docs). Store session cookie securely (Secure, HttpOnly when using HTTPS). Use environment-stored credentials or hashed password env variable (`ADMIN_PASSWORD_HASH`).

CSRF

- Integrate a CSRF token for all POST endpoints. Options: Flask-WTF or lightweight per-form token stored in session.

Input Validation & Sanitization

- Validate all fields server-side via `utils.validators`. Sanitize Markdown output via `bleach` with a restrictive whitelist.

Error Handling & Resilience

- Centralized error handlers for 404/500. Log exceptions with contextual info. For file I/O failures, provide friendly admin messages and keep problematic files in `data/.corrupt/` for later inspection.

Logging & Monitoring

- Use Python `logging` to emit structured logs. For small scale, local logs suffice; for production, forward to hosted logging provider.

Configuration Management

- Use `python-dotenv` for development; require `SECRET_KEY`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD_HASH` in env for production.

---

## 8. Service Communication Patterns

- This monolith uses internal function calls — no inter-service comms.
- External integrations (optional): RSS generation, image processing, TTS — treat as separate adapters invoked by CLI or background tasks.

---

## 9. Python-specific Architectural Patterns

- Module organization: follow `AGENT.md` layout: `app.py`, `models.py`, `routes/`, `utils/`, `templates/`, `static/`, `data/`.
- Prefer simple class-based model (`Article`) for domain logic; keep side-effects (file writes) inside model methods.
- Use type hints and docstrings (Google style) across modules.

---

## 10. Implementation Patterns & Recommendations

- Atomic file write pattern (recommended): write to temporary file and `Path.replace()` to guarantee atomic swap.
- Concurrency: for small scale, locking is optional but recommended to avoid race conditions; use file locks (e.g., `portalocker`) if concurrent admin writes expected.
- Markdown safety: chain `markdown2` -> `bleach.clean()` with allowed tags and attributes.
- Slug handling: generate using regex and normalize to lowercase; validate to prevent traversal.

---

## 11. Testing Architecture

- Strategy:

  - Unit tests for `Article` model (save/load/delete/all/published_articles) using temporary `data` dir fixtures.
  - Integration tests for routes: guest listing, article detail (404 cases), admin create/edit/delete with auth fixture.
  - Sanitization tests: ensure previewed HTML contains no disallowed tags/attributes.
- Coverage target: standardize to **90%** per `project-specification.md` and `EPIC-PRD.md`.

---

## 12. Deployment Architecture

- Recommended minimal deployment:

  - Dockerize app with a simple `Dockerfile` that copies code, installs `requirements.txt`, and runs `gunicorn` for production.
  - Mount persistent storage for `data/` (volume) and ensure permissions allow writes.
- Environment vars required:

  - `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD_HASH`, `FLASK_ENV`.

---

## 13. Extension & Evolution Patterns

- Feature addition: new route -> add blueprint handler -> use model API -> add template -> add tests.
- To add background processing or queue: introduce a small worker process or use platform cron; keep integration via adapters.

---

## 14. Architectural Decision Records (summary)

- Decision: Filesystem-first storage — tradeoff: simplicity and portability vs. queryability and concurrency. Rationale in `project-specification.md`.
- Decision: Monolithic Flask app — fits small scale and lowers operational overhead.
- Decision pending: data/ tracking policy and test coverage target (see Alignment section).

---

## 15. Alignment & Action Items (differences found)

1. Coverage target mismatch

   - Source: `docs/project-specification.md` and `docs/EPIC-PRD.md` -> 90%
   - Source: `docs/DEVELOPMENT_WORKFLOW.md` / `ai-coding-assistant.json` -> 80%
   - Action: standardize to 90% in CI config and `ai-coding-assistant.json` to match PRD.
2. Data versioning / `.gitignore` mismatch

   - Source: `.gitignore` in `DEVELOPMENT_WORKFLOW.md` excludes `data/*.json`.
   - Source: PRD expects articles be versionable and data stored as JSON.
   - Action options:
     - Option A (track content): remove `data/*.json` from `.gitignore`, add guidance for sensitive data, and provide `data/README.md` to instruct maintainers.
     - Option B (ignore content): keep `data/` ignored and add `seed/` or `content/` with tracked canonical posts and import scripts. Document tradeoffs.
3. Sanitization requirement

   - TODO: Ensure `bleach` or equivalent is specified in `requirements.txt` and used before enabling preview endpoints.

---

## 16. Blueprint for New Development (quick checklist)

When implementing a new feature:

1. Add route in appropriate `routes/` blueprint.
2. Add domain logic to `models.py` or new model module.
3. Add validators in `utils/validators.py`.
4. Add templates under `templates/guest` or `templates/admin`.
5. Add unit tests and integration tests; update fixtures.
6. Ensure linting and mypy pass locally.

---

References

- docs/project-specification.md
- docs/DEVELOPMENT_WORKFLOW.md
- AGENT.md
- docs/EPIC-PRD.md

v1.0.0 | Active | Last Updated: Dec 16 2025 - 14:30
