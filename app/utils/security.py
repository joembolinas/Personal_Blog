import os
import hashlib
import secrets
from typing import Tuple


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-HMAC-SHA256 with a random salt.

    Returns: salt$hexdigest
    """
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 600_000)
    return f"{salt}${dk.hex()}"


def check_password(stored: str, password: str) -> bool:
    """Verify a password against stored `salt$hexdigest` format."""
    try:
        salt, hexd = stored.split('$', 1)
    except ValueError:
        return False
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100_000)
    return secrets.compare_digest(dk.hex(), hexd)


def configure_session(app) -> None:
    """Harden session cookie settings for production environments.

    - `SESSION_COOKIE_HTTPONLY` is enabled
    - `SESSION_COOKIE_SAMESITE` defaults to 'Lax'
    - `SESSION_COOKIE_SECURE` enabled when running in production
    """
    app.config.setdefault('SESSION_COOKIE_HTTPONLY', True)
    app.config.setdefault('SESSION_COOKIE_SAMESITE', 'Lax')
    env = os.environ.get('FLASK_ENV') or app.config.get('ENV')
    secure = True if env == 'production' else False
    app.config.setdefault('SESSION_COOKIE_SECURE', secure)
