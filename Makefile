.PHONY: dev run test lint format build docker-run eval

dev:        ## create venv, install deps, install pre-commit
	poetry install || true
	poetry run pre-commit install || true

run:        ## run MCP server locally
	poetry run python -m tools.mcp_server.app

test:       ## run unit tests
	poetry run pytest -q

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

eval:       ## smoke tests (50 add, 10 malformed)
	poetry run python scripts/run_smoke.py && poetry run python scripts/run_malformed.py

build:
	docker build -t ai-agents:week0 .

docker-run:
	docker run --rm -p 8000:8000 ai-agents:week0

adk-web:
	poetry run adk web agents/

mcp-stdio:
	poetry run python -m tools.mcp_server.mcp_stdio

eval-mcp:
	MODE=mcp poetry run python scripts/run_smoke.py
