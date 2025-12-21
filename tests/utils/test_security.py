
import pytest
from app.utils.security import hash_password, check_password, configure_session

def test_hash_password():
    """Test that hashing returns a valid format and is random."""
    pw = "secret"
    hashed = hash_password(pw)
    assert "$" in hashed
    assert len(hashed.split("$")) == 2
    
    # Hashes should be unique due to salt
    hashed2 = hash_password(pw)
    assert hashed != hashed2
    
def test_check_password():
    """Test verification of passwords."""
    pw = "my-password"
    hashed = hash_password(pw)
    
    assert check_password(hashed, pw) is True
    assert check_password(hashed, "wrong-password") is False
    assert check_password("malformed", pw) is False

def test_configure_session():
    """Test session hardening options."""
    class MockApp:
        def __init__(self, env):
            self.config = {'ENV': env}
    
    # Test development
    app_dev = MockApp('development')
    configure_session(app_dev)
    assert app_dev.config['SESSION_COOKIE_HTTPONLY'] == True
    assert app_dev.config['SESSION_COOKIE_SAMESITE'] == 'Lax'
    assert app_dev.config['SESSION_COOKIE_SECURE'] == False
    
    # Test production
    app_prod = MockApp('production')
    configure_session(app_prod)
    assert app_prod.config['SESSION_COOKIE_SECURE'] == True
