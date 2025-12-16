---
title: Process Specification for Personal Blog CMS Development
version: 1.0
date_created: 2025-12-16
last_updated: 2025-12-16
owner: Personal Blog Project Team
tags: [process, cms, blog, flask, filesystem, ai-assisted]
---

# Introduction

This specification defines the process, requirements, and constraints for developing the Personal Blog CMS—a lightweight, filesystem-based content management system for publishing articles, built with Python Flask. The goal is to enable simple, secure, and maintainable article publishing for individuals or small teams, using modern development workflows and AI-assisted tooling.

## Source of Requirements

The canonical source for functional requirements is the Roadmap.sh project brief provided at docs/roadmap.sh.md. This specification formalizes those requirements, and incorporates additional workflow guidance from AGENT.md and docs/DEVELOPMENT_WORKFLOW.md for the AI-optimized development pipeline.

## 1. Purpose & Scope

This document outlines the process for building, testing, and maintaining the Personal Blog CMS. It is intended for developers, maintainers, and contributors. The scope includes project setup, feature development, testing, deployment, and maintenance, with a focus on filesystem-based storage, clean architecture, and minimal dependencies.

## 2. Definitions

- **CMS**: Content Management System
- **Flask**: Python web framework
- **Filesystem-based**: Data stored as files (JSON/Markdown), not in a database
- **Blueprint**: Flask modular route handler
- **Article**: A blog post, stored as a JSON file
- **Admin**: Authenticated user with content management privileges
- **Guest**: Public, unauthenticated user

## 3. Requirements, Constraints & Guidelines

- **REQ-001**: Articles must be stored as individual JSON files in the data/ directory.
- **REQ-002**: The system must provide separate interfaces for public (guest) and admin users.
- **REQ-003**: Admin authentication must use session-based login.
- **REQ-004**: All forms must include CSRF protection.
- **REQ-005**: Markdown content must be rendered safely to HTML.
- **REQ-006**: The system must be deployable without a database.
- **SEC-001**: Passwords must never be stored in plain text.
- **SEC-002**: All user input must be validated and sanitized.
- **CON-001**: Only Python 3.8+ and Flask 3.0+ are supported.
- **CON-002**: No external database dependencies allowed.
- **GUD-001**: Follow PEP 8 and project-specific coding standards.
- **PAT-001**: Use MVC (Model-View-Controller) pattern for code organization.

## 4. Interfaces & Data Contracts

### Article JSON Schema

```json
{
  "slug": "string",
  "title": "string",
  "content": "string (Markdown)",
  "excerpt": "string",
  "author": "string",
  "created_at": "ISO 8601 string",
  "updated_at": "ISO 8601 string",
  "published": "boolean",
  "tags": ["string"]
}
```

### Admin Authentication

- Login form: POST /admin/login
- Session cookie for authenticated state

### Public API

- GET / : List published articles
- GET /article/<slug> : View article

## 5. Acceptance Criteria

- **AC-001**: Given a valid article JSON, when saved, then it is retrievable and viewable by guests.
- **AC-002**: Given an admin user, when logged in, then they can create, edit, and delete articles.
- **AC-003**: Given a guest user, when accessing admin routes, then access is denied.
- **AC-004**: Given invalid input, when submitting forms, then errors are shown and data is not saved.
- **AC-005**: Given a published article, when visiting the homepage, then it appears in the article list.

## 6. Test Automation Strategy

- **Test Levels**: Unit (models, utils), Integration (routes), End-to-End (user flows)
- **Frameworks**: pytest, pytest-cov
- **Test Data Management**: Use fixtures for sample articles; clean up test files after tests.
- **CI/CD Integration**: Run tests and linting in GitHub Actions on push and PR.
- **Coverage Requirements**: Minimum 90% code coverage.
- **Performance Testing**: Manual for now; ensure page loads <1s with 100 articles.

## 7. Rationale & Context

Filesystem-based storage is chosen for simplicity, portability, and ease of versioning. The separation of guest and admin interfaces improves security and maintainability. Minimal dependencies and clear architecture enable easy onboarding and long-term support.

## 8. Dependencies & External Integrations

### External Systems
- **EXT-001**: None (self-contained)

### Third-Party Services
- **SVC-001**: None required

### Infrastructure Dependencies
- **INF-001**: Local or cloud server capable of running Python 3.8+ and Flask 3.0+

### Data Dependencies
- **DAT-001**: Filesystem access for data/ directory

### Technology Platform Dependencies
- **PLT-001**: Python 3.8+, Flask 3.0+, Jinja2, markdown2

### Compliance Dependencies
- **COM-001**: None

## 9. Examples & Edge Cases

```python
# Example: Article with missing required field
{
  "slug": "missing-title",
  "content": "No title here",
  "author": "admin",
  "created_at": "2025-12-16T10:00:00Z",
  "updated_at": "2025-12-16T10:00:00Z",
  "published": true,
  "tags": []
}
# Should fail validation (missing 'title')
```

## 10. Validation Criteria

- All requirements in section 3 are implemented and enforced.
- All acceptance criteria in section 5 are met by automated tests.
- Code passes linting and type checks.
- Documentation is complete and up to date.

## 11. Related Specifications / Further Reading

- [DEVELOPMENT_WORKFLOW.md](./DEVELOPMENT_WORKFLOW.md)
- [AGENT.md](../AGENT.md)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)

```
v1.0.0 | Active | Last Updated: Dec 11 2025 - 14:30
```