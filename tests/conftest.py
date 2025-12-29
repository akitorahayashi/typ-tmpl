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
