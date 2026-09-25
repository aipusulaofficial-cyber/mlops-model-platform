from fastapi.testclient import TestClient
from service import app


def test_api_contract():
    client = TestClient(app)
    assert client.get("/health/live").status_code == 200

    response = client.post(
        "/v1/models",
        json={"key": "fraud", "payload": {}},
    )
    assert response.status_code == 200
    assert response.json() == {
        "model": "fraud",
        "version": "1",
        "stage": "registered",
    }
