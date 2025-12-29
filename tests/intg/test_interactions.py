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
        assert "greet" in result.output

    def test_no_args_shows_help(self, cli_runner: CliRunner) -> None:
        """Test that running without arguments shows help."""
        result = cli_runner.invoke(app, [])

        assert "Usage:" in result.output or "typ-tmpl" in result.output

    def test_greet_command(self, cli_runner: CliRunner) -> None:
        """Test that the greet command works."""
        result = cli_runner.invoke(app, ["greet", "World"])

        assert result.exit_code == 0
        assert "Hello, World!" in result.output

    def test_greet_alias(self, cli_runner: CliRunner) -> None:
        """Test that the 'g' alias works."""
        result = cli_runner.invoke(app, ["g", "Alice"])

        assert result.exit_code == 0
        assert "Hello, Alice!" in result.output

    def test_greet_help_shows_argument(self, cli_runner: CliRunner) -> None:
        """Test that greet --help shows name argument."""
        result = cli_runner.invoke(app, ["greet", "--help"])

        assert result.exit_code == 0
        assert "NAME" in result.output or "name" in result.output.lower()

    def test_greet_missing_name_shows_error(self, cli_runner: CliRunner) -> None:
        """Test that missing name argument shows an error."""
        result = cli_runner.invoke(app, ["greet"])

        assert result.exit_code != 0
