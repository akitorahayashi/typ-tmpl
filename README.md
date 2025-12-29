# typ-tmpl

Minimal Python CLI template using Typer.

## Installation

### Install with pipx

```sh
pipx install git+https://github.com/akitorahayashi/typ-tmpl.git
```

After installation:

```sh
typ-tmpl --version
typ-tmpl --help
typ-tmpl greet World
```

## Development

### Setup

```sh
git clone https://github.com/akitorahayashi/typ-tmpl.git
cd typ-tmpl
uv sync
```

### Run

```sh
uv run typ-tmpl --help
uv run typ-tmpl greet World
uv run typ-tmpl g World          # alias
```

### Test and Lint

```sh
just test    # run tests
just check   # ruff format --check, ruff check, mypy
just fix     # auto-format
```

## Project Structure

```
typ-tmpl/
├── src/typ_tmpl/
│   ├── __init__.py
│   ├── __main__.py       # module entry point
│   ├── main.py           # Typer app definition
│   └── commands/
│       └── greet.py      # greet/g command
├── tests/
├── justfile
└── pyproject.toml
```

## Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `typ-tmpl greet <name>` | `g` | Greet someone by name |
