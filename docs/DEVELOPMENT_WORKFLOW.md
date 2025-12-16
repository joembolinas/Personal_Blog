# Building a Personal Blog with GitHub Copilot: A Complete Guide

<div align="center">
  <h2>AI-Assisted Development Workflow for Personal Blog CMS</h2>
  <p>A comprehensive guide to building a filesystem-based blogging platform using GitHub Copilot's advanced customization features</p>
</div>

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Environment Setup](#environment-setup)
3. [Copilot Customization Setup](#copilot-customization-setup)
4. [Custom Agents and Prompts](#custom-agents-and-prompts)
5. [Development Workflow](#development-workflow)
6. [Example Interactions](#example-interactions)
7. [Best Practices &amp; Versioning](#best-practices--versioning)
8. [Cross-Platform AI Support](#cross-platform-ai-support)

---

## Project Overview

### What We're Building

The **Personal Blog** is a lightweight, filesystem-based content management system designed for publishing articles without the complexity of traditional databases. This guide demonstrates how to leverage GitHub Copilot's customization features to streamline development.

### Key Objectives

- **Simplicity**: Filesystem-based storage using JSON/Markdown
- **Separation of Concerns**: Public guest access and secured admin interface
- **AI-Assisted Development**: Custom Copilot configurations for consistent code generation
- **Cross-Platform AI Support**: Compatible with multiple AI coding assistants

### Technology Stack

- **Backend**: Python 3.x (Flask framework)
- **Frontend**: HTML5, Vanilla CSS3
- **Storage**: Filesystem (JSON/Markdown files)
- **Templating**: Jinja2 (server-side rendering)
- **AI Tooling**: GitHub Copilot with custom configurations

---

## Environment Setup

### Prerequisites

Before starting, ensure you have:

- Python 3.8 or higher
- Git installed
- GitHub Copilot subscription
- Code editor with Copilot support (VS Code, JetBrains IDEs, Neovim)

### Repository Initialization - ✅ done

```bash
# Create and navigate to project directory
mkdir personal-blog
cd personal-blog

# Initialize Git repository
git init

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Create initial project structure
mkdir -p .github/{copilot_instructions,copilot_agents,prompts,collections}
mkdir -p data static templates

# Create essential files
touch app.py requirements.txt .gitignore README.md
```

### Install Dependencies

Create `requirements.txt`:

```txt
Flask==3.0.0
python-dotenv==1.0.0
markdown2==2.4.10
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Configure .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Project specific
.env
*.log
```

---

## Copilot Customization Setup

GitHub Copilot can be customized through configuration files in the `.github/` directory. This section shows how to set up project-specific AI behavior.

### Custom Instructions Overview

Custom instructions guide Copilot's code generation to align with your project's standards and patterns.

### Step 1: Create Global Instructions

Create `.github/COPILOT-INSTRCTIONS.md`:

```markdown
# Global Copilot Instructions for Personal Blog

## Project Context
You are working on a Personal Blog CMS built with Python Flask. This is a filesystem-based blogging platform that stores articles in JSON/Markdown format.

## Coding Standards

### Python
- Follow PEP 8 guidelines strictly
- Use type hints for function parameters and return values
- Prefer list comprehensions over loops when appropriate
- Use context managers for file operations
- Maximum line length: 88 characters (Black formatter standard)

### Code Organization
- Keep functions focused and single-purpose
- Use docstrings for all functions and classes (Google style)
- Separate concerns: routes, business logic, and data access
- Avoid global variables; use Flask app context when needed

### Error Handling
- Always handle file I/O exceptions
- Return appropriate HTTP status codes
- Log errors with context information
- Provide user-friendly error messages

### Security
- Never store passwords in plain text
- Use environment variables for sensitive configuration
- Implement CSRF protection for forms
- Validate and sanitize all user inputs

## Project Architecture

### File Structure
```

/
├── app.py              # Main Flask application
├── models.py           # Data models and file operations
├── routes/             # Route handlers
│   ├── guest.py       # Public routes
│   └── admin.py       # Admin routes
├── utils/              # Helper functions
├── data/               # Article storage
├── static/             # CSS and assets
└── templates/          # Jinja2 templates

```

### Data Storage Pattern
- Articles stored as JSON files in `data/` directory
- Filename format: `{slug}.json`
- Content can be embedded or referenced as separate .md files

### Template Patterns
- Use template inheritance (`base.html` as parent)
- Separate guest and admin base templates
- Include CSRF tokens in all forms
- Use Jinja2 filters for date formatting and markdown rendering

## Response Guidelines
- Generate complete, production-ready code
- Include inline comments for complex logic
- Suggest security improvements when relevant
- Provide alternative approaches when applicable
```

### Step 2: Create Python-Specific Instructions

Create `.github/python/instrcutions.md`:

```markdown
# Python-Specific Instructions

## Flask Application Patterns

### Route Definitions
```python
@app.route('/endpoint', methods=['GET', 'POST'])
def handler_name():
    """Brief description of what this route does."""
    # Implementation
    pass
```

### Blueprint Usage

When creating route modules, use Flask blueprints:

```python
from flask import Blueprint

guest_bp = Blueprint('guest', __name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
```

### File Operations

Always use context managers and handle exceptions:

```python
from pathlib import Path
import json

def read_article(slug: str) -> dict:
    """Read article data from JSON file."""
    file_path = Path('data') / f'{slug}.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        # Log error
        return None
```

### Date Handling

Use datetime for timestamps:

```python
from datetime import datetime

created_at = datetime.now().isoformat()
```

### Markdown Processing

Convert markdown to HTML safely:

```python
import markdown2

html_content = markdown2.markdown(
    markdown_text,
    extras=['fenced-code-blocks', 'tables']
)
```

## Testing Patterns

When generating test code:

- Use pytest framework
- Include fixtures for common test data
- Test both success and failure cases
- Mock file operations

```

### Step 3: Create Frontend Instructions

Create `.github/COPILOT-INSTRCTIONS.mdfrontend.md`:

```markdown
# Frontend Development Instructions

## HTML Standards

### Template Structure
All templates should extend from a base template:
```html
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
<!-- Page content here -->
{% endblock %}
```

### Semantic HTML

- Use semantic tags: `<article>`, `<section>`, `<header>`, `<footer>`, `<nav>`
- Proper heading hierarchy (h1 -> h2 -> h3)
- Accessibility attributes (alt text, aria labels)

### Forms

```html
<form method="POST" action="{{ url_for('route_name') }}">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
  
    <label for="title">Title:</label>
    <input type="text" id="title" name="title" required>
  
    <button type="submit">Submit</button>
</form>
```

## CSS Standards

### Naming Convention

Use BEM (Block Element Modifier) methodology:

```css
.article-card { }
.article-card__title { }
.article-card__title--featured { }
```

### Layout Patterns

- Use CSS Grid for page layouts
- Flexbox for component layouts
- Mobile-first responsive design

### CSS Organization

```css
/* Layout */
/* Typography */
/* Components */
/* Utilities */
/* Media Queries */
```

## No JavaScript Framework

This project uses vanilla JavaScript sparingly. Any interactive features should:

- Use progressive enhancement
- Work without JavaScript when possible
- Be minimal and focused

```

---

## Custom Agents and Prompts

Agents are specialized AI assistants for specific tasks. They combine instructions, prompts, and context to provide focused assistance.

### Creating the Blog Agent

Create `.github/copilot_agents/blog-agent.yml`:

```yaml
name: blog-agent
description: Specialized agent for Personal Blog development tasks
version: 1.0.0

instructions:
  - .github/COPILOT-INSTRCTIONS.mdglobal.md
  - .github/COPILOT-INSTRCTIONS.mdpython.md

capabilities:
  - name: Create Article Model
    description: Generate data model for blog articles
    prompt: .github/prompts/create-article-model.md
  
  - name: Generate Route Handler
    description: Create Flask route with proper error handling
    prompt: .github/prompts/create-route.md
  
  - name: Build Template
    description: Generate Jinja2 template with proper structure
    prompt: .github/prompts/create-template.md
  
  - name: Write Tests
    description: Create comprehensive test cases
    prompt: .github/prompts/create-tests.md

context:
  directories:
    - data
    - templates
    - static
  file_patterns:
    - "*.py"
    - "*.html"
    - "*.css"
    - "*.json"

examples:
  - input: "Create a route to list all articles"
    output: |
      ```python
      @guest_bp.route('/')
      def index():
          """Display list of all published articles."""
          articles = get_all_articles()
          return render_template('guest/index.html', articles=articles)
      ```
```

### Creating Prompt Templates

#### Article Model Prompt

Create `.github/prompts/create-article-model.md`:

```markdown
# Create Article Model

Generate a Python data model for blog articles with the following requirements:

## Data Structure
- **slug**: URL-friendly identifier (unique)
- **title**: Article title (string, required)
- **content**: Article body in Markdown format
- **excerpt**: Short summary (optional)
- **author**: Author name
- **created_at**: ISO format timestamp
- **updated_at**: ISO format timestamp
- **published**: Boolean flag
- **tags**: List of tags

## Methods Required
1. `to_dict()`: Convert model to dictionary for JSON serialization
2. `from_dict(data)`: Create model instance from dictionary
3. `save()`: Persist article to JSON file
4. `load(slug)`: Load article from JSON file
5. `delete()`: Remove article file
6. `all()`: List all articles (class method)
7. `published_articles()`: List only published articles (class method)

## File Storage
- Store in `data/{slug}.json`
- Use UTF-8 encoding
- Pretty print JSON (indent=2)

## Error Handling
- Handle file not found
- Handle JSON decode errors
- Validate required fields
- Return None or raise appropriate exceptions
```

#### Route Handler Prompt

Create `.github/prompts/create-route.md`:

```markdown
# Create Flask Route Handler

Generate a Flask route handler with the following specifications:

## Requirements
- Proper HTTP method handling (GET, POST, PUT, DELETE)
- Input validation for form data
- Error handling with appropriate status codes
- Flash messages for user feedback
- Redirect after successful POST
- Template rendering with context

## Pattern to Follow
```python
@blueprint.route('/path', methods=['GET', 'POST'])
def handler_name():
    """Docstring describing the route's purpose."""
    if request.method == 'POST':
        # Validate input
        # Process data
        # Handle errors
        # Flash message
        # Redirect
  
    # Prepare context
    # Render template
```

## Security Considerations

- CSRF token validation
- Input sanitization
- Authentication check (for admin routes)
- Prevent path traversal in file operations

```

#### Template Creation Prompt

Create `.github/prompts/create-template.md`:

```markdown
# Create Jinja2 Template

Generate an HTML template following these guidelines:

## Structure
```html
{% extends "base.html" %}

{% block title %}Specific Page Title{% endblock %}

{% block content %}
<main class="container">
    <!-- Content here -->
</main>
{% endblock %}

{% block scripts %}
<!-- Page-specific scripts if needed -->
{% endblock %}
```

## Requirements

- Semantic HTML5
- Proper heading hierarchy
- Responsive design classes
- Accessibility attributes
- Template variables properly escaped: `{{ variable | e }}`
- Use filters for formatting: `{{ date | datetime }}`
- Conditional rendering: `{% if condition %}`
- Loop over collections: `{% for item in items %}`

## Forms

- Include CSRF token
- Proper labels for inputs
- Validation attributes
- Error message display

## Styling

- Use existing CSS classes from site stylesheet
- BEM naming convention for new classes
- Mobile-first responsive approach

```

### Creating Collections

Collections group related files for focused context.

Create `.github/collections/models-collection.md`:

```markdown
# Models Collection

This collection includes all data model related files for the Personal Blog project.

## Files Included
- models.py
- utils/file_handler.py
- utils/validators.py

## Purpose
Use this collection when working on:
- Data model definitions
- File I/O operations
- Data validation logic
- Serialization/deserialization

## Context
Articles are stored as JSON files with optional separate Markdown content files. 
The model layer abstracts file operations and provides a clean API for the route handlers.
```

Create `.github/collections/admin-routes-collection.md`:

```markdown
# Admin Routes Collection

Files related to the admin dashboard and content management.

## Files Included
- routes/admin.py
- templates/admin/*.html
- static/css/admin.css

## Purpose
Use when implementing:
- Admin dashboard
- Article CRUD operations
- Authentication/authorization
- Admin UI components

## Context
Admin routes require authentication. All forms must include CSRF protection.
Admin pages use a distinct visual style from the guest-facing pages.
```

---

## Development Workflow

### Phase 1: Project Foundation

#### 1.1 Create Main Application File

**Copilot Prompt:**

```
@blog-agent Create the main Flask application file (app.py) with:
- App initialization
- Blueprint registration
- Error handlers (404, 500)
- Template filters for date and markdown
- Configuration from environment variables
- Development vs production settings
```

**Expected Structure:**

```python
from flask import Flask, render_template
from pathlib import Path
import os

def create_app():
    """Application factory pattern."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
  
    # Register blueprints
    from routes import guest, admin
    app.register_blueprint(guest.guest_bp)
    app.register_blueprint(admin.admin_bp)
  
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
  
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

#### 1.2 Implement Data Models

**Copilot Prompt:**

```
Using the create-article-model prompt, generate the Article model class in models.py
```

### Phase 2: Guest-Facing Features

#### 2.1 Home Page (Article Listing)

**Copilot Prompt:**

```
@blog-agent Create a route in routes/guest.py to display all published articles:
- GET request
- Load all published articles from filesystem
- Sort by created_at descending
- Pass to template with proper context
```

**Follow-up Prompt:**

```
@blog-agent Now create the corresponding template templates/guest/index.html showing:
- Article cards with title, excerpt, date
- Link to full article
- Responsive grid layout
- Empty state if no articles
```

#### 2.2 Article Detail Page

**Copilot Prompt:**

```
@blog-agent Create a route to display a single article:
- URL pattern: /article/<slug>
- Load article by slug
- Return 404 if not found or not published
- Render markdown content to HTML
```

**Template Prompt:**

```
@blog-agent Generate template for article detail page with:
- Article title as h1
- Publication date
- Rendered markdown content
- Back to home link
```

### Phase 3: Admin Interface

#### 3.1 Authentication Setup

**Copilot Prompt:**

```
@blog-agent Implement basic authentication:
- Login form template
- Login route with session management
- Logout route
- Login required decorator for admin routes
- Use environment variables for credentials
```

#### 3.2 Admin Dashboard

**Copilot Prompt:**

```
@blog-agent Create admin dashboard showing:
- All articles (published and drafts)
- Quick actions: edit, delete, toggle published
- Create new article button
- Article count statistics
```

#### 3.3 Article CRUD Operations

**Create New Article:**

```
@blog-agent Generate form and route for creating new articles:
- Form fields: title, content (textarea), tags, published checkbox
- Auto-generate slug from title
- Validation: title required, unique slug
- Save to filesystem
- Flash success message and redirect
```

**Edit Existing Article:**

```
@blog-agent Create edit functionality:
- Pre-populate form with existing data
- Update updated_at timestamp
- Preserve created_at
- Handle slug changes carefully (file rename)
```

**Delete Article:**

```
@blog-agent Implement delete with confirmation:
- Delete route with POST method
- Remove JSON file
- Confirmation modal or page
- Redirect to dashboard after deletion
```

### Phase 4: Styling and Polish

#### 4.1 Guest Stylesheet

**Copilot Prompt:**

```
Generate CSS for guest pages (static/css/guest.css):
- Clean, readable typography
- Responsive grid for article cards
- Article detail layout optimized for reading
- Color scheme: light mode with good contrast
- Mobile-first responsive breakpoints
```

#### 4.2 Admin Stylesheet

**Copilot Prompt:**

```
Create admin interface CSS (static/css/admin.css):
- Dashboard layout with sidebar
- Form styling
- Data table for article list
- Action buttons with hover states
- Distinct visual theme from guest pages
```

### Phase 5: Testing and Documentation

**Copilot Prompt:**

```
@blog-agent Generate pytest test suite including:
- Test fixtures for sample articles
- Tests for all model methods
- Tests for guest routes (including 404 cases)
- Tests for admin routes (with authentication)
- Mock filesystem operations
```

---

## Example Interactions

### Example 1: Creating the Article Model

**Developer:**

```
@blog-agent Using the article model prompt, create models.py with full implementation
```

**Copilot Response:**

```python
"""Data models for Personal Blog."""
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
import json
import re

DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)


class Article:
    """Represents a blog article stored as JSON file."""
  
    def __init__(
        self,
        title: str,
        content: str,
        slug: Optional[str] = None,
        excerpt: str = '',
        author: str = 'Admin',
        published: bool = False,
        tags: Optional[List[str]] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        """Initialize article with provided data."""
        self.title = title
        self.content = content
        self.slug = slug or self._generate_slug(title)
        self.excerpt = excerpt
        self.author = author
        self.published = published
        self.tags = tags or []
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
  
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title."""
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s_-]+', '-', slug)
        slug = slug.strip('-')
        return slug
  
    def to_dict(self) -> Dict:
        """Convert article to dictionary for JSON serialization."""
        return {
            'slug': self.slug,
            'title': self.title,
            'content': self.content,
            'excerpt': self.excerpt,
            'author': self.author,
            'published': self.published,
            'tags': self.tags,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
  
    @classmethod
    def from_dict(cls, data: Dict) -> 'Article':
        """Create article instance from dictionary."""
        return cls(**data)
  
    def save(self) -> None:
        """Persist article to JSON file."""
        self.updated_at = datetime.now().isoformat()
        file_path = DATA_DIR / f'{self.slug}.json'
    
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
  
    @classmethod
    def load(cls, slug: str) -> Optional['Article']:
        """Load article from JSON file."""
        file_path = DATA_DIR / f'{slug}.json'
    
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls.from_dict(data)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None
  
    def delete(self) -> None:
        """Remove article file from filesystem."""
        file_path = DATA_DIR / f'{self.slug}.json'
        if file_path.exists():
            file_path.unlink()
  
    @classmethod
    def all(cls) -> List['Article']:
        """Load all articles from filesystem."""
        articles = []
        for file_path in DATA_DIR.glob('*.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    articles.append(cls.from_dict(data))
            except (json.JSONDecodeError, KeyError):
                continue
    
        return sorted(articles, key=lambda a: a.created_at, reverse=True)
  
    @classmethod
    def published_articles(cls) -> List['Article']:
        """Get only published articles."""
        return [a for a in cls.all() if a.published]
```

### Example 2: Creating Guest Routes

**Developer:**

```
Create routes/guest.py with home page and article detail routes
```

**Copilot Response:**

```python
"""Guest-facing routes for Personal Blog."""
from flask import Blueprint, render_template, abort
from models import Article
import markdown2

guest_bp = Blueprint('guest', __name__)


@guest_bp.route('/')
def index():
    """Display list of all published articles."""
    articles = Article.published_articles()
    return render_template('guest/index.html', articles=articles)


@guest_bp.route('/article/<slug>')
def article_detail(slug: str):
    """Display single article with full content."""
    article = Article.load(slug)
  
    if not article or not article.published:
        abort(404)
  
    # Convert markdown to HTML
    html_content = markdown2.markdown(
        article.content,
        extras=['fenced-code-blocks', 'tables', 'break-on-newline']
    )
  
    return render_template(
        'guest/article.html',
        article=article,
        html_content=html_content
    )
```

### Example 3: Admin Dashboard Template

**Developer:**

```
@blog-agent Create templates/admin/dashboard.html with article management interface
```

**Copilot Response:**

```html
{% extends "admin/base.html" %}

{% block title %}Dashboard - Personal Blog Admin{% endblock %}

{% block content %}
<div class="admin-dashboard">
    <header class="dashboard-header">
        <h1>Article Management</h1>
        <a href="{{ url_for('admin.create_article') }}" class="btn btn-primary">
            + New Article
        </a>
    </header>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <div class="dashboard-stats">
        <div class="stat-card">
            <h3>{{ articles|length }}</h3>
            <p>Total Articles</p>
        </div>
        <div class="stat-card">
            <h3>{{ articles|selectattr('published')|list|length }}</h3>
            <p>Published</p>
        </div>
        <div class="stat-card">
            <h3>{{ articles|rejectattr('published')|list|length }}</h3>
            <p>Drafts</p>
        </div>
    </div>

    <div class="articles-table">
        <table>
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Status</th>
                    <th>Created</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for article in articles %}
                <tr>
                    <td>
                        <strong>{{ article.title }}</strong>
                        <br>
                        <small class="text-muted">/article/{{ article.slug }}</small>
                    </td>
                    <td>
                        <span class="badge badge-{{ 'success' if article.published else 'secondary' }}">
                            {{ 'Published' if article.published else 'Draft' }}
                        </span>
                    </td>
                    <td>{{ article.created_at[:10] }}</td>
                    <td class="actions">
                        {% if article.published %}
                            <a href="{{ url_for('guest.article_detail', slug=article.slug) }}" 
                               class="btn btn-sm" target="_blank">View</a>
                        {% endif %}
                        <a href="{{ url_for('admin.edit_article', slug=article.slug) }}" 
                           class="btn btn-sm btn-secondary">Edit</a>
                        <form method="POST" 
                              action="{{ url_for('admin.delete_article', slug=article.slug) }}" 
                              style="display: inline;"
                              onsubmit="return confirm('Delete this article permanently?');">
                            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
                            <button type="submit" class="btn btn-sm btn-danger">Delete</button>
                        </form>
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="4" class="text-center">
                        <p>No articles yet. Create your first article to get started!</p>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
```

### Example 4: Form Validation Helper

**Developer:**

```
Create a utility function to validate article form data
```

**Copilot Response:**

```python
"""Validation utilities for Personal Blog."""
from typing import Dict, List, Tuple


def validate_article_data(data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate article form data.
  
    Args:
        data: Dictionary containing form fields
    
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
  
    # Required fields
    if not data.get('title', '').strip():
        errors.append('Title is required')
    elif len(data['title']) > 200:
        errors.append('Title must be less than 200 characters')
  
    if not data.get('content', '').strip():
        errors.append('Content is required')
  
    # Optional fields validation
    excerpt = data.get('excerpt', '')
    if excerpt and len(excerpt) > 500:
        errors.append('Excerpt must be less than 500 characters')
  
    # Tags validation
    tags = data.get('tags', [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',') if t.strip()]
  
    if len(tags) > 10:
        errors.append('Maximum 10 tags allowed')
  
    return len(errors) == 0, errors
```

### Example 5: CSS Generation

**Developer:**

```
Generate responsive CSS for article cards on the home page
```

**Copilot Response:**

```css
/* Article Cards - Guest Home Page */

.articles-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem;
    margin: 2rem 0;
}

@media (min-width: 768px) {
    .articles-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1024px) {
    .articles-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

.article-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    transition: transform 0.2s, box-shadow 0.2s;
    display: flex;
    flex-direction: column;
}

.article-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.article-card__title {
    font-size: 1.5rem;
    margin: 0 0 0.5rem 0;
    color: #2c3e50;
}

.article-card__title a {
    color: inherit;
    text-decoration: none;
}

.article-card__title a:hover {
    color: #3498db;
}

.article-card__meta {
    font-size: 0.875rem;
    color: #7f8c8d;
    margin-bottom: 1rem;
}

.article-card__excerpt {
    flex-grow: 1;
    line-height: 1.6;
    color: #34495e;
    margin-bottom: 1rem;
}

.article-card__tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: auto;
}

.article-card__tag {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background: #ecf0f1;
    color: #2c3e50;
    border-radius: 4px;
    font-size: 0.75rem;
    text-decoration: none;
    transition: background 0.2s;
}

.article-card__tag:hover {
    background: #3498db;
    color: white;
}

.article-card__read-more {
    display: inline-block;
    margin-top: 1rem;
    color: #3498db;
    text-decoration: none;
    font-weight: 500;
}

.article-card__read-more:hover {
    text-decoration: underline;
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #7f8c8d;
}

.empty-state h2 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.empty-state p {
    margin: 0;
}
```

---

## Best Practices & Versioning

### Configuration Management

#### Version Control for Copilot Settings

Track your Copilot configurations in Git:

```bash
# Add Copilot configurations to repository
git add .github/COPILOT-INSTRCTIONS.md
git add .github/copilot_agents/
git add .github/prompts/
git add .github/collections/

# Commit with descriptive message
git commit -m "Add Copilot customizations for Personal Blog project"
```

#### Sharing Configurations with Team

**Create a documentation file:**

`.github/COPILOT_GUIDE.md`:

```markdown
# Team Copilot Configuration Guide

## Setup Instructions

1. Ensure you have GitHub Copilot enabled in your IDE
2. Pull the latest changes to get `.github/` configurations
3. Restart your IDE to load custom instructions

## Available Agents

- `@blog-agent`: Primary agent for blog development
  - Use for model creation, routes, and templates
  - Understands project conventions and patterns

## Common Prompts

### Creating New Features
- `@blog-agent Create a route for [feature]`
- `@blog-agent Generate template for [page]`
- `@blog-agent Add tests for [component]`

### Code Review
- "Review this code for security issues"
- "Suggest performance improvements"
- "Check for PEP 8 compliance"

## Tips for Better Results

1. Be specific about requirements
2. Reference prompt templates when available
3. Use collections to provide focused context
4. Review and test generated code before committing
```

### Maintaining Quality

#### Regular Review Process

1. **Weekly Review**: Check if Copilot suggestions align with standards
2. **Update Instructions**: Refine based on common issues or new patterns
3. **Team Feedback**: Gather input on Copilot's effectiveness

#### Testing Copilot Outputs

Always validate generated code:

```bash
# Run linters
flake8 *.py routes/*.py

# Run type checker
mypy *.py

# Run test suite
pytest tests/ -v

# Check code coverage
pytest --cov=. tests/
```

### Continuous Improvement

#### Iteration Checklist

- [ ] Are custom instructions clear and comprehensive?
- [ ] Do agents produce consistent results?
- [ ] Are prompt templates effective?
- [ ] Does the team understand how to use configurations?
- [ ] Are there new patterns that should be documented?

#### Updating Configurations

When you discover better patterns:

1. Update relevant instruction file
2. Test with sample prompts
3. Document the change
4. Share with team
5. Commit and push

**Example commit:**

```bash
git add .github/COPILOT-INSTRCTIONS.mdpython.md
git commit -m "Update Python instructions: Add async/await patterns"
git push origin main
```

### Documentation Standards

Keep a changelog for Copilot configurations:

`.github/COPILOT_CHANGELOG.md`:

```markdown
# Copilot Configuration Changelog

## [1.2.0] - 2024-01-15
### Added
- New agent for deployment tasks
- Prompt template for Docker configuration

### Changed
- Updated Python instructions with async patterns
- Refined error handling guidelines

### Fixed
- Template generation prompt now includes CSRF token reminder

## [1.1.0] - 2024-01-08
### Added
- Collections for focused context
- Frontend-specific instructions

## [1.0.0] - 2024-01-01
### Added
- Initial Copilot customization setup
- Blog agent configuration
- Core prompt templates
```

---

## Cross-Platform AI Support

To make this project accessible to other AI coding assistants (Cursor, Claude Code, Gemini Code, etc.), we provide a universal AGENT.md file.

### Creating AGENT.md

Create `AGENT.md` in project root:

```markdown
# AI Assistant Guide for Personal Blog Project

This document provides context and guidelines for AI coding assistants working on this project.

## Project Overview

**Personal Blog** is a filesystem-based content management system built with Python Flask. Articles are stored as JSON files with Markdown content.

## Project Structure

```

personal-blog/
├── app.py              # Flask application entry point
├── models.py           # Article data model
├── routes/
│   ├── guest.py       # Public-facing routes
│   └── admin.py       # Admin panel routes
├── templates/
│   ├── base.html      # Base template
│   ├── guest/         # Public templates
│   └── admin/         # Admin templates
├── static/
│   └── css/           # Stylesheets
├── data/              # Article storage (JSON files)
├── utils/             # Helper functions
└── tests/             # Test suite

```

## Technology Stack

- **Language**: Python 3.8+
- **Framework**: Flask 3.0
- **Templating**: Jinja2
- **Storage**: Filesystem (JSON + Markdown)
- **Styling**: Vanilla CSS3 (no frameworks)

## Coding Standards

### Python Guidelines

Follow PEP 8 with these specifics:
- Type hints for all function parameters and returns
- Docstrings in Google style
- Maximum line length: 88 characters
- Use `pathlib.Path` for file operations
- Context managers for file I/O

**Example:**
```python
from pathlib import Path
from typing import Optional

def read_article(slug: str) -> Optional[dict]:
    """
    Read article data from JSON file.
  
    Args:
        slug: URL-friendly article identifier
    
    Returns:
        Article data as dictionary, or None if not found
    """
    file_path = Path('data') / f'{slug}.json'
    if not file_path.exists():
        return None
  
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
```

### HTML/CSS Guidelines

- Semantic HTML5 elements
- BEM naming convention for CSS
- Mobile-first responsive design
- Accessibility: alt text, ARIA labels, proper heading hierarchy

### Security Requirements

- CSRF protection on all forms
- Input validation and sanitization
- No plain text password storage
- Environment variables for sensitive config
- Proper error handling without information leakage

## Data Model

### Article Schema

```json
{
  "slug": "my-first-post",
  "title": "My First Post",
  "content": "# Article content in Markdown",
  "excerpt": "Short summary...",
  "author": "Admin",
  "published": true,
  "tags": ["python", "flask"],
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### File Naming Convention

Articles are stored as: `data/{slug}.json`

## Common Tasks

### Creating a New Route

1. Identify if it's guest or admin route
2. Add function to appropriate blueprint
3. Include proper error handling
4. Create corresponding template
5. Add tests

**Template:**

```python
@blueprint.route('/path', methods=['GET', 'POST'])
def handler_name():
    """Brief description of route purpose."""
    # Implementation
    pass
```

### Creating a Template

1. Extend from appropriate base template
2. Define required blocks: title, content
3. Use template filters for dates and markdown
4. Include CSRF tokens in forms

**Template:**

```html
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
<!-- Content here -->
{% endblock %}
```

### Writing Tests

Use pytest with these patterns:

```python
def test_article_creation():
    """Test creating a new article."""
    article = Article(title="Test", content="Content")
    article.save()
  
    loaded = Article.load(article.slug)
    assert loaded.title == "Test"
  
    # Cleanup
    article.delete()
```

## Important Patterns

### Error Handling

```python
try:
    # File operation
    pass
except FileNotFoundError:
    # Handle missing file
    pass
except json.JSONDecodeError:
    # Handle corrupted data
    pass
```

### Form Processing

```python
if request.method == 'POST':
    # Validate
    if not request.form.get('title'):
        flash('Title is required', 'error')
        return redirect(url_for('current_route'))
  
    # Process
    # ...
  
    flash('Success message', 'success')
    return redirect(url_for('next_route'))
```

### Template Rendering

```python
return render_template(
    'template.html',
    variable=value,
    articles=articles
)
```

## Dependencies

See `requirements.txt` for full list:

- Flask==3.0.0
- python-dotenv==1.0.0
- markdown2==2.4.10

## Environment Variables

Required in `.env`:

```
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=hashed-password
FLASK_ENV=development
```

## Testing

Run tests:

```bash
pytest tests/ -v
pytest --cov=. tests/  # With coverage
```

## Common Issues and Solutions

### Issue: Article not appearing on homepage

- Check if `published` is set to `true`
- Verify JSON file is in `data/` directory
- Confirm filename matches slug

### Issue: Template not found

- Check template path relative to `templates/` directory
- Verify blueprint is properly registered
- Ensure template name matches route call

### Issue: CSRF token errors

- Include `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>` in forms
- Check Flask secret key is set
- Verify form method is POST

## Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Jinja2 Templates: https://jinja.palletsprojects.com/
- PEP 8 Style Guide: https://pep8.org/
- Project Repository: https://github.com/yourusername/personal-blog

## Questions?

When working on this project:

1. Check this AGENT.md first
2. Review existing code for patterns
3. Refer to Flask documentation
4. Ask specific questions with context

## Recent Updates

- 2024-01-15: Initial AGENT.md creation
- Project supports GitHub Copilot custom instructions (see `.github/` directory)

```

### Platform-Specific Notes

#### For Cursor AI

Cursor reads both `.github/` configurations and `AGENT.md`. Place this in `.cursorrules`:

```

# Cursor AI Rules for Personal Blog

Read AGENT.md for comprehensive project context.

## Priority Rules

1. Always use type hints
2. Include docstrings
3. Handle exceptions properly
4. Use context managers for files
5. Validate user input

## Quick Reference

- Models: See models.py for Article class
- Routes: Blueprint pattern in routes/ directory
- Templates: Jinja2 in templates/ directory

```

#### For Claude Code

Claude Code benefits from detailed context in AGENT.md. No additional configuration needed.

#### For GitHub Copilot

Primary configuration is in `.github/` directory. AGENT.md serves as additional context.

#### For Gemini Code

Gemini Code reads AGENT.md automatically. Optionally create `.gemini/context.md`:

```markdown
# Gemini Context for Personal Blog

See AGENT.md for full project documentation.

## Key Points
- Flask-based blog CMS
- Filesystem storage (no database)
- Admin authentication required
- Mobile-first CSS design
```

### Universal Configuration File

Create `.ai-coding-assistant.json`:

```json
{
  "project": {
    "name": "Personal Blog",
    "type": "web-application",
    "language": "python",
    "framework": "flask"
  },
  "documentation": {
    "primary": "AGENT.md",
    "github_copilot": ".github/COPILOT-INSTRCTIONS.md",
    "cursor": ".cursorrules"
  },
  "standards": {
    "style_guide": "PEP 8",
    "line_length": 88,
    "type_hints": true,
    "docstring_style": "google"
  },
  "testing": {
    "framework": "pytest",
    "coverage_required": 90
  },
  "security": {
    "csrf_protection": true,
    "input_validation": "required",
    "environment_variables": true
  }
}
```

---

## Appendix: Quick Reference

### Essential Commands

```bash
# Environment setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run application
python app.py

# Run tests
pytest tests/ -v

# Code quality
flake8 *.py routes/
mypy *.py

# Git workflow
git add .
git commit -m "descriptive message"
git push origin main
```

### Common Copilot Prompts

| Task              | Prompt                                                           |
| ----------------- | ---------------------------------------------------------------- |
| Create model      | `@blog-agent Using article model prompt, create models.py`     |
| Add route         | `@blog-agent Create route for [feature] with error handling`   |
| Generate template | `@blog-agent Build template for [page] with responsive design` |
| Write tests       | `@blog-agent Generate tests for [component]`                   |
| Review security   | `Check this code for security vulnerabilities`                 |
| Optimize code     | `Suggest performance improvements for this function`           |

### File Templates

#### Route Template

```python
@blueprint.route('/path', methods=['GET', 'POST'])
def handler():
    """Description."""
    if request.method == 'POST':
        # Validate and process
        flash('Message', 'category')
        return redirect(url_for('route'))
  
    return render_template('template.html', data=data)
```

#### Template File

```html
{% extends "base.html" %}
{% block title %}Title{% endblock %}
{% block content %}
<main class="container">
    <!-- Content -->
</main>
{% endblock %}
```

#### Test Template

```python
def test_feature():
    """Test description."""
    # Setup
    # Execute
    # Assert
    # Cleanup
```

---

## Conclusion

This guide demonstrates how GitHub Copilot's customization features can be leveraged to create a consistent, high-quality development workflow for the Personal Blog project. By combining custom instructions, specialized agents, prompt templates, and collections, we've built an AI-assisted development environment that:

1. **Maintains Code Quality**: Enforces project standards automatically
2. **Increases Productivity**: Reduces boilerplate and repetitive tasks
3. **Ensures Consistency**: All generated code follows the same patterns
4. **Supports Learning**: New team members can understand project conventions
5. **Cross-Platform Compatible**: Works with multiple AI coding assistants

### Next Steps

1. Clone this repository and set up the Copilot configurations
2. Experiment with the provided prompts and agents
3. Customize instructions to match your specific needs
4. Share configurations with your team
5. Iterate and improve based on experience

### Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/copilot)
- [Awesome Copilot Repository](https://github.com/github/awesome-copilot)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Personal Blog Project](https://roadmap.sh/projects/personal-blog)

---

<div align="center">
  <p><strong>Happy Coding with AI-Assisted Development! 🚀</strong></p>
  <sub>Built for the roadmap.sh community</sub>
</div>
```
