from fastapi.testclient import TestClient


def test_crear_y_listar_mesas(client: TestClient) -> None:
    respuesta = client.post("/mesas", json={"nombre": "I1", "capacidad": 4})
    assert respuesta.status_code == 201
    assert respuesta.json()["zona"] == "interior"
    assert [m["nombre"] for m in client.get("/mesas").json()] == ["I1"]


def test_nombre_de_mesa_unico(client: TestClient) -> None:
    client.post("/mesas", json={"nombre": "I1", "capacidad": 4})
    assert client.post("/mesas", json={"nombre": "I1", "capacidad": 2}).status_code == 409


def test_capacidad_valida(client: TestClient) -> None:
    assert client.post("/mesas", json={"nombre": "X", "capacidad": 0}).status_code == 422


def test_mesa_inexistente(client: TestClient) -> None:
    assert client.get("/mesas/99").status_code == 404


def test_desactivar_mesa(client: TestClient, mesas: list[dict]) -> None:
    respuesta = client.post(f"/mesas/{mesas[0]['id']}/desactivar")
    assert respuesta.json()["activa"] is False


def test_salud(client: TestClient) -> None:
    assert client.get("/salud").json()["estado"] == "ok"
