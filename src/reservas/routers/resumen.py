from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from reservas.db import get_session
from reservas.models import ESTADO_CANCELADA, ESTADO_CONFIRMADA, Reserva
from reservas.rules import SERVICIOS

router = APIRouter(prefix="/resumen", tags=["resumen"])
SessionDep = Annotated[Session, Depends(get_session)]


class ResumenServicio(BaseModel):
    reservas: int = 0
    comensales: int = 0


class ResumenDiario(BaseModel):
    fecha: date
    confirmadas: int
    canceladas: int
    comensales: int
    por_servicio: dict[str, ResumenServicio]


@router.get("", response_model=ResumenDiario)
def resumen_diario(session: SessionDep, fecha: date) -> ResumenDiario:
    """Daily summary for the kitchen: bookings and guests per service."""
    reservas = session.scalars(select(Reserva).where(Reserva.fecha == fecha)).all()
    confirmadas = [r for r in reservas if r.estado == ESTADO_CONFIRMADA]
    por_servicio = {nombre: ResumenServicio() for nombre in SERVICIOS}
    for reserva in confirmadas:
        for nombre, (inicio, fin) in SERVICIOS.items():
            if inicio <= reserva.hora <= fin:
                por_servicio[nombre].reservas += 1
                por_servicio[nombre].comensales += reserva.comensales
    return ResumenDiario(
        fecha=fecha,
        confirmadas=len(confirmadas),
        canceladas=sum(1 for r in reservas if r.estado == ESTADO_CANCELADA),
        comensales=sum(r.comensales for r in confirmadas),
        por_servicio=por_servicio,
    )
