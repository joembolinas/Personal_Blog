from app.models.article import Article
from app.models.exceptions import ValidationError, ArticleNotFound


def test_article_save_load_delete(tmp_path, monkeypatch):
    monkeypatch.setattr('app.models.article.DATA_DIR', tmp_path)

    a = Article(slug='test-slug', title='Title', excerpt='Ex', content='Content')
    a.save()

    loaded = Article.load('test-slug')
    assert loaded.slug == 'test-slug'
    assert loaded.title == 'Title'

    loaded.delete()
    try:
        Article.load('test-slug')
        assert False, 'should have raised ArticleNotFound'
    except ArticleNotFound:
        assert True


def test_article_missing_fields_raises():
    bad = {'slug': 's', 'title': '', 'excerpt': 'e', 'content': 'c'}
    try:
        Article.from_dict(bad)
        assert False, 'should raise ValidationError'
    except ValidationError:
        assert True
