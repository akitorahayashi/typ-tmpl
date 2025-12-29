# typ-tmpl

## Overview

Minimal Typer CLI template with item CRUD functionality. Demonstrates Pythonic DI via `ctx.obj`, protocols for storage abstraction, and clean architecture.

## CLI Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `typ-tmpl add <id> -c <content>` | `a` | Add a new item |
| `typ-tmpl list` | `ls` | List all items |
| `typ-tmpl delete <id>` | `rm` | Delete an item |

## Package Structure

```
src/typ_tmpl/
├── main.py                 # Typer CLI + Container setup
├── context.py              # AppContext dataclass (DI container)
├── errors.py               # Application errors
├── commands/
│   ├── add.py              # add/a command
│   ├── list.py             # list/ls command
│   └── delete.py           # delete/rm command
├── protocols/
│   └── storage.py          # Storage protocol
└── storage/
    └── filesystem.py       # FilesystemStorage implementation

dev/
└── mocks/
    └── storage.py          # MockStorage for testing
```

## Design Rules

### Dependency Injection

Use Typer's `ctx.obj` for DI:

```python
@app.callback()
def main(ctx: typer.Context) -> None:
    ctx.obj = AppContext(storage=FilesystemStorage())

def add(ctx: typer.Context, id: str, content: str) -> None:
    app_ctx: AppContext = ctx.obj
    app_ctx.storage.add(id, content)
```

### Protocol-Based Abstraction

Define interfaces in `protocols/` for testability:

```python
class Storage(Protocol):
    def add(self, id: str, content: str) -> None: ...
    def list(self) -> list[str]: ...
```

### Testing

- Mock implementations live in `dev/mocks/`
- Use `app_with_mock` fixture for command tests
- Unit tests use `tmp_path` for FilesystemStorage

### Adding New Commands

1. Create command function in `commands/<name>.py`
2. Import and register in `main.py` with alias
3. Access dependencies via `ctx.obj`

### Development

- `just run <args>`: Run CLI in dev mode
- `just test`: Run tests
- `just check`: Format and lint
