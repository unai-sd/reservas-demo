from fastapi.testclient import TestClient

from tests.conftest import reserva


def test_resumen_diario(client: TestClient, mesas: list[dict]) -> None:
    client.post("/reservas", json=reserva(comensales=2, hora="13:30:00"))
    client.post("/reservas", json=reserva(comensales=4, hora="21:00:00"))
    cancelada = client.post("/reservas", json=reserva(comensales=2, hora="21:00:00")).json()
    client.post(f"/reservas/{cancelada['id']}/cancelar")

    resumen = client.get("/resumen", params={"fecha": "2026-09-02"}).json()
    assert resumen["confirmadas"] == 2
    assert resumen["canceladas"] == 1
    assert resumen["comensales"] == 6
    assert resumen["por_servicio"]["comida"] == {"reservas": 1, "comensales": 2}
    assert resumen["por_servicio"]["cena"] == {"reservas": 1, "comensales": 4}
