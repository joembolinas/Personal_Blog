import pytest
from app.models.exceptions import ArticleNotFound, ValidationError


def test_validation_error_is_exception():
    with pytest.raises(ValidationError):
        raise ValidationError('bad')


def test_article_not_found_is_exception():
    with pytest.raises(ArticleNotFound):
        raise ArticleNotFound('slug')
