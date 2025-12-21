import re
from typing import List


SLUG_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def validate_slug(s: str) -> bool:
    if not s or not isinstance(s, str):
        return False
    return bool(SLUG_RE.match(s))


def validate_title(s: str) -> bool:
    if not s or not isinstance(s, str):
        return False
    return 1 <= len(s.strip()) <= 200


def normalize_tags(tags: List[str]) -> List[str]:
    out = []
    for t in tags or []:
        if not isinstance(t, str):
            continue
        tx = t.strip().lower()
        if tx:
            out.append(tx)
    return sorted(dict.fromkeys(out))
