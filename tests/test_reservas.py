from fastapi.testclient import TestClient

from reservas.clock import get_ahora
from reservas.main import app
from tests.conftest import AHORA, reserva


def test_asigna_la_mesa_mas_pequena_que_cabe(client: TestClient, mesas: list[dict]) -> None:
    respuesta = client.post("/reservas", json=reserva(comensales=3))
    assert respuesta.status_code == 201
    assert respuesta.json()["mesa_id"] == mesas[1]["id"]
    assert respuesta.json()["estado"] == "confirmada"


def test_mesa_concreta(client: TestClient, mesas: list[dict]) -> None:
    respuesta = client.post("/reservas", json=reserva(mesa_id=mesas[2]["id"]))
    assert respuesta.json()["mesa_id"] == mesas[2]["id"]


def test_sin_mesas_libres(client: TestClient, mesas: list[dict]) -> None:
    assert client.post("/reservas", json=reserva(comensales=6)).status_code == 201
    assert client.post("/reservas", json=reserva(comensales=6)).status_code == 409


def test_reservas_solapadas_no_comparten_mesa(client: TestClient, mesas: list[dict]) -> None:
    primera = client.post("/reservas", json=reserva(mesa_id=mesas[0]["id"], hora="21:00:00"))
    assert primera.status_code == 201
    solapada = client.post("/reservas", json=reserva(mesa_id=mesas[0]["id"], hora="21:30:00"))
    assert solapada.status_code == 409
    libre = client.post("/reservas", json=reserva(mesa_id=mesas[0]["id"], hora="22:30:00"))
    assert libre.status_code == 201


def test_regla_incumplida(client: TestClient, mesas: list[dict]) -> None:
    respuesta = client.post("/reservas", json=reserva(fecha="2026-09-07"))
    assert respuesta.status_code == 422
    assert "cierra" in respuesta.json()["detail"]


def test_listar_por_fecha(client: TestClient, mesas: list[dict]) -> None:
    client.post("/reservas", json=reserva())
    client.post("/reservas", json=reserva(fecha="2026-09-03"))
    assert len(client.get("/reservas", params={"fecha": "2026-09-03"}).json()) == 1
    assert len(client.get("/reservas").json()) == 2


def test_cancelar_libera_la_mesa(client: TestClient, mesas: list[dict]) -> None:
    creada = client.post("/reservas", json=reserva(comensales=6)).json()
    cancelada = client.post(f"/reservas/{creada['id']}/cancelar")
    assert cancelada.json()["estado"] == "cancelada"
    assert client.post(f"/reservas/{creada['id']}/cancelar").status_code == 409
    assert client.post("/reservas", json=reserva(comensales=6)).status_code == 201


def test_no_se_cancela_con_menos_de_dos_horas(client: TestClient, mesas: list[dict]) -> None:
    creada = client.post("/reservas", json=reserva(fecha="2026-09-01", hora="13:00:00")).json()
    assert client.post(f"/reservas/{creada['id']}/cancelar").status_code == 200

    app.dependency_overrides[get_ahora] = lambda: AHORA.replace(hour=11, minute=30)
    otra = client.post("/reservas", json=reserva(fecha="2026-09-01", hora="13:00:00")).json()
    assert client.post(f"/reservas/{otra['id']}/cancelar").status_code == 422


def test_reserva_inexistente(client: TestClient) -> None:
    assert client.get("/reservas/42").status_code == 404
