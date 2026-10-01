"""Which tables are free for a given date and time."""

from datetime import date, time

from sqlalchemy import select
from sqlalchemy.orm import Session

from reservas.models import ESTADO_CONFIRMADA, Mesa, Reserva
from reservas.rules import se_solapan


def mesas_libres(session: Session, fecha: date, hora: time, comensales: int = 1) -> list[Mesa]:
    mesas = session.scalars(
        select(Mesa)
        .where(Mesa.activa.is_(True), Mesa.capacidad >= comensales)
        .order_by(Mesa.capacidad, Mesa.nombre)
    ).all()
    reservas = session.scalars(
        select(Reserva).where(Reserva.fecha == fecha, Reserva.estado == ESTADO_CONFIRMADA)
    ).all()
    ocupadas = {r.mesa_id for r in reservas if se_solapan(r.hora, hora)}
    return [m for m in mesas if m.id not in ocupadas]
