from datetime import date, datetime, time

import pytest

from reservas.rules import (
    ReglaIncumplida,
    franjas_del_dia,
    puede_cancelarse,
    se_solapan,
    validar_nueva_reserva,
)

AHORA = datetime(2026, 9, 1, 10, 0)


def test_franjas_de_un_dia_abierto() -> None:
    franjas = franjas_del_dia(date(2026, 9, 2))
    assert franjas[0] == time(13, 0)
    assert franjas[-1] == time(22, 30)
    assert len(franjas) == 12


def test_lunes_cerrado() -> None:
    assert franjas_del_dia(date(2026, 9, 7)) == []
    with pytest.raises(ReglaIncumplida, match="cierra"):
        validar_nueva_reserva(date(2026, 9, 7), time(21, 0), AHORA)


@pytest.mark.parametrize(
    ("a", "b", "esperado"),
    [
        (time(21, 0), time(21, 0), True),
        (time(13, 0), time(20, 0), False),
    ],
)
def test_solapamiento(a: time, b: time, esperado: bool) -> None:
    assert se_solapan(a, b) is esperado


def test_hora_fuera_de_franja() -> None:
    with pytest.raises(ReglaIncumplida, match="franja"):
        validar_nueva_reserva(date(2026, 9, 2), time(18, 0), AHORA)


def test_no_se_reserva_en_el_pasado() -> None:
    with pytest.raises(ReglaIncumplida, match="pasado"):
        validar_nueva_reserva(date(2026, 8, 30), time(21, 0), AHORA)


def test_antelacion_maxima() -> None:
    with pytest.raises(ReglaIncumplida, match="antelación"):
        validar_nueva_reserva(date(2026, 12, 1), time(21, 0), AHORA)


def test_cancelacion_hasta_dos_horas_antes() -> None:
    assert puede_cancelarse(date(2026, 9, 1), time(13, 0), AHORA)
    assert not puede_cancelarse(date(2026, 9, 1), time(11, 30), AHORA)
