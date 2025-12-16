from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, abort
import os
from secrets import token_urlsafe

from models.article import Article
from utils.security import check_password, configure_session

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.before_app_request
def _configure():
    # ensure session cookie settings are configured before handling admin requests
    configure_session(current_app)


def _ensure_csrf():
    if 'csrf_token' not in session:
        session['csrf_token'] = token_urlsafe(32)
    return session['csrf_token']


def _verify_csrf(form_token: str) -> bool:
    return bool(form_token and session.get('csrf_token') == form_token)


def login_required(f):
    from functools import wraps

    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get('admin_authenticated'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)

    return wrapped


@bp.route('/login', methods=['GET', 'POST'])
def login():
    _ensure_csrf()
    if request.method == 'POST':
        form_csrf = request.form.get('csrf_token')
        if not _verify_csrf(form_csrf):
            abort(400)
        pw = request.form.get('password', '')
        admin_hash = os.environ.get('ADMIN_PASSWORD_HASH')
        if not admin_hash:
            abort(500)
        if check_password(admin_hash, pw):
            session['admin_authenticated'] = True
            return redirect(url_for('admin.dashboard'))
        return render_template('admin/login.html', error='Invalid credentials', csrf_token=session.get('csrf_token'))
    return render_template('admin/login.html', csrf_token=session.get('csrf_token'))


@bp.route('/logout')
def logout():
    session.pop('admin_authenticated', None)
    return redirect(url_for('admin.login'))


@bp.route('/')
@login_required
def dashboard():
    articles = sorted(Article.all(), key=lambda a: a.created_at, reverse=True)
    return render_template('admin/dashboard.html', articles=articles)


@bp.route('/articles/create', methods=['GET', 'POST'])
@login_required
def create_article():
    _ensure_csrf()
    if request.method == 'POST':
        if not _verify_csrf(request.form.get('csrf_token')):
            abort(400)
        slug = request.form.get('slug')
        title = request.form.get('title')
        excerpt = request.form.get('excerpt')
        content = request.form.get('content')
        tags = [t.strip() for t in (request.form.get('tags') or '').split(',') if t.strip()]
        a = Article(slug=slug, title=title, excerpt=excerpt, content=content, tags=tags)
        a.save()
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/article_form.html', csrf_token=session.get('csrf_token'))


@bp.route('/articles/<slug>/publish', methods=['POST'])
@login_required
def publish_article(slug):
    if not _verify_csrf(request.form.get('csrf_token')):
        abort(400)
    try:
        a = Article.load(slug)
    except Exception:
        abort(404)
    a.published = True
    a.save()
    return redirect(url_for('admin.dashboard'))
