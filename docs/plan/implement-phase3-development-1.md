---
goal: Implement Phase 3 — Development & Quality Gates
version: 1.0
date_created: 2025-12-16
last_updated: 2025-12-16
owner: Personal Blog Project Team
status: 'Planned'
tags: [feature, implement, phase3]
---

# Introduction

![Status: Planned](https://img.shields.io/badge/status-Planned-blue)

This plan implements the Phase 3 backlog defined in docs/Phase3_Development_Quality_Gates.md. It is deterministic, machine-readable, and organized into atomic phases with explicit file-level tasks and verification steps.

Pre-Implementation Checklist (MANDATORY)

- [ ] **MANDATORY**: Read and understand docs/Phase3_Development_Quality_Gates.md
- [ ] **MANDATORY**: Inspect repository conventions: docs/DEVELOPMENT_WORKFLOW.md, docs/TECH-STACK.md
- [ ] **MANDATORY**: Confirm test runner: `pytest` and CI coverage settings from ai-coding-assistant.json
- [ ] **MANDATORY**: Identify target files listed in this plan and open them before coding

## 1. Requirements & Constraints

- **REQ-001**: Implement `models.Article` with methods `to_dict()`, `from_dict(dict)`, `save()`, `load(slug)`, `delete()`, `all()`, `published_articles()`.
- **REQ-002**: All file writes must be atomic: write a temporary file then `Path.replace()` to final path (see `utils/file_ops.py`).
- **REQ-003**: JSON must be UTF-8 encoded; decode errors must be handled and surfaced as `ValidationError`.
- **SEC-001**: Admin authentication must use hashed password from env var `ADMIN_PASSWORD_HASH`. Session cookie settings must be hardened for production.
- **GUD-001**: Follow existing repository patterns and tests style; use `pytest` and fixtures in `tests/conftest.py`.
- **CON-001**: Coverage threshold: `--cov-fail-under=90` (CI requirement).

## 2. Implementation Steps

### Implementation Phase 1

- GOAL-001: Implement core model and file utilities required by remaining features.

| Task | Description | File(s) | Function(s) | Completed | Date |
|------|-------------|---------|-------------|-----------|------|
| TASK-001 | Implement atomic file helper and tests | utils/file_ops.py, tests/utils/test_file_ops.py | `atomic_write(path, data: bytes, tmp_suffix='.tmp')` | ✅ | 2025-12-16 |
| TASK-002 | Implement `models.Article` with persistence and validation | models/article.py, tests/models/test_article.py | `Article.to_dict()`, `Article.from_dict()`, `Article.save()`, `Article.load(slug)`, `Article.delete()`, `Article.all()`, `Article.published_articles()` | ✅ | 2025-12-16 |
| TASK-003 | Add domain exceptions | models/exceptions.py, tests/models/test_exceptions.py | `ArticleNotFound`, `ValidationError` | ✅ | 2025-12-16 |

### Implementation Phase 2

- GOAL-002: Implement service layer and basic business logic.

| Task | Description | File(s) | Function(s) | Completed | Date |
|------|-------------|---------|-------------|-----------|------|
| TASK-004 | Implement `services/article_service.py` with create/save/publish logic | services/article_service.py, tests/services/test_article_service.py | `create_from_form(form_data)`, `save(article)`, `publish(slug)`, `unpublish(slug)`, `list_articles(sort_by, reverse)` | | |
| TASK-005 | Add validators for slug/title/excerpt/tags | utils/validators.py, tests/utils/test_validators.py | `validate_slug(s)`, `validate_title(s)`, `normalize_tags(tags)` | | |

### Implementation Phase 3

- GOAL-003: Routes, templates, and security

| Task | Description | File(s) | Function(s) / Endpoints | Completed | Date |
|------|-------------|---------|------------------------|-----------|------|
| TASK-006 | Implement guest routes for viewing articles and list | routes/guest.py, templates/guest/*, tests/routes/test_guest.py | `GET /`, `GET /articles/<slug>` | ✅ | 2025-12-16 |
| TASK-007 | Implement admin routes with session auth and CSRF protection | routes/admin.py, templates/admin/*, tests/routes/test_admin.py | `GET /admin`, `POST /admin/articles/create`, `POST /admin/articles/<slug>/publish` | | |
| TASK-008 | Add security helpers for password hashing & session config | utils/security.py, tests/utils/test_security.py | `hash_password(pw)`, `check_password(hash,pw)`, `configure_session(app)` | | |

### Implementation Phase 4

- GOAL-004: Tests, CI, packaging and docs

| Task | Description | File(s) | Commands / Validation | Completed | Date |
|------|-------------|---------|-----------------------|-----------|------|
| TASK-009 | Add pytest fixtures and integration tests | tests/conftest.py, tests/integration/test_smoke.py | `pytest -q` | | |
| TASK-010 | Add `requirements.txt` with pinned versions | requirements.txt | verify `pip install -r requirements.txt` | | |
| TASK-011 | Add `Dockerfile` and `Makefile` for dev tasks | Dockerfile, Makefile | `docker build .` | | |
| TASK-012 | Update README.md and docs/ with quickstart and ADRs | README.md, docs/ARCHITECTURE_DECISIONS.md | `markdownlint` (if configured) | | |

## 3. Alternatives

- **ALT-001**: Use SQLite instead of file-based persistence — rejected to keep zero-dependency file-storage and match Phase 3 spec.
- **ALT-002**: Use Flask-WTF for CSRF — acceptable; plan uses lightweight custom tokens unless CSRF library already present in requirements.

## 4. Dependencies

- **DEP-001**: Flask==3.0.0
- **DEP-002**: python-dotenv==1.0.0
- **DEP-003**: markdown2==2.4.10
- **DEP-004**: bleach (latest pinned in requirements.txt)
- **DEP-005**: pytest, pytest-cov

## 5. Files

- **FILE-001**: models/article.py — new core model
- **FILE-002**: utils/file_ops.py — atomic file helper
- **FILE-003**: services/article_service.py — business logic
- **FILE-004**: utils/validators.py — validation helpers
- **FILE-005**: routes/guest.py — guest routes
- **FILE-006**: routes/admin.py — admin routes
- **FILE-007**: templates/guest/ — guest templates
- **FILE-008**: templates/admin/ — admin templates
- **FILE-009**: tests/ — unit and integration tests as described above
- **FILE-010**: requirements.txt, Dockerfile, Makefile

## 6. Testing

- **TEST-001**: Unit tests for `models.Article` covering save/load/delete, JSON decode errors, validation failures.
- **TEST-002**: Unit tests for `utils/file_ops.atomic_write` ensuring atomicity (create then replace semantics in test tmpdir).
- **TEST-003**: Service layer tests for create/publish/unpublish and list sorting.
- **TEST-004**: Integration tests using Flask test client for guest and admin routes, including CSRF and auth flows.
- **TEST-005**: Coverage target: `pytest --cov=. --cov-fail-under=90` must pass in CI.

Run commands for local verification:

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
pytest -q
pytest --cov=. --cov-report=term-missing --cov-fail-under=90
```

## 7. Risks & Assumptions

- **RISK-001**: File-based storage may not scale; mitigate by creating `data/index.json` as cache (optional TASK).
- **RISK-002**: CI environment differences; run tests locally and in CI using identical Python version.
- **ASSUMPTION-001**: Existing codebase follows Flask patterns; templates folder layout is compatible.

## 8. Related Specifications / Further Reading

- docs/Phase3_Development_Quality_Gates.md
- docs/DEVELOPMENT_WORKFLOW.md
- docs/TECH-STACK.md

---

v1.0.0 | Planned | Last Updated: 2025-12-16
