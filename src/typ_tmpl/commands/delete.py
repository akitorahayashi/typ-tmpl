"""Delete command implementation."""

import typer
from rich.console import Console

from typ_tmpl.context import AppContext
from typ_tmpl.errors import ItemNotFoundError

console = Console()


def delete(
    ctx: typer.Context,
    id: str = typer.Argument(..., help="Identifier of the item to delete."),
) -> None:
    """Delete an item.

    Examples:
        typ-tmpl delete note1
        typ-tmpl rm note2
    """
    app_ctx: AppContext = ctx.obj

    try:
        app_ctx.storage.delete(id)
        console.print(f"[green]Deleted '{id}'[/]")
    except ItemNotFoundError:
        console.print(f"[red]Error: Item '{id}' not found[/]")
        raise typer.Exit(1)
