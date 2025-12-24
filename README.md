# fapi-tmpl

`fapi-tmpl` is a minimal, database-independent FastAPI project template. It provides a clean scaffold with modern dependency injection using FastAPI's `Depends`, protocols for service interfaces, and a factory pattern for services. This enables high extensibility, maintainability, and testability. Includes environment-aware configuration, dockerisation, and a lightweight test suite so you can start new services quickly without dragging in domain-specific code.

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) for dependency management
- (Optional) Docker and Docker Compose

### Local Setup

```shell
just setup
```

This installs dependencies with `uv` and creates a local `.env` file if one does not exist.

### Run the Application (Local, In-Process)

```shell
just dev
```

The service will be available at `http://127.0.0.1:8000/health`.

### Run Tests and Linters

```shell
just test       # full test matrix (local + dockerized)
just local-test # unit + intg (ASGITransport, in-process FastAPI)
just api-test   # dockerized API tests (development target)
just e2e-test   # dockerized production acceptance tests
just check      # ruff format --check, ruff check, and mypy
just fix        # auto-format with ruff format and ruff --fix
```

## 🧱 Project Structure

```
├── dev/
│   └── mocks/
│       └── services/
│           └── mock_greeting_service.py  # Toggleable mock implementation
├── src/
│   └── fapi_tmpl/
│       ├── api/
│       │   ├── main.py      # FastAPI app factory and router registration
│       │   └── router.py    # Health check and greeting endpoints
│       ├── config/
│       │   ├── __init__.py
│       │   └── app_settings.py  # Pydantic settings
│       ├── dependencies.py  # Dependency providers using FastAPI Depends
│       ├── protocols/       # Protocol definitions for service interfaces
│       └── services/        # Concrete service implementations
├── tests/
│   ├── unit/                  # Pure unit tests (no FastAPI)
│   ├── intg/                  # In-process API tests (ASGITransport, no Docker)
│   ├── api/                   # Dockerized API tests (development target)
│   └── e2e/                   # Production-like E2E tests
├── justfile
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── entrypoint.sh
```

## 🐳 Docker Usage

The template assumes Docker is used for:

- Development stacks (`just up`, `just down`, `just rebuild`, `just up-prod`, `just down-prod`, `just rebuild-prod`)
- Dockerized API / E2E tests (`just api-test`, `just e2e-test`)

The primary compose entrypoint is `docker-compose.yml`. See `justfile` for the exact environment variables used for dev vs production stacks.

## 🔧 Configuration

Environment variables are loaded from `.env` (managed by `just setup`):

- `FAPI_TMPL_APP_NAME` – application display name (default `fapi-tmpl`).
- `FAPI_TMPL_USE_MOCK_GREETING` – when `true`, injects the development mock greeting service.
- `FAPI_TMPL_BIND_IP` / `FAPI_TMPL_BIND_PORT` – bind address when running under Docker (defaults `0.0.0.0:8000`).
- `FAPI_TMPL_DEV_PORT` – port used by `just dev` (default `8000`).

## ✅ Endpoints

The template ships with health and greeting endpoints:

```http
GET /health -> {"status": "ok"}
GET /hello/{name} -> {"message": "Hello, {name}"}
```

Use this as a foundation for adding your own routes, dependencies, and persistence layers.
