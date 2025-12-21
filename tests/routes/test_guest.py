
from app.models.article import Article

def test_guest_index_no_articles(client, tmp_data_dir):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'No articles.' in rv.data

def test_guest_index_with_articles(client, tmp_data_dir):
    # Create published article
    a = Article(slug='published', title='Published Post', excerpt='e', content='c', published=True)
    a.save()
    # Create draft
    d = Article(slug='draft', title='Draft Post', excerpt='e', content='c', published=False)
    d.save()

    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Published Post' in rv.data
    assert b'Draft Post' not in rv.data

def test_article_detail(client, tmp_data_dir):
    a = Article(slug='detail', title='My Detail', excerpt='e', content='**Bold**', published=True)
    a.save()

    rv = client.get('/articles/detail')
    assert rv.status_code == 200
    assert b'My Detail' in rv.data
    # Check simple markdown rendering if implemented? 
    # Current implementation might just dump content or basic render.

def test_article_not_found(client, tmp_data_dir):
    rv = client.get('/articles/non-existent')
    assert rv.status_code == 404
