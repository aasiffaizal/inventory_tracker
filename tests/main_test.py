from fastapi.testclient import TestClient


def test_root_returns_200(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
