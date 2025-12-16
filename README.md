<div align="center">
  <a href="https://roadmap.sh/projects/personal-blog">
    <img src="https://roadmap.sh/favicon.ico" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Personal Blog</h3>

<p align="center">
    A simple, filesystem-based content management system for publishing articles.
    <br />
    <a href="https://roadmap.sh"><strong>Explore roadmap.sh »</strong></a>
    <br />
    <br />
    <a href="https://roadmap.sh/backend/projects">Project Architecture</a>
    ·
    <a href="https://github.com/joembolinas/Personal_Blog/issues">Technology Stack</a>
    ·
    <a href="https://github.com/joembolinas/Personal_Blog/issues">Project Structure</a>
  </p>
</div>

<!-- ABLE TO USE BOTH BANNERS IF NEEDED, BUT ONE IS CLEANER -->

<div align="center">
  <img src="https://assets.roadmap.sh/guest/blog-guest-pages.png" alt="Personal Blog Guest Pages" width="100%">
</div>

## Project Overview

**Personal Blog** is a lightweight blogging platform designed to help users write and publish articles effortlessly. It features a separation of concerns between public access and administrative control, ensuring a smooth reading experience for guests and a robust management interface for the author.

The project emphasizes simplicity by utilizing the filesystem for data storage, eliminating the need for complex database setups during the initial phase.

## Key Features

### 🌍 Guest Section

Accessible to all visitors:

- **Home Page**: Browse a curated list of published articles.
- **Article Viewer**: Read full articles with distraction-free layout and publication dates.

### 🔒 Admin Section

Secured area for content management:

- **Dashboard**: Overview of all articles with quick actions.
- **Create & Edit**: Rich forms to draft new posts or update existing content.
- **Delete**: Remove outdated or unwanted articles.
- **Authentication**: Secure login protection for administrative routes.

<div align="center">
  <img src="https://assets.roadmap.sh/guest/blog-admin-pages.png" alt="Personal Blog Admin Pages" width="80%">
</div>

## Technology Stack

- **Core**: Python (Backend logic and server)
- **Frontend**: HTML5, Vanilla CSS3 (No JavaScript framework required)
- **Storage**: Filesystem-based storage (JSON/Markdown)
- **Templating**: Server-side HTML rendering

## Project Architecture

The application follows a simplified **Model-View-Controller (MVC)** pattern:

- **Model**: Data is structured in flat files (JSON/MD) stored locally.
- **View**: HTML templates rendered on the server side using the backend engine.
- **Controller**: Python routes handle incoming requests, process data, and return the appropriate view.

> **Note**: This architecture is designed for ease of use and learning, avoiding the complexity of a full RDBMS.

## Quick Start

---

## Quick Start

Prerequisites:

- Python 3.8+
- Git

Clone and run:

```bash
git clone https://github.com/joembolinas/Personal_Blog.git
cd Personal_Blog
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py
```

Open:

- Guest: http://localhost:5000
- Admin: http://localhost:5000/admin

---

## What this project provides

- Filesystem-based article storage (`data/{slug}.json`) for easy versioning and backups.
- Minimal Flask-based CMS with public guest views and a protected admin area.
- Automated tests and CI guidance (project aims for 90% coverage).

---

## Documentation (developer-facing)

The repository includes curated documentation to onboard contributors and guide implementations. Read these first:

- [docs/DEVELOPMENT_WORKFLOW.md](docs/DEVELOPMENT_WORKFLOW.md) — Contributor workflow, Copilot customization, and project practices.
- [docs/PROJECT_ARCHITECTURE.md](docs/PROJECT_ARCHITECTURE.md) — Architecture decisions and component responsibilities.
- [docs/EPIC-PRD.md](docs/EPIC-PRD.md) — Epic-level product requirements and feature breakdowns.
- [docs/TECH-STACK.md](docs/TECH-STACK.md) — Recommended packages and versions.
- [docs/Project_Folders_Structure_Blueprint.md](docs/Project_Folders_Structure_Blueprint.md) — Project folder layout and file responsibilities.
- [docs/Logical_Design_Exemplars.md](docs/Logical_Design_Exemplars.md) — Code patterns and testing exemplars.
- [docs/Phase3_Development_Quality_Gates.md](docs/Phase3_Development_Quality_Gates.md) — Implementation backlog and Phase 3 quality gates (new).
- [docs/project_memory.md](docs/project_memory.md) — Project memory, goals, and integration notes.

---

## Integration & Reusability (from project memory)

This project is structured so components can be reused inside a larger application. Key notes:

- Keep domain logic (`models.py`) decoupled from Flask handlers so the model can be imported as a library in other projects.
- Provide small adapter wrappers if embedding into larger systems (e.g., `adapters/` exposing a clear programmatic API).
- Include example import/usage patterns in `README` or `docs/` when creating integration scenarios.

Planned integration items (see docs/Phase3_Development_Quality_Gates.md): adapters, example embeddings, and additional CI checks for cross-platform support (Windows + Linux).

---

## Project Status & Next Steps

Key pending tasks (high level):

- Implement `models.Article` with robust atomic `save()` / `load()` / `delete()` and comprehensive unit tests.
- Add `requirements.txt` (pinned versions) and optional `Dockerfile` for production containerization.
- Add integration tests, CI coverage enforcement (90%), and lint/type checks (`flake8`, `mypy`).

See [docs/Phase3_Development_Quality_Gates.md](docs/Phase3_Development_Quality_Gates.md) for a full, prioritized backlog and quality gates.

---

## Contributing

Please follow the conventions in [docs/DEVELOPMENT_WORKFLOW.md](docs/DEVELOPMENT_WORKFLOW.md).

- Create a branch per feature: `feature/<short-description>`
- Include tests for new behavior and ensure coverage targets are met locally before opening a PR.

---

## License & Attribution

This mini-project is provided as-is for learning and experimentation.

---

v1.0.0 | Active | Last Updated: Dec 16 2025 - 14:30
