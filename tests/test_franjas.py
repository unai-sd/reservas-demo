from fastapi.testclient import TestClient

from tests.conftest import reserva


def test_franjas_con_mesas_libres(client: TestClient, mesas: list[dict]) -> None:
    client.post("/reservas", json=reserva(comensales=2, hora="21:00:00"))
    respuesta = client.get("/franjas", params={"fecha": "2026-09-02", "comensales": 2})
    franjas = {f["hora"]: f["mesas_libres"] for f in respuesta.json()}
    assert len(franjas) == 12
    assert franjas["13:00:00"] == 3
    assert franjas["20:00:00"] == 2
    assert franjas["21:00:00"] == 2
    assert franjas["22:30:00"] == 3


def test_dia_cerrado_sin_franjas(client: TestClient) -> None:
    assert client.get("/franjas", params={"fecha": "2026-09-07"}).json() == []
