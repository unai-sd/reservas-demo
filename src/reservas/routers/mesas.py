from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from reservas.db import get_session
from reservas.models import Mesa
from reservas.schemas import MesaIn, MesaOut

router = APIRouter(prefix="/mesas", tags=["mesas"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("", response_model=list[MesaOut])
def listar_mesas(session: SessionDep) -> list[Mesa]:
    return list(session.scalars(select(Mesa).order_by(Mesa.nombre)))


@router.post("", response_model=MesaOut, status_code=status.HTTP_201_CREATED)
def crear_mesa(datos: MesaIn, session: SessionDep) -> Mesa:
    if session.scalar(select(Mesa).where(Mesa.nombre == datos.nombre)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe una mesa con ese nombre")
    mesa = Mesa(**datos.model_dump())
    session.add(mesa)
    session.commit()
    return mesa


@router.get("/{mesa_id}", response_model=MesaOut)
def obtener_mesa(mesa_id: int, session: SessionDep) -> Mesa:
    mesa = session.get(Mesa, mesa_id)
    if mesa is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Mesa no encontrada")
    return mesa


@router.post("/{mesa_id}/desactivar", response_model=MesaOut)
def desactivar_mesa(mesa_id: int, session: SessionDep) -> Mesa:
    mesa = obtener_mesa(mesa_id, session)
    mesa.activa = False
    session.commit()
    return mesa
