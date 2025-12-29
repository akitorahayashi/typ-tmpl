# justfile for typ-tmpl

# default target
default: help

# Show available recipes
help:
    @echo "Usage: just [recipe]"
    @echo "Available recipes:"
    @just --list | tail -n +2 | awk '{printf "  \033[36m%-15s\033[0m %s\n", $1, substr($0, index($0, $2))}'

# Install dependencies
setup:
    @echo "Installing dependencies..."
    @uv sync
    @echo "Done"

# Run the CLI application
run *args:
    @uv run typ-tmpl {{args}}

# Automatically format and fix code
fix:
    @echo "Formatting code..."
    @uv run ruff format .
    @uv run ruff check . --fix

# Run static checks
check:
    @echo "Running checks..."
    @uv run ruff format --check .
    @uv run ruff check .
    @uv run mypy .

# Run tests
test:
    @echo "Running tests..."
    @uv run pytest tests/
    @echo "Done"

# Remove cache files
clean:
    @echo "Cleaning up..."
    @find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    @rm -rf .venv .pytest_cache .ruff_cache .mypy_cache
    @echo "Done"
