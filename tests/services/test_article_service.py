def test_create_publish_unpublish(tmp_path, monkeypatch):
    monkeypatch.setattr('app.models.article.DATA_DIR', tmp_path)

    form = {
        'slug': 'svc-test',
        'title': 'Service Test',
        'excerpt': 'ex',
        'content': 'c',
        'tags': 'a,b',
    }
    a = article_service.create_from_form(form)
    assert a.slug == 'svc-test'

    # publish
    p = article_service.publish('svc-test')
    assert p.published is True

    # unpublish
    u = article_service.unpublish('svc-test')
    assert u.published is False

    # list
    lst = article_service.list_articles()
    assert any(x.slug == 'svc-test' for x in lst)
