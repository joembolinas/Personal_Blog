from pathlib import Path

from utils.file_ops import atomic_write


def test_atomic_write_creates_file(tmp_path):
    target = tmp_path / 'out.txt'
    atomic_write(target, 'hello world')
    assert target.exists()
    assert target.read_text(encoding='utf-8') == 'hello world'


def test_atomic_write_overwrites(tmp_path):
    target = tmp_path / 'out.txt'
    atomic_write(target, 'first')
    atomic_write(target, 'second')
    assert target.read_text(encoding='utf-8') == 'second'
