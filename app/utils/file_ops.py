from pathlib import Path
import tempfile
from typing import Union


def atomic_write(path: Union[str, Path], data: Union[bytes, str], tmp_suffix: str = '.tmp') -> None:
    """Atomically write data to `path` by writing to a temporary file
    in the same directory and replacing the target path.

    - `data` may be bytes or string. Strings are encoded as UTF-8.
    - Ensures parent directory exists.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(data, str):
        write_bytes = data.encode('utf-8')
    else:
        write_bytes = data

    fd, tmp_path = tempfile.mkstemp(suffix=tmp_suffix, dir=str(p.parent))
    try:
        with open(fd, 'wb') as f:
            f.write(write_bytes)
        tmp_p = Path(tmp_path)
        tmp_p.replace(p)
    finally:
        try:
            tp = Path(tmp_path)
            if tp.exists():
                tp.unlink()
        except Exception:
            pass
