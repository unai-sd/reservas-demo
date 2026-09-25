"""ORM models: tables (mesas) and bookings (reservas)."""

from datetime import date, datetime, time

from sqlalchemy import Date, DateTime, ForeignKey, String, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

ESTADO_CONFIRMADA = "confirmada"
ESTADO_CANCELADA = "cancelada"


class Base(DeclarativeBase):
    pass


class Mesa(Base):
    __tablename__ = "mesas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(20), unique=True)
    capacidad: Mapped[int]
    zona: Mapped[str] = mapped_column(String(20), default="interior")
    activa: Mapped[bool] = mapped_column(default=True)

    reservas: Mapped[list["Reserva"]] = relationship(back_populates="mesa")


class Reserva(Base):
    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(primary_key=True)
    mesa_id: Mapped[int] = mapped_column(ForeignKey("mesas.id"))
    nombre_cliente: Mapped[str] = mapped_column(String(100))
    telefono: Mapped[str] = mapped_column(String(20))
    comensales: Mapped[int]
    fecha: Mapped[date] = mapped_column(Date)
    hora: Mapped[time] = mapped_column(Time)
    estado: Mapped[str] = mapped_column(String(20), default=ESTADO_CONFIRMADA)
    creada_en: Mapped[datetime] = mapped_column(DateTime)

    mesa: Mapped[Mesa] = relationship(back_populates="reservas")
