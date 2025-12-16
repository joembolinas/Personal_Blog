---
title: Technology Stack Blueprint
version: 1.0
date_created: 2025-12-16
last_updated: 2025-12-16
owner: Personal Blog Project Team
---
# Technology Stack Blueprint — Personal Blog

Scope & Auto-detected context

- Project type: Python web application (Flask)
- Scale: small (guest users + single admin)
- Team expertise (auto-detect): Python / Flask oriented
- Preferred language (auto-detect): Python
- Deployment target (auto-detect): container or small VPS (Docker + volume for `data/`)

References

- `docs/project-specification.md`
- `docs/DEVELOPMENT_WORKFLOW.md`
- `docs/Project_Architecture.md`
- `AGENT.md`

---

## 1. Technology Identification

- Language: Python 3.8+ (docs require 3.8+)
- Web framework: Flask 3.0.0 (docs/DEVELOPMENT_WORKFLOW.md)
- Markdown: markdown2 (markdown2==2.4.10)
- Env/config: python-dotenv (python-dotenv==1.0.0)
- Testing: pytest, pytest-cov
- Linting / type: flake8, mypy
- Sanitization: bleach (recommended for markdown output)

Package versions referenced in docs (recommended):

- Flask==3.0.0
- python-dotenv==1.0.0
- markdown2==2.4.10
- pytest (latest 7.x), pytest-cov
- bleach (pin per policy)

---

## 2. Core Technologies & Purpose

- Flask 3.0: application factory pattern, Blueprints for `guest` and `admin` routes, lightweight server-side templating with Jinja2.
- Jinja2: HTML templating and template inheritance (`base.html`, `admin/base.html`).
- Filesystem storage: JSON files stored in `data/{slug}.json` (Article model handles serialization). No external DB dependency.
- markdown2 + sanitizer: convert article Markdown to HTML, then sanitize via `bleach`.
- python-dotenv: load environment variables for secrets (SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD_HASH).

---

## 3. Project Conventions & Coding Standards

- Style guide: PEP 8; line length 88
- Type hints: used throughout for public functions and models
- Docstrings: Google style required
- File organization (per AGENT.md):
  - `app.py` — factory and app config
  - `models.py` — domain model (`Article`)
  - `routes/guest.py`, `routes/admin.py` — blueprints
  - `utils/` — validators, auth, file helpers
  - `templates/`, `static/`
  - `data/` — tracked article JSON files

---

## 4. Implementation Patterns & Recommendations

- Article model

  - Keep persistence inside `models.Article` methods.
  - Use `pathlib.Path` and context managers for file I/O.
  - Save JSON with `json.dump(..., indent=2, ensure_ascii=False)`.
  - Atomic write: write to `{slug}.json.tmp` then `Path.replace()` to `{slug}.json`.
- Markdown pipeline

  - `html = markdown2.markdown(markdown_text, extras=[...])`
  - `safe_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)`
- Slug handling

  - Generate and validate slugs using regex; deny `..`, slashes, and empty values.
- Concurrency

  - For a single-admin small site, optional, but recommend file lock (`portalocker`) if concurrent writes possible.
- Error handling

  - Model methods return None or raise documented exceptions; controllers translate to HTTP codes and flash messages.

---

## 5. Testing & CI

- Testing framework: `pytest` with fixtures that use a temporary `data/` directory via `tmp_path`.
- Coverage: enforced at 90% in CI (see `.github/workflows/ci.yml` and `ai-coding-assistant.json`).
- Tests to include:
  - Unit: `Article` methods, validators, file ops.
  - Integration: guest routes, article detail, 404 handling.
  - Admin flows: auth, create/edit/delete (with session fixtures).
  - Sanitization tests for rendered HTML.

---

## 6. Tooling & Local Dev Setup

- Virtual env: `python -m venv venv`
- Install: `pip install -r requirements.txt` (recommend adding `requirements.txt` with pinned versions).
- Lint: `flake8` and `mypy` before commit.
- Run app: `python app.py` (development) or `gunicorn 'app:create_app()'` for production within Docker.

---

## 7. Deployment Recommendations

- Containerization: provide `Dockerfile` and `docker-compose.yml` for local dev/prod parity.
- Persistence: mount host volume for `data/` and ensure proper permissions.
- Secrets: do not store in repo; use environment variables or secret manager.

Minimal `Dockerfile` guidance:

```
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:create_app()"]
```

---

## 8. Security Considerations

- Authentication: session-based admin auth with secure cookies; store hashed password in `ADMIN_PASSWORD_HASH`.
- CSRF: all POST forms must include CSRF token (Flask-WTF or custom token in session).
- Input validation & sanitization: server-side validation for all form fields; sanitize Markdown output.
- File access: validate slugs and never accept raw filesystem paths from users.

---

## 9. Integration Points & Optional Add-ons

- RSS feed generator (script) reading `data/` and outputting `static/rss.xml`.
- Image processing and TTS modules described in `project_memory.md` can be integrated as adapters that write derived files to `static/` or `data/`.
- Background jobs: small worker (RQ/Celery) if needed for expensive processing.

---

## 10. Decision Context & Next Steps

- Decisions taken:

  - Track `data/` in repo (Option A) — `data/README.md` added with guidance.
  - Coverage target standardized to 90% and enforced in CI.
- Recommended next actions:

  - Add `requirements.txt` with pinned versions from docs.
  - Implement `models.Article` with atomic writes and unit tests.
  - Add a minimal `Dockerfile` and `Makefile` or `scripts/` for common tasks.

Save as `docs/TECH-STACK.md` (this file).

v1.0.0 | Active | Last Updated: Dec 16 2025 - 14:30
