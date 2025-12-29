"""Add command implementation."""

import typer
from rich.console import Console

from typ_tmpl.context import AppContext

console = Console()


def add(
    ctx: typer.Context,
    id: str = typer.Argument(..., help="Unique identifier for the item."),
    content: str = typer.Option(..., "--content", "-c", help="Content of the item."),
) -> None:
    """Add a new item.

    Examples:
        typ-tmpl add note1 -c "My first note"
        typ-tmpl a note2 --content "Another note"
    """
    app_ctx: AppContext = ctx.obj

    if app_ctx.storage.exists(id):
        console.print(f"[red]Error: Item '{id}' already exists[/]")
        raise typer.Exit(1)

    app_ctx.storage.add(id, content)
    console.print(f"[green]Added '{id}'[/]")
