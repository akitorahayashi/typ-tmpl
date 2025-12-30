"""Unit tests for AppContext."""

from typ_tmpl.context import AppContext


class TestAppContext:
    """Tests for AppContext."""

    def test_context_holds_storage(self) -> None:
        """Test that context can hold a storage instance."""
        from dev.mocks.storage import MockStorage

        mock = MockStorage()
        ctx = AppContext(storage=mock)

        assert ctx.storage is mock
