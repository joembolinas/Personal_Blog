def test_smoke_create_and_view(tmp_data_dir, admin_session):
    client = admin_session

    # create article via admin route
    rv = client.post('/admin/articles/create', data={
        'csrf_token': 'test-csrf-token',
        'slug': 'smoke-1',
        'title': 'Smoke Test',
        'excerpt': 'smoke',
        'content': 'smoke content',
        'tags': 'one,two'
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Smoke Test' in rv.data

    # public index
    r2 = client.get('/')
    assert r2.status_code == 200
    assert b'Smoke Test' in r2.data

    # article detail
    r3 = client.get('/articles/smoke-1')
    assert r3.status_code == 200
    assert b'smoke content' in r3.data
