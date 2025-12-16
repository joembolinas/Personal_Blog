from flask import Blueprint, render_template, abort
from models.article import Article

bp = Blueprint('guest', __name__)


@bp.route('/')
def index():
    articles = sorted(Article.all(), key=lambda a: a.created_at, reverse=True)
    return render_template('guest/index.html', articles=articles)


@bp.route('/articles/<slug>')
def article_detail(slug):
    try:
        article = Article.load(slug)
    except Exception:
        abort(404)
    return render_template('guest/article.html', article=article)
