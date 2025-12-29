"""Shared pytest fixtures for typ-tmpl."""

import pytest
from typer.testing import CliRunner

from typ_tmpl.main import app


@pytest.fixture()
def cli_runner() -> CliRunner:
    """Provide a CLI runner for testing Typer commands."""
    return CliRunner()


@pytest.fixture()
def typer_app():
    """Return the Typer application under test."""
    return app


@pytest.fixture()
def mock_storage():
    """Provide a mock storage for testing."""
    from dev.mocks.storage import MockStorage

    return MockStorage()


@pytest.fixture()
def app_with_mock(mock_storage):
    """Return app with mock storage injected via callback override."""
    import typer

    from typ_tmpl.context import AppContext

    # Create a fresh app to avoid state pollution
    test_app = typer.Typer(
        name="typ-tmpl",
        help="A minimal Python CLI template using Typer.",
        no_args_is_help=True,
    )

    @test_app.callback()
    def setup(ctx: typer.Context) -> None:
        ctx.obj = AppContext(storage=mock_storage)

    # Register commands from main app
    from typ_tmpl.main import app

    for command_info in app.registered_commands:
        if command_info.callback:
            test_app.command(
                name=command_info.name,
                help=command_info.help,
                hidden=command_info.hidden,
            )(command_info.callback)

    return test_app
