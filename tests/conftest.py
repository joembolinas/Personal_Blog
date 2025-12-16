import os
from pathlib import Path
import pytest

from flask import Flask


@pytest.fixture
def app(tmp_path):
    project_root = Path(__file__).resolve().parents[1]
    app = Flask(__name__, template_folder=str(project_root / 'templates'))
    app.secret_key = 'test-secret'
    # register blueprints lazily to avoid import cycles
    from routes.guest import bp as guest_bp
    from routes.admin import bp as admin_bp
    app.register_blueprint(guest_bp)
    app.register_blueprint(admin_bp)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def tmp_data_dir(monkeypatch, tmp_path):
    # point DATA_DIR to temporary directory for isolation
    monkeypatch.setattr('models.article.DATA_DIR', tmp_path)
    yield tmp_path


@pytest.fixture
def admin_session(client):
    # create a logged-in admin session with csrf token
    with client.session_transaction() as sess:
        sess['admin_authenticated'] = True
        sess['csrf_token'] = 'test-csrf-token'
    return client
