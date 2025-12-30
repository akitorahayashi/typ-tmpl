"""Integration tests for CLI commands."""

from typer.testing import CliRunner

from typ_tmpl.main import app


class TestCLIIntegration:
    """Integration tests for CLI command interactions."""

    def test_version_flag_shows_version(self, cli_runner: CliRunner) -> None:
        """Test that --version flag shows version information."""
        result = cli_runner.invoke(app, ["--version"])

        assert result.exit_code == 0
        assert "typ-tmpl version:" in result.output

    def test_short_version_flag_shows_version(self, cli_runner: CliRunner) -> None:
        """Test that -V flag shows version information."""
        result = cli_runner.invoke(app, ["-V"])

        assert result.exit_code == 0
        assert "typ-tmpl version:" in result.output

    def test_help_flag_shows_help(self, cli_runner: CliRunner) -> None:
        """Test that --help flag shows help information."""
        result = cli_runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "typ-tmpl" in result.output
        assert "add" in result.output
        assert "list" in result.output
        assert "delete" in result.output

    def test_no_args_shows_help(self, cli_runner: CliRunner) -> None:
        """Test that running without arguments shows help."""
        result = cli_runner.invoke(app, [])

        assert "Usage:" in result.output or "typ-tmpl" in result.output


class TestAddCommand:
    """Tests for the add command."""

    def test_add_item(self, cli_runner: CliRunner, app_with_mock, mock_storage) -> None:
        """Test adding an item."""
        result = cli_runner.invoke(
            app_with_mock, ["add", "note1", "-c", "Test content"]
        )

        assert result.exit_code == 0
        assert "Added" in result.output and "note1" in result.output
        assert mock_storage.items["note1"] == "Test content"

    def test_add_alias(
        self, cli_runner: CliRunner, app_with_mock, mock_storage
    ) -> None:
        """Test that 'a' alias works."""
        result = cli_runner.invoke(
            app_with_mock, ["a", "note2", "--content", "More content"]
        )

        assert result.exit_code == 0
        assert "Added" in result.output and "note2" in result.output

    def test_add_duplicate_fails(
        self, cli_runner: CliRunner, app_with_mock, mock_storage
    ) -> None:
        """Test that adding duplicate item fails."""
        mock_storage.items["existing"] = "Old content"

        result = cli_runner.invoke(
            app_with_mock, ["add", "existing", "-c", "New content"]
        )

        assert result.exit_code == 1
        assert "already exists" in result.output


class TestListCommand:
    """Tests for the list command."""

    def test_list_empty(self, cli_runner: CliRunner, app_with_mock) -> None:
        """Test listing when no items exist."""
        result = cli_runner.invoke(app_with_mock, ["list"])

        assert result.exit_code == 0
        assert "No items found" in result.output

    def test_list_items(
        self, cli_runner: CliRunner, app_with_mock, mock_storage
    ) -> None:
        """Test listing items."""
        mock_storage.items["note1"] = "Content 1"
        mock_storage.items["note2"] = "Content 2"

        result = cli_runner.invoke(app_with_mock, ["list"])

        assert result.exit_code == 0
        assert "note1" in result.output
        assert "note2" in result.output

    def test_list_alias(
        self, cli_runner: CliRunner, app_with_mock, mock_storage
    ) -> None:
        """Test that 'ls' alias works."""
        mock_storage.items["item1"] = "Content"

        result = cli_runner.invoke(app_with_mock, ["ls"])

        assert result.exit_code == 0
        assert "item1" in result.output


class TestDeleteCommand:
    """Tests for the delete command."""

    def test_delete_item(
        self, cli_runner: CliRunner, app_with_mock, mock_storage
    ) -> None:
        """Test deleting an item."""
        mock_storage.items["to-delete"] = "Content"

        result = cli_runner.invoke(app_with_mock, ["delete", "to-delete"])

        assert result.exit_code == 0
        assert "Deleted" in result.output and "to-delete" in result.output
        assert "to-delete" not in mock_storage.items

    def test_delete_alias(
        self, cli_runner: CliRunner, app_with_mock, mock_storage
    ) -> None:
        """Test that 'rm' alias works."""
        mock_storage.items["item"] = "Content"

        result = cli_runner.invoke(app_with_mock, ["rm", "item"])

        assert result.exit_code == 0
        assert "Deleted" in result.output and "item" in result.output

    def test_delete_nonexistent_fails(
        self, cli_runner: CliRunner, app_with_mock
    ) -> None:
        """Test that deleting nonexistent item fails."""
        result = cli_runner.invoke(app_with_mock, ["delete", "nonexistent"])

        assert result.exit_code == 1
        assert "not found" in result.output
