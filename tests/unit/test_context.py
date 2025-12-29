"""Unit tests for AppContext."""

from typ_tmpl.context import AppContext


class TestAppContext:
    """Tests for AppContext."""

    def test_context_holds_storage(self) -> None:
        """Test that context can hold a storage instance."""
        # Import here to avoid path issues
        import sys
        from pathlib import Path

        dev_path = Path(__file__).parent.parent.parent / "dev"
        if str(dev_path.parent) not in sys.path:
            sys.path.insert(0, str(dev_path.parent))

        from dev.mocks.storage import MockStorage

        mock = MockStorage()
        ctx = AppContext(storage=mock)

        assert ctx.storage is mock
