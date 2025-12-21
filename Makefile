
# Minimal Makefile for Personal Blog
# Windows Note: To run this, install 'make' or use WSL/Git Bash.
# Alternatively, check 'docs/DEVELOPMENT_WORKFLOW.md' for direct commands.

.PHONY: install test run docker-build docker-run

install:
	pip install -r requirements.txt

test:
	pytest -q

run:
	flask --app app:create_app run --debug

docker-build:
	docker build -t personal-blog .

docker-run:
	docker run -p 8000:8000 -v "${PWD}/data:/app/data" personal-blog
