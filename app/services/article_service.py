from typing import List, Dict, Any, Optional

from app.models.article import Article
from app.utils.validators import validate_slug, validate_title, normalize_tags
from app.models.exceptions import ValidationError, ArticleNotFound


def create_from_form(form: Dict[str, Any]) -> Article:
    slug = (form.get('slug') or '').strip()
    title = (form.get('title') or '').strip()
    excerpt = (form.get('excerpt') or '').strip()
    content = (form.get('content') or '').strip()
    tags_raw = form.get('tags') or ''
    tags = [t.strip() for t in tags_raw.split(',') if t.strip()]
    tags = normalize_tags(tags)

    if not validate_slug(slug):
        raise ValidationError('invalid slug')
    if not validate_title(title):
        raise ValidationError('invalid title')

    article = Article(slug=slug, title=title, excerpt=excerpt, content=content, tags=tags)
    article.save()
    return article


def save(article: Article) -> None:
    article.save()


def publish(slug: str) -> Article:
    a = Article.load(slug)
    a.published = True
    a.save()
    return a


def unpublish(slug: str) -> Article:
    a = Article.load(slug)
    a.published = False
    a.save()
    return a


def list_articles(sort_by: str = 'created_at', reverse: bool = True) -> List[Article]:
    articles = Article.all()
    # Validate sort_by attribute exists before sorting
    if articles and not hasattr(articles[0], sort_by):
        raise ValidationError(f"Invalid sort_by attribute: {sort_by}")
    
    articles.sort(key=lambda a: getattr(a, sort_by), reverse=reverse)
    return articles
