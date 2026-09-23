"""Current time as a dependency, so tests can freeze it."""

from datetime import datetime


def get_ahora() -> datetime:
    return datetime.now()
