---
title: Logical Design Exemplars
version: 1.0
date_created: 2025-12-16
last_updated: 2025-12-16
owner: Personal Blog Project Team
---

# Logical Design Exemplars — Patterns & Examples

Purpose: provide compact, copy-ready examples for component structure, service layer, API handlers, error handling, state management, and testing patterns aligned with the project's Flask + filesystem tech stack.

Notes: adapt these examples to `models.py`, `routes/`, and `utils/` per repository conventions.

---

## 1) Component Structure (Blueprints + modules)

Recommended layout (small excerpt):

- `app.py` — application factory
- `routes/guest.py` — public blueprint
- `routes/admin.py` — admin blueprint (url_prefix `/admin`)
- `models.py` — `Article` model
- `services/article_service.py` — business logic (service layer)
- `utils/file_ops.py`, `utils/validators.py`

Example `routes/admin.py` (structure only):

```python
from flask import Blueprint, render_template, request, redirect, flash, url_for
from services.article_service import ArticleService

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/articles/new', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        data = request.form.to_dict()
        article = ArticleService.create_from_form(data)
        ArticleService.save(article)
        flash('Article created', 'success')
        return redirect(url_for('admin.edit_article', slug=article.slug))
    return render_template('admin/create.html')
```

Keep route handlers thin — delegate validation and persistence to `services` and `models`.

---

## 2) Service Layer (separation of business logic)

Why: centralizes validation, normalization, and complex operations so `routes` remain simple and testable.

Example `services/article_service.py`:

```python
from models import Article
from utils.validators import validate_article_data
from datetime import datetime

class ArticleService:
    @staticmethod
    def create_from_form(data: dict) -> Article:
        validate_article_data(data)
        now = datetime.utcnow().isoformat()
        return Article(
            slug=data['slug'],
            title=data['title'].strip(),
            content=data.get('content',''),
            excerpt=data.get('excerpt',''),
            author=data.get('author',''),
            created_at=now,
            updated_at=now,
            published=bool(data.get('published', False)),
            tags=data.get('tags', [])
        )

    @staticmethod
    def save(article: Article) -> None:
        # business rules (e.g., update timestamps)
        article.updated_at = datetime.utcnow().isoformat()
        article.save()  # delegates to models.Article.save

    @staticmethod
    def publish(slug: str) -> Article:
        a = Article.load(slug)
        if a is None:
            raise ArticleNotFound(slug)
        a.published = True
        ArticleService.save(a)
        return a

class ArticleNotFound(Exception):
    pass
```

Service methods return domain objects or raise domain-specific exceptions for routes to catch and translate into HTTP responses.

---

## 3) API Calls (REST-style endpoints)

Pattern: provide both HTML routes and JSON API endpoints. Keep JSON API stateless and authenticated with token or session.

Example JSON endpoint in `routes/guest.py`:

```python
from flask import Blueprint, jsonify
from models import Article

guest_bp = Blueprint('guest', __name__)

@guest_bp.route('/api/articles', methods=['GET'])
def api_list_articles():
    articles = Article.all()
    summaries = [a.to_dict() for a in articles if a.published]
    return jsonify(summaries)

@guest_bp.route('/api/articles/<slug>', methods=['GET'])
def api_get_article(slug):
    a = Article.load(slug)
    if a is None or not a.published:
        return jsonify({'error': 'not found'}), 404
    return jsonify(a.to_dict())
```

For admin API endpoints, require session auth or token and return appropriate status codes.

---

## 4) Error Handling (exceptions & handlers)

Pattern: define domain exceptions, raise in service/model, centralize HTTP mapping in `app.py`.

Example `errors.py` (domain exceptions):

```python
class ArticleError(Exception):
    pass

class ArticleNotFound(ArticleError):
    def __init__(self, slug):
        super().__init__(f'Article not found: {slug}')

class ValidationError(ArticleError):
    def __init__(self, errors):
        super().__init__('Validation failed')
        self.errors = errors
```

Register HTTP handlers in `app.py`:

```python
from flask import jsonify
from errors import ArticleNotFound, ValidationError

@app.errorhandler(ArticleNotFound)
def handle_not_found(e):
    return jsonify({'error': str(e)}), 404

@app.errorhandler(ValidationError)
def handle_validation(e):
    return jsonify({'error': 'validation', 'details': e.errors}), 400

@app.errorhandler(Exception)
def handle_generic(e):
    app.logger.exception('Unhandled exception')
    return jsonify({'error': 'internal error'}), 500
```

Prefer explicit domain exceptions to avoid leaking internal traces to clients. Log full trace server-side.

---

## 5) State Management (server + minimal client)

Server-side state
- Use Flask `session` for admin auth state (small, signed cookies). Keep secrets in env `SECRET_KEY`.
- Avoid storing large state in session; persist in `data/`.

Example login flow (session):

```python
from flask import session

def login_user(username):
    session['user'] = username

def logout_user():
    session.pop('user', None)

def current_user():
    return session.get('user')
```

Client-side state
- Minimal vanilla JS for UI interactions (prefetch, local edits). Example: preview editor state stored in `localStorage`.

```html
<script>
  const draftKey = 'article:draft'
  const editor = document.querySelector('#content')
  editor.addEventListener('input', () => {
    localStorage.setItem(draftKey, editor.value)
  })
  // restore
  editor.value = localStorage.getItem(draftKey) || ''
</script>
```

For rich apps, introduce a small state module; for this project keep client-side JS minimal.

---

## 6) Testing Patterns (pytest examples)

Principles
- Use fixtures for `app`, `client`, and `tmp_data_dir` to isolate file I/O.
- Test models and services with unit tests; test routes with Flask test client in integration tests.
- Aim to mock expensive operations where appropriate and assert side effects on `data/` files.

Example `tests/conftest.py` (minimal):

```python
import pytest
from app import create_app
from pathlib import Path

@pytest.fixture
def tmp_data_dir(tmp_path, monkeypatch):
    d = tmp_path / 'data'
    d.mkdir()
    monkeypatch.setenv('DATA_DIR', str(d))
    yield d

@pytest.fixture
def app(tmp_data_dir):
    app = create_app({'TESTING': True})
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
```

Unit test example for `Article` (`tests/unit/test_models.py`):

```python
def test_article_save_load(tmp_data_dir):
    from models import Article
    a = Article(slug='hello-world', title='Hello', content='x')
    a.save()
    b = Article.load('hello-world')
    assert b is not None
    assert b.title == 'Hello'
```

Integration test example for routes (`tests/integration/test_routes.py`):

```python
def test_guest_list(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b'Articles' in res.data
```

Coverage and CI
- Run `pytest --cov=.` and assert coverage >= 90% in CI via `--cov-fail-under=90`.

---

## 7) Quick mapping: file → responsibility

- `models.py` — domain, serialization, atomic file writes
- `services/` — business rules, validation orchestration
- `routes/` — HTTP handlers, minimal orchestration
- `utils/` — helpers (slugify, atomic write, sanitization)
- `tests/` — unit and integration tests with fixtures

---

## Next steps (recommended)

1. Implement `services/article_service.py` and unit tests for each method.
2. Implement domain exceptions and register error handlers in `app.py`.
3. Add `tests/conftest.py` and write coverage-focused tests for `models` and `services`.

v1.0.0 | Active | Last Updated: Dec 16 2025 - 14:30
