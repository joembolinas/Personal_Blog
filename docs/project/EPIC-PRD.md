---
title: Personal Blog CMS - Epic PRD & Architecture
version: 1.0
date_created: 2025-12-16
last_updated: 2025-12-16
owner: Personal Blog Project Team
---
# Epic PRD: Personal Blog CMS (Filesystem-based)

## 1. Epic Name

Personal Blog CMS — Filesystem-first Article Publishing

## 2. Goal

- Problem: Individuals and small teams need a lightweight, easy-to-run blogging CMS that requires no database, is versionable via git, and supports safe Markdown rendering, admin editing, and simple deployment. Existing solutions are often heavyweight or require infrastructure the user doesn't want to manage.
- Solution: Provide a Flask-based CMS that stores articles as JSON/Markdown files in `data/`, exposes a public guest site and a secured admin UI with session-based auth, CSRF protection, and safe Markdown-to-HTML rendering.
- Impact: Faster time-to-publish for non-technical authors, low operational cost (no DB), easier backups/versioning, and maintainable code suitable for learning and small deployments.

## 3. User Personas

- Admin: Individual blog owner or small-team editor who creates, edits, and publishes articles.
- Guest Reader: Public visitor who browses, searches, and reads published articles.
- Developer / Maintainer: Contributor who extends features, runs tests, and deploys the site.

## 4. High-Level User Journeys

- Admin onboarding: set SECRET_KEY and admin credentials → login → create article → preview → publish.
- Reader journey: visit homepage → view list of published articles → open article → share or search by tag.
- Maintenance flow: developer runs tests → creates article fixtures → deploys via simple container or static-friendly host.

## 5. Business Requirements

- Functional Requirements:

  - FR1: Create, read, update, delete articles persisted as `data/{slug}.json` (REQ-001).
  - FR2: Public site listing published articles and single-article view (GET /, GET /article/`<slug>`).
  - FR3: Admin UI with session-based login and article management (REQ-002, REQ-003).
  - FR4: CSRF protection on all forms (REQ-004).
  - FR5: Markdown content rendered safely to HTML (REQ-005).
  - FR6: Validation and sanitization of inputs (SEC-002).
- Non-Functional Requirements:

  - NFR1: Deployable without a DB (CON-002).
  - NFR2: Python 3.8+ and Flask 3.0+ compatibility (CON-001).
  - NFR3: PEP 8 and project coding standards (GUD-001).
  - NFR4: Proper test coverage and CI (pytest + GitHub Actions).

## 6. Success Metrics

- Time to first published article: < 10 minutes from repo clone.
- Test coverage: >= 90% (as specified in docs/project-specification.md).
- Page load time: < 1s with 100 articles (manual perf target).
- Admin user can create/edit/delete articles and changes persist to `data/`.

## 7. Out of Scope

- Multi-user roles beyond single-admin model (e.g., granular roles/permissions).
- High-scale features like indexing or advanced query APIs (beyond filesystem scans).

## 8. Business Value

- Value: High — low-cost, easy-to-run CMS helps individuals and small teams publish quickly; strong learning product for new devs.

---

## Part 2 — Epics Breakdown (from docs/project-specification.md)

Epic list (prioritized by business value & dependencies):

1. Content Management (Epic A)

   - User value: Create/edit/publish articles; core product capability.
   - Business priority: Highest.
   - Dependencies: Models + file storage, admin auth, markdown rendering.
2. Public Site & Rendering (Epic B)

   - User value: Fast public site with article listings and article pages.
   - Business priority: High.
   - Dependencies: Content Management (A), markdown rendering, templates.
3. Authentication & Security (Epic C)

   - User value: Protect admin UI, secure forms.
   - Business priority: High (security is critical).
   - Dependencies: Session management, CSRF middleware, secure config (.env).
4. Validation, Sanitization & Markdown Safety (Epic D)

   - User value: Prevent XSS and data corruption; safe rendering.
   - Business priority: High.
   - Dependencies: Markdown library selection, sanitization utilities.
5. Testing, CI & Quality (Epic E)

   - User value: Confidence in releases and regressions prevented.
   - Business priority: Medium-High.
   - Dependencies: Model code, routes, fixtures.
6. Deployment & Infrastructure (Epic F)

   - User value: Simple deploy options (container or simple host) and environment config.
   - Business priority: Medium.
   - Dependencies: App packaging, requirements.txt, Dockerfile.

Notes on dependencies: Epics A and C are prerequisites for B. D affects A+B for safety. E should run alongside development; F depends on completed features from A/B/C.

---

## Part 3 — Technical Architecture Considerations (apply epics)

### Architecture Overview

Small monolithic Flask app organized by Blueprints (`routes/guest.py`, `routes/admin.py`), a models layer (`models.py`) handling filesystem persistence under `data/`, and utilities (`utils/validators.py`, `utils/auth.py`). Templates under `templates/` and static assets in `static/`.

### System Components Needed

- Flask app and Blueprints (guest, admin).
- Article model: `Article` class with `to_dict()`, `from_dict()`, `save()`, `load()`, `delete()`, `all()`, `published_articles()`.
- Storage subsystem: file I/O wrapper using `pathlib` and strict filename/slug validation.
- Auth subsystem: session-based login, `login_required` decorator.
- CSRF protection: integrate Flask's CSRF or a lightweight token system.
- Markdown renderer: `markdown2` with safe-lite pipeline + sanitizer (e.g., bleach) or restricted rendering extras.
- Validation library/functions: slug, title, content validation.
- Tests: pytest fixtures, unit + integration tests for file I/O and routes.
- CI: GitHub Actions workflow to run tests and lint.

### Integration Points

- Template rendering uses article data from model layer.
- Admin routes call model methods that persist JSON files in `data/`.
- Environment variables loaded via `python-dotenv` (.env) for secrets.

### Technical Risks

- Race conditions on simultaneous writes to the same file (low for small single-admin sites but must be guarded with atomic write patterns).
- XSS or unsafe HTML from Markdown — must sanitize output or limit HTML features.
- Corrupt JSON files causing runtime errors — implement robust error handling and recovery (backups/temp files).
- File path traversal risks — validate slugs and never accept raw filenames from users.

### Infrastructure Requirements

- Host capable of running Python 3.8+ and Flask 3.0 (any small VPS or container platform).
- Optional: containerization (Dockerfile) for consistent deploys.
- Filesystem with write access for `data/` directory and secure .env storage for secrets.

---

## System Architecture Diagram (Mermaid)

```text
                           +----------------+      +----------------+
                           |Browser - Guest |      |Browser - Admin |
                           +--------+-------+      +--------+-------+
                                    |                       |
                                    | GET /, GET /article  | Admin UI
                                    v                       | requests
                                 +------+               +----v----+
                                 |guest_|               | admin_ |
                                 | bp   |               | bp     |
                                 +--+---+               +---+----+
                                    |                       |
                                    +--------+--------------+
                                             |
                                             v
                                +-------------------------------+
                                |          Flask App            |
                                |  (routes, templates, handlers)|
                                +--------+----------+-----------+
                                         |          |
                    public/site flows --->+          +---> validators &
                                         |                     sanitizer
                                         v                         ^
                                +----------------+                |
                                | Article Model  |<---------------+
                                |   (M)          |                |
                                +--------+-------+                |
                                         |                        |
                                         v                        |
                                +----------------+               |
                                | Filesystem     |               |
                                | (data/)        |               |
                                +----------------+               |
                                                                 |
                                +----------------+               |
                                | Markdown       |---------------+
                                | Renderer (MD)  |
                                +----------------+

Legend:
- guest_bp / admin_bp: Blueprints handling guest/admin requests
- Flask App: coordinates routes, invokes model/renderer/validators
- Article Model -> Filesystem: persistence of data/{slug}.json
- Markdown Renderer -> Validators: sanitized HTML pipeline
```

---

## High-Level Features & Technical Enablers

- Features:

  - Article CRUD with filesystem persistence
  - Public listing and article view pages
  - Admin login and session management
  - Safe Markdown rendering and excerpts
  - Search by tag and simple pagination (optional)
- Technical enablers:

  - `markdown2` + sanitizer or equivalent
  - Atomic file write utility
  - CSRF token implementation or Flask-WTF integration
  - GitHub Actions for tests and linting
  - Dockerfile for containerization

## Technology Stack

- Python 3.8+
- Flask 3.0+
- markdown2
- python-dotenv
- pytest + pytest-cov
- flake8 / mypy (lint + types)

## Technical Value

- High: delivers core functionality with low operational cost and high learnability.

## T-Shirt Size Estimate

- Epic A (Content Mgmt): M
- Epic B (Public site): S-M
- Epic C (Auth & Security): S
- Epic D (Sanitization & Validation): S
- Epic E (Testing & CI): S
- Epic F (Deployment): S

---

## Task 4 — Feature PRD: "Article Management (Admin CRUD)" (from Epic A)

### 1. Feature Name

Article Management — Create / Edit / Delete / Publish articles

### 2. Epic

Parent Epic: Content Management (Epic A)

### 3. Goal

- Problem: Admins need a simple UI to manage article lifecycle without editing JSON by hand.
- Solution: Provide an admin UI with form-driven create/edit flows, preview, and publish toggles, persisting to `data/{slug}.json` with validation and safe Markdown handling.
- Impact: Non-technical users can publish reliably; reduces errors and time to publish.

### 4. User Personas

- Admin (primary): create and maintain content.

### 5. User Stories

- As an Admin, I want to create an article with title, slug, content, excerpt, tags, and publish flag so that I can publish a new post.
- As an Admin, I want to preview the rendered article before publishing so that I can verify formatting and safety.
- As an Admin, I want to edit an existing article and save changes without losing history (file is updated) so that I can correct mistakes.
- As an Admin, I want to delete an article so that I can remove outdated content.

### 6. Requirements

- Functional Requirements:

  - FR1: Admin form accepts `title`, `slug`, `content` (Markdown), `excerpt`, `author`, `tags`, `published`.
  - FR2: On save, validate required fields; generate `created_at` and `updated_at` ISO timestamps.
  - FR3: Save to `data/{slug}.json` atomically (write temp then move).
  - FR4: Provide preview endpoint that renders sanitized HTML from Markdown (no permanent save required).
  - FR5: Deleting an article removes the JSON file (with confirmation).
- Non-Functional Requirements:

  - NFR1: Atomic writes to prevent file corruption.
  - NFR2: Slug validation: lowercase, alphanum + hyphens; prevent path traversal.
  - NFR3: All admin endpoints protected by session-based auth + CSRF.

### 7. Acceptance Criteria

- AC1 (Create): Given valid form data, when I submit create, then `data/{slug}.json` exists and article appears in published list (if published=true).
- AC2 (Preview): Given Markdown content, when I request preview, then server returns sanitized HTML matching expected rendering.
- AC3 (Edit): Given an existing slug, when I edit and save, then the file is updated and `updated_at` changes.
- AC4 (Delete): Given a deletion action and confirmation, when executed, then the file is removed and article no longer accessible.

### 8. UI/UX Requirements

- Admin create/edit form layout:
  - Fields: Title (text), Slug (text, auto-generated editable), Excerpt (textarea), Content (large textarea with Markdown help), Tags (comma-separated), Published (checkbox), Save, Preview, Delete (for edits).
  - Inline validation errors and flash messages for success/failure.
  - Preview opens in a modal or separate panel showing rendered (sanitized) HTML.

### 9. Edge Cases

- Slug collision: attempting to create with existing slug should prompt to overwrite or choose a new slug.
- Invalid JSON on disk for an article: edit should surface an error and offer to restore from backup if available.
- Very large article content: server should handle up to a reasonable size (document recommended limit, e.g., 1MB) and reject larger uploads.

### 10. Error Handling

- Validation errors: return 400 with field-level messages displayed in form.
- File I/O errors: return 500 with a friendly message and log full exception server-side.
- Concurrent write: use atomic file write; if write fails due to lock, show retry message.
- Sanitization failure: refuse to preview/render and log the raw Markdown for developer diagnosis.

---

## Comparison & Alignment with existing docs

- Consistency with [docs/DEVELOPMENT_WORKFLOW.md](docs/DEVELOPMENT_WORKFLOW.md): This PRD follows the described technology stack (Flask, markdown2), coding standards (PEP8, type hints), and file layout (models, routes, templates). It keeps the filesystem-first storage pattern and required features (CSRF, session auth).
- Consistency with [AGENT.md](AGENT.md): Architecture and component breakdown mirror the directory layout and priorities in AGENT.md. Epics A-F map to the modules described there (`routes/`, `models.py`, `templates/`).
- Notes on policy from repository docs: Do not include AI/agent provenance in public docs or README (see .github/copilot-instructions). This EPIC PRD avoids exposing AI-assistant involvement.

---

## Next Steps / Recommendations

- Implement `models.Article` and unit tests first (Epic A), add atomic write utility.
- Add minimal admin auth and CSRF (Epic C) to enable safe admin flows.
- Implement markdown rendering + sanitizer before enabling preview (Epic D).
- Add GitHub Actions workflow to run tests and linters (Epic E).

---

References

- docs/project-specification.md
- docs/DEVELOPMENT_WORKFLOW.md
- AGENT.md

```
v1.0.0 | Active | Last Updated: Dec 11 2025 - 14:30
```
