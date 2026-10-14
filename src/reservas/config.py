"""Runtime configuration read from environment variables."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str


def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv("RESERVAS_DATABASE_URL", "sqlite:///./reservas.db"),
    )
