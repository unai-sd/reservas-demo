"""Request and response bodies of the public API."""

from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, Field


class MesaIn(BaseModel):
    nombre: str = Field(min_length=1, max_length=20)
    capacidad: int = Field(ge=1, le=12)
    zona: str = Field(default="interior", pattern="^(interior|terraza)$")


class MesaOut(MesaIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activa: bool


class ReservaIn(BaseModel):
    nombre_cliente: str = Field(min_length=2, max_length=100)
    telefono: str = Field(pattern=r"^\+?[0-9 ]{9,15}$")
    comensales: int = Field(ge=1, le=12)
    fecha: date
    hora: time
    mesa_id: int | None = None


class ReservaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    mesa_id: int
    nombre_cliente: str
    telefono: str
    comensales: int
    fecha: date
    hora: time
    estado: str
    creada_en: datetime
