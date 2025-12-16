# AGENT.md - AI Assistant Context for Personal Blog

> **Universal AI Assistant Guide**
> Compatible with: GitHub Copilot, Cursor, Claude Code, Gemini Code, GPT-Codex, and other AI coding assistants

---

## 📋 Project Overview

**Personal Blog** is a lightweight, filesystem-based content management system for publishing articles. Built with Python Flask, it demonstrates clean architecture principles while maintaining simplicity.

### Key Characteristics

- **Type**: Web Application (Blog CMS)
- **Language**: Python 3.8+
- **Framework**: Flask 3.0
- **Storage**: Filesystem (JSON + Markdown)
- **Architecture**: MVC pattern (simplified)
- **Authentication**: Session-based (admin only)
- **Frontend**: Server-rendered HTML + Vanilla CSS

### Project Goals

1. Simple article publishing without database complexity
2. Clean separation between public and admin interfaces
3. Filesystem-based content that's easy to backup and version
4. Minimal dependencies and straightforward deployment

---

## 🏗️ Architecture & Structure

### Directory Layout

```
personal-blog/
│
├── .github/                    # GitHub-specific configurations
│   ├── copilot_instructions/  # Custom Copilot instructions
│   ├── copilot_agents/        # Specialized agents
│   ├── prompts/               # Reusable prompt templates
│   └── collections/           # File groupings for context
│
├── data/                      # Article storage (JSON files)
│   └── *.json                # Individual article files
│
├── routes/                    # Route handlers (Blueprints)
│   ├── __init__.py
│   ├── guest.py              # Public-facing routes
│   └── admin.py              # Admin panel routes
│
├── templates/                 # Jinja2 HTML templates
│   ├── base.html             # Base template (guest)
│   ├── guest/                # Public templates
│   │   ├── index.html       # Article listing
│   │   └── article.html     # Single article view
│   └── admin/                # Admin templates
│       ├── base.html         # Admin base template
│       ├── login.html        # Authentication
│       ├── dashboard.html    # Article management
│       ├── create.html       # New article form
│       └── edit.html         # Edit article form
│
├── static/                    # Static assets
│   ├── css/
│   │   ├── guest.css         # Public site styling
│   │   └── admin.css         # Admin panel styling
│   └── images/               # Site images
│
├── utils/                     # Helper modules
│   ├── __init__.py
│   ├── validators.py         # Input validation
│   └── auth.py               # Authentication helpers
│
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_routes.py
│   └── conftest.py           # Pytest fixtures
│
├── app.py                     # Application entry point
├── models.py                  # Data models
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── AGENT.md                  # This file
└── README.md                 # User-facing documentation
```

### Architecture Pattern

**Model-View-Controller (Simplified)**

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│      Flask Routes           │
│    (Controller Layer)       │
│  • guest.py - Public        │
│  • admin.py - Management    │
└──────┬──────────────────────┘
       │
       ├──────────────────┐
       ▼                  ▼
┌─────────────┐    ┌─────────────┐
│   Models    │    │  Templates  │
│ (Data Layer)│    │ (View Layer)│
│             │    │             │
│ • Article   │    │ • Jinja2    │
│ • File I/O  │    │ • HTML      │
└──────┬──────┘    └─────────────┘
       │
       ▼
┌─────────────┐
│ Filesystem  │
│ data/*.json │
└─────────────┘
```

---

## 🔧 Technology Stack Details

### Core Dependencies

```python
Flask==3.0.0              # Web framework
python-dotenv==1.0.0      # Environment variable management
markdown2==2.4.10         # Markdown to HTML conversion
```

### Development Dependencies

```python
pytest==7.4.3             # Testing framework
pytest-cov==4.1.0         # Test coverage
flake8==6.1.0             # Linting
mypy==1.7.0               # Static type checking
```

### No External Database

Articles are stored as JSON files in the `data/` directory:

- **Pros**: Simple, portable, version-controllable, no setup required
- **Cons**: Not suitable for high-traffic sites or complex queries
- **Use Case**: Personal blogs, small documentation sites, prototypes

---

## 📊 Data Models

### Article Schema

```python
{
    "slug": str,           # URL-friendly identifier (unique)
    "title": str,          # Article title (required)
    "content": str,        # Markdown content (required)
    "excerpt": str,        # Short summary (optional)
    "author": str,         # Author name (default: "Admin")
    "published": bool,     # Publication status
    "tags": List[str],     # Category tags
    "created_at": str,     # ISO 8601 timestamp
    "updated_at": str      # ISO 8601 timestamp
}
```

### Article Class Interface

```python
class Article:
    """Blog article with filesystem persistence."""
  
    def __init__(self, title: str, content: str, **kwargs) -> None:
        """Initialize article with title and content."""
        pass
  
    def to_dict(self) -> Dict[str, Any]:
        """Serialize article to dictionary."""
        pass
  
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Article':
        """Deserialize article from dictionary."""
        pass
  
    def save(self) -> None:
        """Persist article to filesystem."""
        pass
  
    def delete(self) -> None:
        """Remove article from filesystem."""
        pass
  
    @classmethod
    def load(cls, slug: str) -> Optional['Article']:
        """Load article by slug."""
        pass
  
    @classmethod
    def all(cls) -> List['Article']:
        """Get all articles."""
        pass
  
    @classmethod
    def published_articles(cls) -> List['Article']:
        """Get only published articles."""
        pass
```

### File Naming Convention

- **Pattern**: `data/{slug}.json`
- **Example**: `data/getting-started-with-python.json`
- **Slug Generation**: Lowercase, alphanumeric + hyphens, unique

---

## 🎯 Coding Standards

### Python Style Guide (PEP 8+)

#### General Rules

```python
# Maximum line length
MAX_LINE_LENGTH = 88  # Black formatter standard

# Import organization
import stdlib_module
from stdlib_module import something

import third_party
from third_party import another

import local_module
from local_module import custom
```

#### Type Hints (Required)

```python
from typing import Optional, List, Dict, Any

def process_article(
    slug: str, 
    data: Dict[str, Any]
) -> Optional[Article]:
    """
    Process and validate article data.
  
    Args:
        slug: Article identifier
        data: Raw article data
    
    Returns:
        Article instance or None if invalid
    """
    pass
```

#### Docstrings (Google Style)

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
  
    Longer description if needed. Explain the purpose,
    behavior, and any important considerations.
  
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When input is invalid
        FileNotFoundError: When file doesn't exist
    
    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

#### Error Handling

```python
# Always use specific exceptions
try:
    with open(file_path, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    return None
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON in {file_path}: {e}")
    return None
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise
```

#### Context Managers

```python
# Use pathlib and context managers
from pathlib import Path

def read_file(filename: str) -> str:
    """Read file contents safely."""
    file_path = Path('data') / filename
  
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
```

### HTML/CSS Standards

#### Semantic HTML5

```html
<!-- Good: Semantic structure -->
<article class="blog-post">
    <header class="blog-post__header">
        <h1 class="blog-post__title">Article Title</h1>
        <time class="blog-post__date" datetime="2024-01-15">
            January 15, 2024
        </time>
    </header>
  
    <section class="blog-post__content">
        <!-- Content -->
    </section>
  
    <footer class="blog-post__footer">
        <nav class="blog-post__tags">
            <!-- Tags -->
        </nav>
    </footer>
</article>

<!-- Bad: Non-semantic -->
<div class="post">
    <div class="header">
        <div class="title">Article Title</div>
        <div class="date">January 15, 2024</div>
    </div>
</div>
```

#### BEM CSS Naming

```css
/* Block */
.article-card { }

/* Element */
.article-card__title { }
.article-card__excerpt { }
.article-card__meta { }

/* Modifier */
.article-card--featured { }
.article-card__title--large { }

/* State */
.article-card.is-loading { }
.article-card.is-hidden { }
```

#### Responsive Design (Mobile-First)

```css
/* Base styles (mobile) */
.container {
    padding: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
    .container {
        padding: 2rem;
    }
}

/* Desktop */
@media (min-width: 1024px) {
    .container {
        max-width: 1200px;
        margin: 0 auto;
    }
}
```

---

## 🔒 Security Requirements

### Authentication

```python
# Session-based authentication
from flask import session

def login_required(f):
    """Decorator to protect admin routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function
```

### CSRF Protection

```html
<!-- All forms must include CSRF token -->
<form method="POST" action="{{ url_for('admin.create') }}">
    <input type="hidden" 
           name="csrf_token" 
           value="{{ csrf_token() }}"/>
  
    <!-- Form fields -->
</form>
```

### Input Validation

```python
def validate_article_input(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate article form data.
  
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
  
    # Required fields
    if not data.get('title', '').strip():
        errors.append('Title is required')
  
    if not data.get('content', '').strip():
        errors.append('Content is required')
  
    # Length limits
    if len(data.get('title', '')) > 200:
        errors.append('Title must be under 200 characters')
  
    # Sanitization
    title = bleach.clean(data.get('title', ''))
  
    return len(errors) == 0, errors
```

### Environment Variables

```python
# .env file (not committed to Git)
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=hashed-password
FLASK_ENV=development
DEBUG=True
```

```python
# Loading in app.py
from dotenv import load_dotenv
import os

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'
```

---

## 🚀 Common Development Tasks

### Task 1: Creating a New Route

**Pattern:**

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Define blueprint
blueprint_name = Blueprint('name', __name__, url_prefix='/prefix')

@blueprint_name.route('/path', methods=['GET', 'POST'])
def handler_name():
    """
    Brief description of what this route does.
  
    Returns:
        Rendered template or redirect
    """
    if request.method == 'POST':
        # 1. Get form data
        data = request.form.to_dict()
    
        # 2. Validate
        is_valid, errors = validate_input(data)
        if not is_valid:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('current_route'))
    
        # 3. Process
        try:
            # Business logic here
            article = Article(**data)
            article.save()
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('current_route'))
    
        # 4. Success feedback
        flash('Operation successful', 'success')
        return redirect(url_for('next_route'))
  
    # GET request
    context = {
        'key': 'value'
    }
    return render_template('template.html', **context)
```

### Task 2: Creating a Template

**Pattern:**

```html
{% extends "base.html" %}

{% block title %}Page Title - Personal Blog{% endblock %}

{% block extra_head %}
<!-- Page-specific CSS/meta tags -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/page.css') }}">
{% endblock %}

{% block content %}
<main class="container">
    <header class="page-header">
        <h1>Page Heading</h1>
    </header>
  
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
  
    <section class="content">
        <!-- Main content -->
        {% if items %}
            {% for item in items %}
                <article class="item">
                    <h2>{{ item.title }}</h2>
                    <p>{{ item.excerpt }}</p>
                </article>
            {% endfor %}
        {% else %}
            <p class="empty-state">No items found.</p>
        {% endif %}
    </section>
</main>
{% endblock %}

{% block scripts %}
<!-- Page-specific JavaScript -->
<script>
    // Minimal, progressive enhancement only
</script>
{% endblock %}
```

### Task 3: Writing Tests

**Pattern:**

```python
import pytest
from pathlib import Path
from models import Article

@pytest.fixture
def sample_article_data():
    """Provide sample article data for tests."""
    return {
        'title': 'Test Article',
        'content': '# Test Content',
        'published': True,
        'tags': ['test', 'sample']
    }

@pytest.fixture
def article(sample_article_data):
    """Create and cleanup test article."""
    article = Article(**sample_article_data)
    article.save()
  
    yield article
  
    # Cleanup
    article.delete()

def test_article_creation(sample_article_data):
    """Test creating a new article."""
    article = Article(**sample_article_data)
  
    assert article.title == 'Test Article'
    assert article.published is True
    assert 'test' in article.tags
  
def test_article_save_and_load(article):
    """Test persisting and loading article."""
    loaded = Article.load(article.slug)
  
    assert loaded is not None
    assert loaded.title == article.title
    assert loaded.content == article.content

def test_article_not_found():
    """Test loading non-existent article."""
    article = Article.load('non-existent-slug')
  
    assert article is None

def test_all_published_articles(article):
    """Test retrieving published articles."""
    # Create unpublished article
    draft = Article(title='Draft', content='Content', published=False)
    draft.save()
  
    published = Article.published_articles()
  
    assert len(published) == 1
    assert published[0].slug == article.slug
  
    # Cleanup
    draft.delete()
```

### Task 4: Adding Validation

**Pattern:**

```python
from typing import Dict, List, Tuple, Any
import re

def validate_slug(slug: str) -> bool:
    """
    Check if slug format is valid.
  
    Args:
        slug: String to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
    return bool(re.match(pattern, slug))

def validate_article_data(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate article form data comprehensively.
  
    Args:
        data: Dictionary containing form fields
    
    Returns:
        Tuple of (is_valid, list_of_error_messages)
    """
    errors = []
  
    # Title validation
    title = data.get('title', '').strip()
    if not title:
        errors.append('Title is required')
    elif len(title) < 3:
        errors.append('Title must be at least 3 characters')
    elif len(title) > 200:
        errors.append('Title must be less than 200 characters')
  
    # Content validation
    content = data.get('content', '').strip()
    if not content:
        errors.append('Content is required')
    elif len(content) < 10:
        errors.append('Content must be at least 10 characters')
  
    # Excerpt validation (optional but limited)
    excerpt = data.get('excerpt', '').strip()
    if excerpt and len(excerpt) > 500:
        errors.append('Excerpt must be less than 500 characters')
  
    # Tags validation
    tags = data.get('tags', [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',') if t.strip()]
  
    if len(tags) > 10:
        errors.append('Maximum 10 tags allowed')
  
    for tag in tags:
        if len(tag) > 50:
            errors.append(f'Tag "{tag}" is too long (max 50 chars)')
  
    # Slug validation (if provided)
    slug = data.get('slug', '').strip()
    if slug and not validate_slug(slug):
        errors.append('Slug must contain only lowercase letters, numbers, and hyphens')
  
    return len(errors) == 0, errors
```

---

## 🎨 UI/UX Guidelines

### Design Principles

1. **Simplicity First**: Clean, uncluttered interface
2. **Readability**: Typography optimized for long-form content
3. **Accessibility**: WCAG 2.1 AA compliance
4. **Responsiveness**: Mobile-first approach
5. **Performance**: Minimal CSS, no heavy frameworks

### Color Palette Example

```css
:root {
    /* Primary colors */
    --color-primary: #3498db;
    --color-primary-dark: #2980b9;
    --color-primary-light: #5dade2;
  
    /* Neutral colors */
    --color-text: #2c3e50;
    --color-text-light: #7f8c8d;
    --color-background: #ffffff;
    --color-background-alt: #ecf0f1;
  
    /* Semantic colors */
    --color-success: #27ae60;
    --color-error: #e74c3c;
    --color-warning: #f39c12;
    --color-info: #3498db;
  
    /* Spacing system */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 2rem;
    --spacing-xl: 4rem;
}
```

### Typography

```css
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 
                 Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: var(--color-text);
}

/* Headings */
h1 { font-size: 2.5rem; font-weight: 700; line-height: 1.2; }
h2 { font-size: 2rem; font-weight: 600; line-height: 1.3; }
h3 { font-size: 1.5rem; font-weight: 600; line-height: 1.4; }

/* Reading content */
.article-content {
    max-width: 70ch;  /* Optimal reading width */
    font-size: 1.125rem;
    line-height: 1.8;
}
```

---

## 🛠️ Development Workflow

### 1. Environment Setup

```bash
# Clone repository
git clone <repository-url>
cd personal-blog

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your settings

# Create data directory
mkdir -p data

# Run application
python app.py
```

### 2. Development Cycle

```bash
# 1. Create feature branch
git checkout -b feature/article-search

# 2. Make changes
# ... code ...

# 3. Run tests
pytest tests/ -v

# 4. Check code quality
flake8 *.py routes/ utils/
mypy *.py

# 5. Commit changes
git add .
git commit -m "feat: Add article search functionality"

# 6. Push and create PR
git push origin feature/article-search
```

### 3. Testing Workflow

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py -v

# Run with coverage
pytest --cov=. tests/

# Generate HTML coverage report
pytest --cov=. --cov-report=html tests/

# Run only failed tests
pytest --lf tests/
```

---

## 🐛 Troubleshooting Guide

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

#### Issue: Article not showing on homepage

**Checklist:**

1. Is `published` set to `true` in JSON file?
2. Is JSON file in `data/` directory?
3. Is filename format correct: `{slug}.json`?
4. Is JSON valid? Check with `python -m json.tool data/article.json`

**Debug:**

```python
# Add to route handler
articles = Article.all()
print(f"Total articles: {len(articles)}")

published = Article.published_articles()
print(f"Published articles: {len(published)}")
```

#### Issue: Template not found error

**Solution:**

```python
# Check template path
# ✅ Correct
render_template('guest/index.html')

# ❌ Wrong
render_template('/guest/index.html')  # No leading slash
render_template('templates/guest/index.html')  # No 'templates' prefix
```

#### Issue: Static files not loading

**Check:**

```html
<!-- ✅ Correct -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/guest.css') }}">

<!-- ❌ Wrong -->
<link rel="stylesheet" href="/static/css/guest.css">
```

#### Issue: CSRF token error on form submission

**Solution:**

```html
<!-- Ensure form includes token -->
<form method="POST">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    <!-- form fields -->
</form>
```

```python
# In app.py, ensure CSRFProtect is configured
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
csrf = CSRFProtect(app)
```

---

## 📚 Quick Reference

### Flask Route Examples

```python
# GET only
@app.route('/about')
def about():
    return render_template('about.html')

# Multiple methods
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form
        pass
    return render_template('contact.html')

# URL parameters
@app.route('/article/<slug>')
def article(slug):
    return render_template('article.html', slug=slug)

# Query parameters
@app.route('/search')
def search():
    query = request.args.get('q', '')
    return render_template('search.html', query=query)
```

### Jinja2 Template Syntax

```html
<!-- Variables -->
{{ variable }}
{{ variable | e }}  <!-- Escape HTML -->
{{ variable | default('N/A') }}

<!-- Filters -->
{{ article.created_at | datetime }}
{{ article.content | markdown }}
{{ text | truncate(100) }}

<!-- Conditionals -->
{% if condition %}
    <!-- content -->
{% elif other_condition %}
    <!-- content -->
{% else %}
    <!-- content -->
{% endif %}

<!-- Loops -->
{% for item in items %}
    {{ item.name }}
{% else %}
    No items found
{% endfor %}

<!-- Template inheritance -->
{% extends "base.html" %}
{% block content %}
    <!-- Override content -->
{% endblock %}

<!-- Include partial -->
{% include "partials/header.html" %}
```

### File Operations

```python
from pathlib import Path
import json

# Read JSON
def read_json(filepath: Path) -> dict:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

# Write JSON
def write_json(filepath: Path, data: dict) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# List files
def list_json_files(directory: Path) -> List[Path]:
    return list(directory.glob('*.json'))

# Check if file exists
def file_exists(filepath: Path) -> bool:
    return filepath.exists() and filepath.is_file()
```

---

## 🤖 AI Assistant Integration

### 1. GitHub Copilot

Primary configuration in VS. CODE  `.github/COPILOT-INSTRCTIONS.md`

**Usage:**

```
@blog-agent Create a route for displaying featured articles
```

### 2. Gemini Code

GEMINI-CLI, ANTIGRAVITY, GOOGLE CLAUDE CODE Looks for AGENT.md and `GEMINI.md`

**Usage:**

```
Following the patterns in AGENT.md, generate admin dashboard route
```

### Universal Prompts

These work across all AI assistants:

1. **"Create a Flask route for [feature] following this project's patterns"**
2. **"Generate tests for [component] using pytest"**
3. **"Build a template for [page] with BEM CSS naming"**
4. **"Add validation for [field] following security guidelines"**
5. **"Review this code for errors and suggest improvements"**

---

## 📖 Additional Resources

### Documentation

- [Flask Documentation](https://flask.palletsprojects.com/) - Web framework
- [Jinja2 Documentation](https://jinja.palletsprojects.com/) - Template engine
- [Python Type Hints](https://docs.python.org/3/library/typing.html) - Type annotations
- [PEP 8](https://pep8.org/) - Python style guide

### Tools

- [Black](https://black.readthedocs.io/) - Code formatter
- [Flake8](https://flake8.pycqa.org/) - Linter
- [MyPy](http://mypy-lang.org/) - Static type checker
- [Pytest](https://docs.pytest.org/) - Testing framework

### Project-Specific

- [Project README](README.md) - User documentation
- [GitHub Repository](https://github.com/yourusername/personal-blog)
- [Roadmap.sh Project](https://roadmap.sh/projects/personal-blog)

---

## 🔄 Version History

### AGENT.md Changelog

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2024-01-15 | Initial AGENT.md creation        |
|         |            | - Complete project structure     |
|         |            | - Coding standards defined       |
|         |            | - Common patterns documented     |
|         |            | - AI assistant integration guide |

---

## 💬 Need Help?

### When You Need Assistance

1. **Check this AGENT.md first** - Most patterns are documented here
2. **Review existing code** - See how similar features are implemented
3. **Check Flask documentation** - For framework-specific questions
4. **Use AI assistants** - Reference this file in your prompts
5. **Open an issue** - For project-specific problems

### Asking Effective Questions

**Good:**

```
Following the route pattern in AGENT.md, I'm trying to add pagination 
to the article listing. The current implementation loads all articles. 
How should I modify the route and template to support pagination?
```

**Better:**

```
Context: Article listing route in routes/guest.py
Goal: Add pagination (10 articles per page)
Constraints: Must follow existing patterns in AGENT.md
Question: Should pagination be query-param based (?page=2) or 
URL-based (/articles/page/2)? What's the Flask best practice?
```

---

## ✅ Project Checklist

Use this checklist when working on the Personal Blog project:

### Code Quality

- [ ] Follows PEP 8 style guidelines
- [ ] Includes type hints for all functions
- [ ] Has docstrings (Google style)
- [ ] Uses context managers for file operations
- [ ] Handles errors appropriately
- [ ] No hard-coded configuration values

### Security

- [ ] CSRF protection on all forms
- [ ] Input validation implemented
- [ ] No plain text passwords
- [ ] Environment variables used correctly
- [ ] SQL injection not applicable (no SQL)
- [ ] XSS protection via template escaping

### Testing

- [ ] Unit tests for new functions
- [ ] Route tests with auth checks
- [ ] Edge cases covered
- [ ] Test coverage > 80%
- [ ] All tests passing

### Documentation

- [ ] README updated if needed
- [ ] AGENT.md updated for new patterns
- [ ] Code comments for complex logic
- [ ] Docstrings complete

### UI/UX

- [ ] Responsive design tested
- [ ] Accessibility guidelines followed
- [ ] BEM naming convention used
- [ ] Mobile-first CSS
- [ ] Flash messages for user feedback

---

<div align="center">

**Built with ❤️ for developers who love clean code**

*This AGENT.md file is designed to work with multiple AI coding assistants.*

</div>
