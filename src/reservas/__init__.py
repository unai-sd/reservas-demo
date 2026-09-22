"""API de reservas de mesas de Casa Demo."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("reservas-demo")
except PackageNotFoundError:  # pragma: no cover - only when running from a raw checkout
    __version__ = "0.0.0"
