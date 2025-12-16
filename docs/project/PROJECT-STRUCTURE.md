---
title: Project Folders Structure Blueprint
version: 1.0
date_created: 2025-12-16
last_updated: 2025-12-16
owner: Personal Blog Project Team
---

# Project Folders Structure Blueprint (auto-detected)

Detection summary
- Project type: single-app Flask web application (monolithic, filesystem-first)
- Primary language: Python 3.8+
- Storage: filesystem JSON articles under `data/` (tracked in repo — Option A)
- CI & QA: GitHub Actions, `pytest` + `pytest-cov` (coverage target 90%)

This blueprint documents source organization, test locations, configuration files, documentation structure, and a detailed ASCII file tree with per-file/folder descriptions.

---

**High-level organization principles**
- Layered monolith: presentation (templates + routes), application (route handlers), domain (models), persistence (file helpers), and utilities.
- Conventions: PEP-8 style, type hints, Google-style docstrings, tests under `tests/`, tracked `data/` JSON content for versioning.

---

**ASCII directory map (depth=4)**

```
Personal_Blog/
├── .github/
│   ├── workflows/ci.yml                 # CI: tests + coverage enforcement
│   └── prompts/                         # prompt templates (project-specific)
├── data/                                # Tracked content: {slug}.json articles
│   └── README.md                         # Guidance for maintainers about tracked content
├── docs/                                # Project documentation and blueprints
│   ├── DEVELOPMENT_WORKFLOW.md
│   ├── EPIC-PRD.md
│   ├── Project_Architecture_Blueprint.md
│   ├── Technology_Stack_Blueprint.md
│   └── Project_Folders_Structure_Blueprint.md  # (this file)
├── routes/                              # Flask Blueprints: guest + admin
│   ├── guest.py
│   └── admin.py
├── templates/                            # Jinja2 templates (guest & admin)
│   ├── base.html
│   └── admin/
├── static/                               # CSS, JS, images
├── utils/                                # Helpers: validators, auth, file ops
│   ├── validators.py
│   └── file_ops.py
├── tests/                                # Unit and integration tests
│   ├── unit/
│   │   └── test_models.py
│   └── integration/
│       └── test_routes.py
├── app.py                                # App factory and entrypoint
├── models.py                             # Domain model: Article
├── requirements.txt                      # Pinned dependencies (recommended)
├── .gitignore
├── README.md
└── ai-coding-assistant.json              # AI config (coverage_required: 90)
```

---

Directory & file descriptions

- `.github/` — CI and project automation. Key files:
  - `.github/workflows/ci.yml`: runs tests, enforces 90% coverage, lints as configured.
  - `.github/prompts/`: prompt templates and agent artifacts used in AI-assisted development.

- `data/` — Tracked article JSON files. Each article stored as `data/{slug}.json` using UTF-8 and `json.dump(..., indent=2, ensure_ascii=False)`.
  - `data/README.md`: explains Option A (track content), sensitive-data guidance, and backup/versioning tips.

- `docs/` — Project documentation. Important docs already present:
  - `DEVELOPMENT_WORKFLOW.md`: contributor workflow, environment setup.
  - `Project_Architecture_Blueprint.md`: architecture rationale, decisions (coverage=90%, track `data/`).
  - `EPIC-PRD.md`: PRD and feature breakdowns.
  - `Technology_Stack_Blueprint.md`: stack choices and dev guidance.
  - `Project_Folders_Structure_Blueprint.md`: this blueprint.

- `routes/` — Flask Blueprints. Conventions:
  - `guest.py`: public-facing routes (list, detail, RSS, preview read-only endpoints).
  - `admin.py`: admin CRUD routes under `/admin` with `login_required` checks and CSRF for write operations.

- `templates/` — Jinja templates organized by purpose:
  - `base.html`: shared layout for guest site.
  - `admin/`: admin-specific base and pages.
  - Use template inheritance and filters for markdown/date formatting.

- `static/` — Assets: CSS split `guest.css` / `admin.css`, optional JS (progressive enhancement), images.

- `utils/` — Reusable helpers:
  - `validators.py`: slug, title, content validators.
  - `file_ops.py`: atomic file write helper (write `.tmp` then `Path.replace()`), optional locking helper.

- `models.py` — `Article` domain model exposing:
  - `to_dict()`, `from_dict()`, `save()`, `load(slug)`, `delete()`, `all()`, `published_articles()`.
  - Implementation notes: use `pathlib.Path`, robust JSON decode handling, and atomic writes. Tests should cover all methods and edge cases.

- `tests/` — Tests organized by type and scope:
  - `tests/unit/`: unit tests for `models.py`, `utils/`, validators. Naming: `test_<module>.py` or `test_<feature>.py`.
  - `tests/integration/`: integration tests for `routes/` using Flask test client. Include auth fixtures for admin flows.
  - Fixtures: `tests/conftest.py` (provides `tmp_path` override for `data/`, `app`, `client`, and auth session fixtures).

- Root files:
  - `app.py`: application factory `create_app(config_name=None)` registering blueprints and config.
  - `requirements.txt`: pin versions (Flask==3.0.0, python-dotenv==1.0.0, markdown2==2.4.10, bleach, pytest, pytest-cov, flake8, mypy).
  - `.gitignore`: updated to allow `data/` and `data/*.json` (per Option A); still ignore `venv/`, logs, IDE files.
  - `ai-coding-assistant.json`: AI config including `coverage_required: 90`.

---

Testing locations & patterns (recommended)

- Unit tests
  - Location: `tests/unit/`
  - Naming: `test_models.py`, `test_utils.py`, `test_validators.py`.
  - Use `tmp_path` or a `tmp_data_dir` fixture to isolate `data/` access.

- Integration tests
  - Location: `tests/integration/`
  - Files: `test_guest_routes.py`, `test_admin_routes.py`.
  - Use Flask test client fixtures and a temporary `data/` directory.

- Test fixtures
  - `tests/conftest.py` provides `app`, `client`, `tmp_data_dir`, `auth_headers` or `admin_session` helper.

---

Configuration files (what to expect)

- `requirements.txt` — pinned dependencies for reproducible installs.
- `.env` / `.env.example` — environment variables (do not commit `.env`): `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD_HASH`.
- `.flaskenv` (optional) — local dev run config.
- `.github/workflows/ci.yml` — CI pipeline executing tests, linters, and coverage check (90% threshold).
- `ai-coding-assistant.json` — AI assistant settings used by project tooling.

---

Documentation structure and guidance

- Primary user-facing docs: `README.md` with quickstart and `docs/DEVELOPMENT_WORKFLOW.md` for contributor guidelines.
- Technical artifacts: `docs/EPIC-PRD.md`, `docs/Project_Architecture_Blueprint.md`, `docs/Technology_Stack_Blueprint.md`.
- Keep ephemeral notes and decisions in `docs/project_memory.md` (if present) or an `ARCHITECTURE_DECISIONS.md` file for ADRs.

---

File placement rules & naming conventions

- Python modules: snake_case filenames (e.g., `file_ops.py`), classes in PascalCase (e.g., `Article`).
- Tests: prefix `test_` and mirror module structure where helpful.
- Templates: group by feature (e.g., `templates/guest/`, `templates/admin/`).
- Article filenames: slugs must match regex `^[a-z0-9-]+$` (no `..`, no slashes).

---

Quick developer tasks (when adding a feature)

1. Add routes in `routes/` blueprint file.
2. Implement domain logic in `models.py` or a new model module.
3. Add validators in `utils/validators.py` if new input types are required.
4. Add templates under `templates/` and static assets under `static/`.
5. Add unit tests to `tests/unit/` and integration tests to `tests/integration/`.
6. Run CI locally with `pytest --cov=.` and ensure coverage >= 90%.

Try-it commands (local dev)

```bash
python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt
pytest --maxfail=1 --disable-warnings -q
```

---

Decision notes & next steps

- Detection concluded this is a single-app monolith (not a monorepo or microservices). If you prefer a different layout (monorepo or multi-service), request a reorganization plan.
- Next recommended work: implement `models.Article` with atomic write/load/delete and a comprehensive test suite in `tests/unit/test_models.py` to begin satisfying the 90% coverage target.

v1.0.0 | Active | Last Updated: Dec 16 2025 - 14:30