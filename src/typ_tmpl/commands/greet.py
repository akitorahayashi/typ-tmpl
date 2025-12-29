"""Greet command implementation."""

import typer
from rich.console import Console

console = Console()


def greet(
    name: str = typer.Argument(..., help="Name of the person to greet."),
) -> None:
    """Greet someone by name.

    Examples:
        typ-tmpl greet World
        typ-tmpl g World
    """
    console.print(f"Hello, {name}!")
