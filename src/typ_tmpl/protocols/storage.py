"""Storage protocol definition."""

from typing import Protocol


class Storage(Protocol):
    """Storage abstraction for item persistence."""

    def add(self, id: str, content: str) -> None:
        """Add a new item.

        Args:
            id: Unique identifier for the item.
            content: Content of the item.
        """
        ...

    def list(self) -> list[str]:
        """List all item IDs.

        Returns:
            List of item IDs.
        """
        ...

    def delete(self, id: str) -> None:
        """Delete an item.

        Args:
            id: Identifier of the item to delete.
        """
        ...

    def exists(self, id: str) -> bool:
        """Check if an item exists.

        Args:
            id: Identifier to check.

        Returns:
            True if item exists, False otherwise.
        """
        ...

    def get(self, id: str) -> str | None:
        """Get the content of an item.

        Args:
            id: Identifier of the item.

        Returns:
            Content of the item, or None if not found.
        """
        ...
