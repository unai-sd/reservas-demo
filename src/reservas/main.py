"""FastAPI application entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from reservas import __version__
from reservas.db import init_db
from reservas.routers import mesas


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(title="Reservas Casa Demo", version=__version__, lifespan=lifespan)
app.include_router(mesas.router)


@app.get("/salud", tags=["sistema"])
def salud() -> dict[str, str]:
    return {"estado": "ok", "version": __version__}
