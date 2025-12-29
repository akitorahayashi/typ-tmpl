"""Application context for dependency injection."""

from dataclasses import dataclass

from typ_tmpl.protocols.storage import Storage


@dataclass
class AppContext:
    """Application context holding dependencies."""

    storage: Storage
