# data/

This directory stores article JSON files used by the Personal Blog application.

Policy: tracked content
- The project currently follows the "track content" policy: canonical article files are committed to the repository under `data/` so they can be versioned, reviewed, and restored via git history.

Guidance for maintainers
- When creating articles for the site, add them as `data/{slug}.json` files using the JSON schema defined in `docs/project-specification.md`.
- Ensure `slug` values are lowercase, URL-safe, and unique across files.
- Avoid committing secrets or sensitive information in article JSON files. If you must include confidential data, do NOT commit it — instead store it in a secure external store and reference it via environment variables or adapter services.
- Large binary blobs (images) should not be embedded in JSON; store images in `static/images/` and reference paths from articles.

Security notes
- Do not add passwords, API keys, or private tokens to files under `data/`.
- If article content includes user-supplied HTML or embedded content, ensure sanitization is applied before rendering (see `markdown` + sanitizer pipeline in docs).

Backup and migrations
- For major content migrations, create a `data/migrations/` directory and add a migration script in `scripts/`.
- Keep a `data/README.md` entry documenting migration steps and provide a `scripts/export_content.py` helper if needed.

If you prefer not to track runtime content in the repository, consider switching to the "ignore content" policy: keep `data/` in `.gitignore` and maintain a `seed/` or `content/` folder with example posts for development.
