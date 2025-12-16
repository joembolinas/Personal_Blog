from app.services import article_service
from app.models.article import Article
from app.models.exceptions import ValidationError


def test_create_publish_unpublish(tmp_path, monkeypatch):
    monkeypatch.setattr('app.models.article.DATA_DIR', tmp_path)

    form = {
        'slug': 'svc-test',
        'title': 'Service Test',
        'excerpt': 'ex',
        'content': 'c',
        'tags': 'a,b',
    }
    a = create_from_form(form)
    assert a.slug == 'svc-test'

    # publish
    p = publish('svc-test')
    assert p.published is True

    # unpublish
    u = unpublish('svc-test')
    assert u.published is False

    # list
    lst = list_articles()
    assert any(x.slug == 'svc-test' for x in lst)
