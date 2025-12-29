"""Filesystem-based storage implementation."""

from pathlib import Path


class FilesystemStorage:
    """Storage implementation using filesystem."""

    def __init__(self, base_dir: Path | None = None) -> None:
        """Initialize filesystem storage.

        Args:
            base_dir: Base directory for storing items.
                      Defaults to ~/.config/typ-tmpl/items
        """
        if base_dir is None:
            base_dir = Path.home() / ".config" / "typ-tmpl" / "items"
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _item_path(self, id: str) -> Path:
        """Get path for an item."""
        return self.base_dir / f"{id}.txt"

    def add(self, id: str, content: str) -> None:
        """Add a new item.

        Args:
            id: Unique identifier for the item.
            content: Content of the item.
        """
        path = self._item_path(id)
        path.write_text(content)

    def list(self) -> list[str]:
        """List all item IDs.

        Returns:
            List of item IDs sorted alphabetically.
        """
        items = [p.stem for p in self.base_dir.glob("*.txt")]
        return sorted(items)

    def delete(self, id: str) -> None:
        """Delete an item.

        Args:
            id: Identifier of the item to delete.
        """
        path = self._item_path(id)
        if path.exists():
            path.unlink()

    def exists(self, id: str) -> bool:
        """Check if an item exists.

        Args:
            id: Identifier to check.

        Returns:
            True if item exists, False otherwise.
        """
        return self._item_path(id).exists()

    def get(self, id: str) -> str | None:
        """Get the content of an item.

        Args:
            id: Identifier of the item.

        Returns:
            Content of the item, or None if not found.
        """
        path = self._item_path(id)
        if path.exists():
            return path.read_text()
        return None
