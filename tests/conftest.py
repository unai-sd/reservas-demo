import os

# Keep the app's own engine away from the developer database during tests.
os.environ.setdefault("RESERVAS_DATABASE_URL", "sqlite://")

from collections.abc import Iterator
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from reservas.clock import get_ahora
from reservas.db import get_session
from reservas.main import app
from reservas.models import Base

# Tuesday 1 September 2026, 10:00. Monday 7 September is a closed day.
AHORA = datetime(2026, 9, 1, 10, 0)


@pytest.fixture
def session_factory() -> Iterator[sessionmaker[Session]]:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine, expire_on_commit=False)
    engine.dispose()


@pytest.fixture
def client(session_factory: sessionmaker[Session]) -> Iterator[TestClient]:
    def _session() -> Iterator[Session]:
        with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = _session
    app.dependency_overrides[get_ahora] = lambda: AHORA
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def mesas(client: TestClient) -> list[dict]:
    datos = [
        {"nombre": "I1", "capacidad": 2},
        {"nombre": "I2", "capacidad": 4},
        {"nombre": "T1", "capacidad": 6, "zona": "terraza"},
    ]
    return [client.post("/mesas", json=d).json() for d in datos]


def reserva(**cambios: object) -> dict:
    base = {
        "nombre_cliente": "Lucía Prieto",
        "telefono": "600 000 001",
        "comensales": 2,
        "fecha": "2026-09-02",
        "hora": "21:00:00",
    }
    return base | cambios
