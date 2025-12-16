import sys
from pathlib import Path
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app

@pytest.fixture
def app(tmp_path):
    # Use the app factory directly
    app = create_app({
        'TESTING': True,
        'SECRET_KEY': 'test-secret',
        'TEMPLATE_FOLDER': str(Path(__file__).resolve().parents[1] / 'app' / 'templates')
    })
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def tmp_data_dir(monkeypatch, tmp_path):
    # point DATA_DIR to temporary directory for isolation
    monkeypatch.setattr('app.models.article.DATA_DIR', tmp_path)
    yield tmp_path


@pytest.fixture
def admin_session(client):
    # create a logged-in admin session with csrf token
    with client.session_transaction() as sess:
        sess['admin_authenticated'] = True
        sess['csrf_token'] = 'test-csrf-token'
    return client
