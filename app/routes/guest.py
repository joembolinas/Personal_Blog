from flask import Blueprint, render_template, abort
from app.models.article import Article

bp = Blueprint('guest', __name__)


@bp.route('/')
def index():
    articles = sorted(Article.published_articles(), key=lambda a: a.created_at, reverse=True)
    return render_template('guest/index.html', articles=articles)


@bp.route('/articles/<slug>')
def article_detail(slug):
    try:
        article = Article.load(slug)
        if not article.published:
            abort(404)
    except ArticleNotFound:
        abort(404)
    return render_template('guest/article.html', article=article)
