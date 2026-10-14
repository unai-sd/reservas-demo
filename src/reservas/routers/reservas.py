from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from reservas.availability import mesas_libres
from reservas.clock import get_ahora
from reservas.db import get_session
from reservas.models import ESTADO_CANCELADA, ESTADO_CONFIRMADA, Reserva
from reservas.rules import ReglaIncumplida, puede_cancelarse, validar_nueva_reserva
from reservas.schemas import ReservaIn, ReservaOut

router = APIRouter(prefix="/reservas", tags=["reservas"])
SessionDep = Annotated[Session, Depends(get_session)]
AhoraDep = Annotated[datetime, Depends(get_ahora)]


@router.get("", response_model=list[ReservaOut])
def listar_reservas(session: SessionDep, fecha: date | None = None) -> list[Reserva]:
    consulta = select(Reserva).order_by(Reserva.fecha, Reserva.hora)
    if fecha is not None:
        consulta = consulta.where(Reserva.fecha == fecha)
    return list(session.scalars(consulta))


@router.post("", response_model=ReservaOut, status_code=status.HTTP_201_CREATED)
def crear_reserva(datos: ReservaIn, session: SessionDep, ahora: AhoraDep) -> Reserva:
    try:
        validar_nueva_reserva(datos.fecha, datos.hora, ahora)
    except ReglaIncumplida as error:
        raise HTTPException(422, str(error)) from error

    libres = mesas_libres(session, datos.fecha, datos.hora, datos.comensales)
    if datos.mesa_id is not None:
        libres = [m for m in libres if m.id == datos.mesa_id]
    if not libres:
        raise HTTPException(status.HTTP_409_CONFLICT, "No hay mesas libres para esa franja")

    reserva = Reserva(
        mesa_id=libres[0].id,
        nombre_cliente=datos.nombre_cliente,
        telefono=datos.telefono,
        comensales=datos.comensales,
        fecha=datos.fecha,
        hora=datos.hora,
        estado=ESTADO_CONFIRMADA,
        creada_en=ahora,
    )
    session.add(reserva)
    session.commit()
    return reserva


@router.get("/{reserva_id}", response_model=ReservaOut)
def obtener_reserva(reserva_id: int, session: SessionDep) -> Reserva:
    reserva = session.get(Reserva, reserva_id)
    if reserva is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Reserva no encontrada")
    return reserva


@router.post("/{reserva_id}/cancelar", response_model=ReservaOut)
def cancelar_reserva(reserva_id: int, session: SessionDep, ahora: AhoraDep) -> Reserva:
    reserva = obtener_reserva(reserva_id, session)
    if reserva.estado == ESTADO_CANCELADA:
        raise HTTPException(status.HTTP_409_CONFLICT, "La reserva ya estaba cancelada")
    if not puede_cancelarse(reserva.fecha, reserva.hora, ahora):
        raise HTTPException(
            422,
            "Las reservas solo se pueden cancelar hasta 2 horas antes",
        )
    reserva.estado = ESTADO_CANCELADA
    session.commit()
    return reserva
