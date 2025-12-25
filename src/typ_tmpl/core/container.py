"""Dependency injection container for the Typer CLI application."""

from dataclasses import dataclass

from typ_tmpl.config.settings import AppSettings
from typ_tmpl.protocols.greeting_service_protocol import GreetingServiceProtocol


@dataclass
class AppContext:
    """Application context holding settings and service instances."""

    settings: AppSettings
    greeting_service: GreetingServiceProtocol


def create_container(settings: AppSettings | None = None) -> AppContext:
    """
    Create and return the application context with all dependencies wired.

    Args:
        settings: Optional pre-configured settings. If None, loads from environment.

    Returns:
        AppContext with settings and services initialized.
    """
    if settings is None:
        settings = AppSettings()

    if settings.use_mock_greeting:
        from dev.mocks.services.mock_greeting_service import MockGreetingService

        service: GreetingServiceProtocol = MockGreetingService()
    else:
        from typ_tmpl.services.greeting_service import GreetingService

        service = GreetingService()

    return AppContext(settings=settings, greeting_service=service)
