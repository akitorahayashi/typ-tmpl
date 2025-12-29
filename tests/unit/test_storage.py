"""Unit tests for storage implementations."""

from pathlib import Path

import pytest

from typ_tmpl.storage.filesystem import FilesystemStorage


class TestFilesystemStorage:
    """Tests for FilesystemStorage."""

    @pytest.fixture
    def storage(self, tmp_path: Path) -> FilesystemStorage:
        """Create a FilesystemStorage with a temp directory."""
        return FilesystemStorage(base_dir=tmp_path)

    def test_add_creates_file(self, storage: FilesystemStorage) -> None:
        """Test that add creates a file."""
        storage.add("test-item", "Test content")

        assert (storage.base_dir / "test-item.txt").exists()
        assert (storage.base_dir / "test-item.txt").read_text() == "Test content"

    def test_list_returns_item_ids(self, storage: FilesystemStorage) -> None:
        """Test that list returns item IDs."""
        storage.add("item1", "Content 1")
        storage.add("item2", "Content 2")

        items = storage.list()

        assert items == ["item1", "item2"]

    def test_list_empty(self, storage: FilesystemStorage) -> None:
        """Test that list returns empty list when no items."""
        items = storage.list()

        assert items == []

    def test_delete_removes_file(self, storage: FilesystemStorage) -> None:
        """Test that delete removes the file."""
        storage.add("to-delete", "Content")
        assert storage.exists("to-delete")

        storage.delete("to-delete")

        assert not storage.exists("to-delete")

    def test_delete_nonexistent_is_noop(self, storage: FilesystemStorage) -> None:
        """Test that deleting nonexistent item doesn't raise."""
        storage.delete("nonexistent")  # Should not raise

    def test_exists_true(self, storage: FilesystemStorage) -> None:
        """Test that exists returns True for existing item."""
        storage.add("existing", "Content")

        assert storage.exists("existing") is True

    def test_exists_false(self, storage: FilesystemStorage) -> None:
        """Test that exists returns False for nonexistent item."""
        assert storage.exists("nonexistent") is False

    def test_get_returns_content(self, storage: FilesystemStorage) -> None:
        """Test that get returns item content."""
        storage.add("item", "Test content")

        content = storage.get("item")

        assert content == "Test content"

    def test_get_nonexistent_returns_none(self, storage: FilesystemStorage) -> None:
        """Test that get returns None for nonexistent item."""
        content = storage.get("nonexistent")

        assert content is None
