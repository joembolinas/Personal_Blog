<div align="center">
  <a href="https://roadmap.sh/projects/personal-blog">
    <img src="https://roadmap.sh/favicon.ico" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Personal Blog</h3>

<p align="center">
    A lightweight, filesystem-based CMS for publishing articles. <br/>
    <a href="https://roadmap.sh/projects/personal-blog"><strong>Project URL »</strong></a>
    <br />
    <br />
    <a href="https://roadmap.sh/backend/projects">Project Architecture</a>
    ·
    <a href="https://github.com/joembolinas/Personal_Blog/issues">Technology Stack</a>
    ·
    <a href="https://github.com/joembolinas/Personal_Blog/issues">Report Bug</a>
  </p>
</div>

<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

</div>

<div align="center">
  <img src="https://assets.roadmap.sh/guest/blog-guest-pages.png" alt="Personal Blog Guest Pages" width="100%">
</div>

## 💡 About The Project

**Personal Blog** is a practice project designed to demonstrate core backend development skills—**templating, filesystem operations, authentication, and session management**—without the complexity of a heavy database.

### Why This Exists

I built this project to:

* Practise comprehensive **Python Web Development**.
* Showcase my ability to build a **Simple CMS** from scratch.
* Demonstrate mastery of **MVC Architecture** in a RESTful environment.

### Who This Is For

* **Developers**: Looking for a modular CMS module to integrate into larger project in Python.
* **Students**: Wanting to learn how to build a content management system for blogs or notes.
* **Learners**: Exploring how to implement authentication and file handling manually.

---

## 🔥 Key Features

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

---



## Quick Start

### Option A: Docker (Recommended)

```bash
 # Build image
 docker build -t personal-blog .
 
 # Run container (mounts data/ directory for persistence)
 # Linux/Mac:
 docker run -p 8000:8000 -v $(pwd)/data:/app/data personal-blog
 
 # Windows (PowerShell):
 docker run -p 8000:8000 -v ${PWD}/data:/app/data personal-blog
```

 Visit [http://localhost:8000](http://localhost:8000).

### Option B: Manual Setup

1. **Install Dependencies**:

   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate

   pip install -r requirements.txt
   ```
2. **Configure Admin**:
   generate a hash for your password:

   ```bash
   # Run this once in python shell
   from utils.security import hash_password
   print(hash_password("my-secret-password"))
   ```

   Set the hash in your environment (or `.env` file):

   ```bash
   export ADMIN_PASSWORD_HASH='salt$hash...'
   export SECRET_KEY='your-secret-key'
   ```
3. **Run App**:

   ```bash
   flask --app app:create_app run
   ```

---

## What this project provides

- Filesystem-based article storage (`data/{slug}.json`) for easy versioning and backups.
- Minimal Flask-based CMS with public guest views and a protected admin area.
- Automated tests and CI guidance (project aims for 90% coverage).

---

## Documentation (developer-facing)

The repository includes curated documentation to onboard contributors and guide implementations. Read these first:

- [docs/DEVELOPMENT_WORKFLOW.md](docs/project/DEVELOPMENT_WORKFLOW.md) — Contributor workflow, Copilot customization, and project practices.
- [docs/PROJECT_ARCHITECTURE.md](docs/project/PROJECT_ARCHITECTURE.md) — Architecture decisions and component responsibilities.
- [docs/EPIC-PRD.md](docs/project/EPIC-PRD.md) — Epic-level product requirements and feature breakdowns.
- [docs/TECH-STACK.md](docs/project/TECH-STACK.md) — Recommended packages and versions.
- [docs/Project_Folders_Structure_Blueprint.md](docs/Project_Folders_Structure_Blueprint.md) — Project folder layout and file responsibilities.
- [docs/Logical_Design_Exemplars.md](docs/Logical_Design_Exemplars.md) — Code patterns and testing exemplars.
- [docs/Phase3_Development_Quality_Gates.md](docs/Phase3_Development_Quality_Gates.md) — Implementation backlog and Phase 3 quality gates (new).
- [docs/project_memory.md](docs/project_memory.md) — Project memory, goals, and integration notes.

---

## Integration & Reusability

This project is structured so components can be reused inside a larger application. Key notes:

- Keep domain logic (`models.py`) decoupled from Flask handlers so the model can be imported as a library in other projects.
- Provide small adapter wrappers if embedding into larger systems (e.g., `adapters/` exposing a clear programmatic API).
- Include example import/usage patterns in `README` or `docs/` when creating integration scenarios.

Planned integration items (see docs/Phase3_Development_Quality_Gates.md): adapters, example embeddings, and additional CI checks for cross-platform support (Windows + Linux).

---

## Project Status

 ✅ **Phase 3 COMPLETE**: Core features, Admin UI, and Security implemented.

- **Core**: Article CRUD with atomic file locking.
- **Security**: Session hardening, Password hashing (PBKDF2), CSRF protection.
- **Deployment**: Dockerized with Gunicorn.
- **Quality**: 90%+ Test Coverage.

---

## Contributing

Please follow the conventions in [docs/DEVELOPMENT_WORKFLOW.md](docs/project/DEVELOPMENT_WORKFLOW.md).

- Create a branch per feature: `feature/<short-description>`
- Include tests for new behavior and ensure coverage targets are met locally before opening a PR.

---

## License & Attribution

This mini-project is provided as-is for learning and experimentation.

---

v1.0.0 | Active | Last Updated: Dec 16 2025 - 14:30
