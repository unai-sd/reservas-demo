"""Database engine and session handling (SQLite through SQLAlchemy 2)."""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from reservas.config import get_settings
from reservas.models import Base


def make_engine(url: str) -> Engine:
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=connect_args)


engine = make_engine(get_settings().database_url)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def init_db(bind: Engine = engine) -> None:
    """Create tables if they do not exist (the project has no migrations yet)."""
    Base.metadata.create_all(bind)


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session
