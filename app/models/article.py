from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json
from typing import List, Dict, Any

from app.models.exceptions import ValidationError, ArticleNotFound
from app.utils.file_ops import atomic_write


DATA_DIR = Path('data') / 'articles'


def _now_iso() -> str:
    return datetime.utcnow().isoformat() + 'Z'


@dataclass
class Article:
    slug: str
    title: str
    excerpt: str
    content: str
    tags: List[str] = field(default_factory=list)
    published: bool = False
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'title': self.title,
            'excerpt': self.excerpt,
            'content': self.content,
            'tags': self.tags,
            'published': self.published,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Article':
        required = ['slug', 'title', 'excerpt', 'content']
        for r in required:
            if r not in data or not data[r]:
                raise ValidationError(f"missing required field: {r}")

        return cls(
            slug=str(data['slug']),
            title=str(data['title']),
            excerpt=str(data['excerpt']),
            content=str(data['content']),
            tags=list(data.get('tags', [])),
            published=bool(data.get('published', False)),
            created_at=data.get('created_at', _now_iso()),
            updated_at=data.get('updated_at', _now_iso()),
        )

    @property
    def _path(self) -> Path:
        return DATA_DIR / f"{self.slug}.json"

    def save(self) -> None:
        self.updated_at = _now_iso()
        data = json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
        atomic_write(self._path, data)

    @classmethod
    def load(cls, slug: str) -> 'Article':
        p = DATA_DIR / f"{slug}.json"
        if not p.exists():
            raise ArticleNotFound(slug)
        try:
            text = p.read_text(encoding='utf-8')
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise ValidationError(f'JSON decode error for {slug}: {e}')
        return cls.from_dict(data)

    def delete(self) -> None:
        p = self._path
        if p.exists():
            p.unlink()
        else:
            raise ArticleNotFound(self.slug)

    @classmethod
    def all(cls) -> List['Article']:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        articles: List[Article] = []
        for p in sorted(DATA_DIR.glob('*.json')):
            try:
                text = p.read_text(encoding='utf-8')
                data = json.loads(text)
                articles.append(cls.from_dict(data))
            except Exception:
                continue
        return articles

    @classmethod
    def published_articles(cls) -> List['Article']:
        return [a for a in cls.all() if a.published]
