from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from reservas.availability import mesas_libres
from reservas.db import get_session
from reservas.rules import franjas_del_dia
from reservas.schemas import Franja

router = APIRouter(prefix="/franjas", tags=["franjas"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("", response_model=list[Franja])
def listar_franjas(
    session: SessionDep,
    fecha: date,
    comensales: Annotated[int, Query(ge=1, le=12)] = 2,
) -> list[Franja]:
    """Time slots of a day with the number of free tables for the party size."""
    return [
        Franja(hora=hora, mesas_libres=len(mesas_libres(session, fecha, hora, comensales)))
        for hora in franjas_del_dia(fecha)
    ]
