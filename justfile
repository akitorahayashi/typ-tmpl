# ==============================================================================
# justfile for fapi-tmpl automation
# ==============================================================================

set dotenv-load

APP_NAME := env("FAPI_TMPL_APP_NAME", "fapi-tmpl")
HOST_IP := env("FAPI_TMPL_BIND_IP", "127.0.0.1")
DEV_PORT := env("FAPI_TMPL_DEV_PORT", "8000")

DEV_COMPOSE_PROJECT := env("FAPI_TMPL_DEV_PROJECT_NAME", "fapi-tmpl-dev")
PROD_COMPOSE_PROJECT := env("FAPI_TMPL_PROD_PROJECT_NAME", "fapi-tmpl-prod")

# default target
default: help

# Show available recipes
help:
    @echo "Usage: just [recipe]"
    @echo "Available recipes:"
    @just --list | tail -n +2 | awk '{printf "  \033[36m%-20s\033[0m %s\n", $1, substr($0, index($0, $2))}'

# ==============================================================================
# Environment Setup
# ==============================================================================

# Initialize project: install dependencies and create the .env file
setup:
    @echo "🐍 Installing python dependencies with uv..."
    @uv sync
    @echo "Creating environment file..."
    @if [ ! -f .env ] && [ -f .env.example ]; then \
        echo "Creating .env from .env.example..."; \
        cp .env.example .env; \
        echo "✅ Environment file created (.env)"; \
    else \
        echo ".env already exists. Skipping creation."; \
    fi

# ==============================================================================
# Development Environment Commands
# ==============================================================================

# Run local development server (in-process FastAPI, no Docker)
dev:
    @echo "Starting local development server..."
    @uv run uvicorn fapi_tmpl.api.main:app --reload --host {{HOST_IP}} --port {{DEV_PORT}}

# Start development stack (development target)
up:
    @echo "Starting development stack..."
    @COMPOSE_PROJECT_NAME={{DEV_COMPOSE_PROJECT}} FAPI_TMPL_BUILD_TARGET=development docker compose up -d

# Stop development stack
down:
    @echo "Stopping development stack..."
    @COMPOSE_PROJECT_NAME={{DEV_COMPOSE_PROJECT}} docker compose down --remove-orphans

# Rebuild and restart development stack
rebuild:
    @echo "Rebuilding development stack..."
    @COMPOSE_PROJECT_NAME={{DEV_COMPOSE_PROJECT}} docker compose down --remove-orphans
    @COMPOSE_PROJECT_NAME={{DEV_COMPOSE_PROJECT}} FAPI_TMPL_BUILD_TARGET=development docker compose build --no-cache
    @COMPOSE_PROJECT_NAME={{DEV_COMPOSE_PROJECT}} FAPI_TMPL_BUILD_TARGET=development docker compose up -d

# Start production stack (production target)
up-prod:
    @echo "Starting production stack..."
    @COMPOSE_PROJECT_NAME={{PROD_COMPOSE_PROJECT}} FAPI_TMPL_BUILD_TARGET=production docker compose up -d

# Stop production stack
down-prod:
    @echo "Stopping production stack..."
    @COMPOSE_PROJECT_NAME={{PROD_COMPOSE_PROJECT}} docker compose down --remove-orphans

# Rebuild and restart production stack
rebuild-prod:
    @echo "Rebuilding production stack..."
    @COMPOSE_PROJECT_NAME={{PROD_COMPOSE_PROJECT}} docker compose down --remove-orphans
    @COMPOSE_PROJECT_NAME={{PROD_COMPOSE_PROJECT}} FAPI_TMPL_BUILD_TARGET=production docker compose build --no-cache
    @COMPOSE_PROJECT_NAME={{PROD_COMPOSE_PROJECT}} FAPI_TMPL_BUILD_TARGET=production docker compose up -d

# ==============================================================================
# CODE QUALITY
# ==============================================================================

# Automatically format and fix code (Ruff)
fix:
    @echo "🔧 Formatting and fixing code..."
    @uv run ruff format .
    @uv run ruff check . --fix

# Run static checks (Ruff, Mypy)
check: fix
    @echo "🔍 Running static checks..."
    @uv run ruff format --check .
    @uv run ruff check .
    @uv run mypy .

# ==============================================================================
# TESTING
# ==============================================================================

# Run complete test suite
test:
    @just local-test
    @just docker-test
    @echo "✅ All tests passed!"

# Run lightweight local (in-process) test suite
local-test:
    @just unit-test
    @just intg-test
    @echo "✅ All local tests passed!"

# Run unit tests
unit-test:
    @echo "🚀 Running unit tests..."
    @uv run pytest tests/unit

# Run integration tests (in-process FastAPI with ASGITransport)
intg-test:
    @echo "🚀 Running integration tests..."
    @uv run pytest tests/intg

# Run all Docker-based tests
docker-test:
    @just api-test
    @just e2e-test
    @echo "✅ All Docker tests passed!"

# Run dockerized API tests against development target
api-test:
    @echo "🚀 Building image for dockerized API tests (development target)..."
    @docker build --target development -t fapi-tmpl-e2e:dev .
    @echo "🚀 Running dockerized API tests (development target)..."
    @FAPI_TMPL_E2E_IMAGE=fapi-tmpl-e2e:dev uv run pytest tests/api

# Run e2e tests against production-like target
e2e-test:
    @echo "🚀 Building image for production acceptance tests..."
    @docker build --target production -t fapi-tmpl-e2e:prod .
    @echo "🚀 Running production acceptance tests..."
    @FAPI_TMPL_E2E_IMAGE=fapi-tmpl-e2e:prod uv run pytest tests/e2e

# ==============================================================================
# CLEANUP
# ==============================================================================

# Remove __pycache__ and .venv to make project lightweight
clean:
    @echo "🧹 Cleaning up project..."
    @find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    @rm -rf .venv
    @rm -rf .pytest_cache
    @rm -rf .ruff_cache
    @rm -rf .aider.tags.cache.v4
    @rm -rf .serena/cache
    @rm -rf .uv-cache
    @rm -rf .tmp
    @echo "✅ Cleanup completed"
