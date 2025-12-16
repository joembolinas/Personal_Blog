from utils.validators import validate_slug, validate_title, normalize_tags


def test_validate_slug():
    assert validate_slug('hello-world')
    assert validate_slug('a1')
    assert not validate_slug('Hello')
    assert not validate_slug('bad slug')
    assert not validate_slug('')


def test_validate_title():
    assert validate_title('A good title')
    assert not validate_title('')
    assert not validate_title('   ')


def test_normalize_tags():
    tags = ['One', ' two ', 'one', '', None]
    assert normalize_tags(tags) == ['one', 'two']
