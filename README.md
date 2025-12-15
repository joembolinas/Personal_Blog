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
    <a href="https://github.com/yourusername/personal-blog/issues">Technology Stack</a>
    ·
    <a href="https://github.com/yourusername/personal-blog/issues">Project Structure</a>
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

## Getting Started

### Prerequisites
- Python 3.x installed on your machine.

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/personal-blog.git
    cd personal-blog
    ```

2.  **Set up the environment** (Recommended)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Run the application**
    ```bash
    python app.py
    ```

4.  **Access the blog**
    - Guest View: `http://localhost:5000`
    - Admin Panel: `http://localhost:5000/admin`

## Project Structure

```plaintext
/
├── data/               # Article storage (JSON/Markdown files)
├── static/             # CSS stylesheets and images
├── templates/          # HTML templates for pages
├── app.py              # Main application entry point
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Development Workflow

1.  **Plan**: Define the data structure for articles.
2.  **Build**: Implement the file storage system and Python backend.
3.  **Design**: Create HTML templates and style them with CSS.
4.  **Secure**: Add basic authentication for the admin dashboard.
5.  **Test**: Verify create, read, update, and delete (CRUD) operations.

## Coding Standards

- **Python**: Adhere to [PEP 8](https://pep8.org/) guidelines.
- **HTML/CSS**: Maintain semantic HTML and clean, organized CSS classes.
- **Commits**: Use descriptive commit messages.

## Testing

Testing is performed manually during this phase:
- Verify page navigation.
- Validate form submissions (creation and editing).
- Check authentication barriers.

---

<div align="center">
  <sub>Built with ❤️ for the <a href="https://roadmap.sh">roadmap.sh</a> community</sub>
</div>
