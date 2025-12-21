class ArticleNotFound(Exception):
    """Raised when an Article cannot be found by slug."""


class ValidationError(Exception):
    """Raised when data validation fails for models or input."""
