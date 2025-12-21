import os
from flask import Flask

from app.routes.admin import bp as admin_bp
from app.utils.security import hash_password
from app.models.article import Article


def test_admin_login_and_create_article(client, monkeypatch, tmp_path):
    # set admin password hash
    os.environ['ADMIN_PASSWORD_HASH'] = hash_password('secret')

    # isolate data dir (already done by conftest if we used tmp_data_dir, but explicit is fine)
    # Actually, let's use the explicit one here to align with existing test logic
    monkeypatch.setattr('app.models.article.DATA_DIR', tmp_path)


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
