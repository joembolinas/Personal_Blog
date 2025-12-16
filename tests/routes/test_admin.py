import os
from flask import Flask

from routes.admin import bp as admin_bp
from utils.security import hash_password
from models.article import Article


def make_app():
    from pathlib import Path
    project_root = Path(__file__).resolve().parents[2]
    app = Flask(__name__, template_folder=str(project_root / 'templates'))
    app.secret_key = 'test-secret'
    app.register_blueprint(admin_bp)
    return app


def test_admin_login_and_create_article(tmp_path, monkeypatch):
    # set admin password hash
    os.environ['ADMIN_PASSWORD_HASH'] = hash_password('secret')

    # isolate data dir
    monkeypatch.setattr('models.article.DATA_DIR', tmp_path)

    app = make_app()
    client = app.test_client()

    # GET login to obtain CSRF (session cookie)
    rv = client.get('/admin/login')
    assert rv.status_code == 200
    # naive extraction: look for csrf_token value in html
    body = rv.data.decode('utf-8')
    start = body.find('name="csrf_token" value="')
    assert start != -1
    start += len('name="csrf_token" value="')
    end = body.find('"', start)
    token = body[start:end]

    # POST login
    rv2 = client.post('/admin/login', data={'csrf_token': token, 'password': 'secret'}, follow_redirects=True)
    assert b'Admin Dashboard' in rv2.data

    # create article
    rv3 = client.get('/admin/articles/create')
    assert rv3.status_code == 200
    body3 = rv3.data.decode('utf-8')
    start = body3.find('name="csrf_token" value="')
    start += len('name="csrf_token" value="')
    end = body3.find('"', start)
    token2 = body3[start:end]

    rv4 = client.post('/admin/articles/create', data={
        'csrf_token': token2,
        'slug': 'admintest',
        'title': 'Admin Test',
        'excerpt': 'ex',
        'content': 'content',
        'tags': 'one,two'
    }, follow_redirects=True)
    assert b'Admin Dashboard' in rv4.data

    # verify article exists
    a = Article.load('admintest')
    assert a.title == 'Admin Test'
