"""Business rules of Casa Demo: services, time slots and booking constraints."""

from datetime import date, datetime, time, timedelta

# Opening services: first and last bookable time of each one.
SERVICIOS: dict[str, tuple[time, time]] = {
    "comida": (time(13, 0), time(15, 30)),
    "cena": (time(20, 0), time(22, 30)),
}
INTERVALO_MINUTOS = 30
DURACION_RESERVA_MINUTOS = 90
DIAS_CERRADO = {0}  # Monday
ANTELACION_MAXIMA_DIAS = 60
HORAS_MINIMAS_CANCELACION = 2


class ReglaIncumplida(ValueError):
    """A booking request breaks one of the restaurant rules."""


def franjas_del_dia(fecha: date) -> list[time]:
    if fecha.weekday() in DIAS_CERRADO:
        return []
    franjas: list[time] = []
    for inicio, fin in SERVICIOS.values():
        actual = datetime.combine(fecha, inicio)
        while actual.time() <= fin:
            franjas.append(actual.time())
            actual += timedelta(minutes=INTERVALO_MINUTOS)
    return franjas


def _minutos(hora: time) -> int:
    return hora.hour * 60 + hora.minute


def se_solapan(hora_a: time, hora_b: time) -> bool:
    """Two bookings on the same table overlap if they start less than one booking apart."""
    return abs(_minutos(hora_a) - _minutos(hora_b)) < DURACION_RESERVA_MINUTOS


def validar_nueva_reserva(fecha: date, hora: time, ahora: datetime) -> None:
    if fecha.weekday() in DIAS_CERRADO:
        raise ReglaIncumplida("El restaurante cierra ese día")
    if hora not in franjas_del_dia(fecha):
        raise ReglaIncumplida("La hora no corresponde a ninguna franja de servicio")
    inicio = datetime.combine(fecha, hora)
    if inicio <= ahora:
        raise ReglaIncumplida("No se puede reservar en el pasado")
    if fecha > ahora.date() + timedelta(days=ANTELACION_MAXIMA_DIAS):
        raise ReglaIncumplida(
            f"Solo se admiten reservas con {ANTELACION_MAXIMA_DIAS} días de antelación como máximo"
        )


def puede_cancelarse(fecha: date, hora: time, ahora: datetime) -> bool:
    limite = datetime.combine(fecha, hora) - timedelta(hours=HORAS_MINIMAS_CANCELACION)
    return ahora <= limite
