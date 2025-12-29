# typ-tmpl

## Overview

Minimal Typer CLI template. Clean starting point for new CLI tools.

## CLI Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `typ-tmpl greet <name>` | `g` | Greet someone by name |

## Package Structure

```
src/typ_tmpl/
├── main.py           # Typer CLI entry point
└── commands/
    └── greet.py      # greet/g command
```

## Design Rules

### Command Registration

Commands are simple functions registered in `main.py`:

```python
app.command(name="greet", help="... [aliases: g]")(greet)
app.command(name="g", hidden=True)(greet)
```

### Adding New Commands

1. Create command function in `commands/<name>.py`
2. Import and register in `main.py` with alias

### Development

- `just run <args>`: Run CLI in dev mode
- `just test`: Run tests
- `just check`: Format and lint
