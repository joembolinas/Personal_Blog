from app.models.exceptions import ArticleNotFound, ValidationError, ArticleNotFound


def test_validation_error_is_exception():
    try:
        raise ValidationError('bad')
    except ValidationError:
        assert True


def test_article_not_found_is_exception():
    try:
        raise ArticleNotFound('slug')
    except ArticleNotFound:
        assert True
