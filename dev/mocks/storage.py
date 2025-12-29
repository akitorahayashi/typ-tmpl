"""Mock storage implementation for testing."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MockStorage:
    """Mock storage for testing."""

    items: dict[str, str] = field(default_factory=dict)
    calls: list[tuple[str, tuple[Any, ...]]] = field(default_factory=list)

    def add(self, id: str, content: str) -> None:
        """Add a new item."""
        self.calls.append(("add", (id, content)))
        self.items[id] = content

    def list(self) -> list[str]:
        """List all item IDs."""
        self.calls.append(("list", ()))
        return sorted(self.items.keys())

    def delete(self, id: str) -> None:
        """Delete an item."""
        self.calls.append(("delete", (id,)))
        self.items.pop(id, None)

    def exists(self, id: str) -> bool:
        """Check if an item exists."""
        self.calls.append(("exists", (id,)))
        return id in self.items

    def get(self, id: str) -> str | None:
        """Get the content of an item."""
        self.calls.append(("get", (id,)))
        return self.items.get(id)
