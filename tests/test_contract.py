from fastapi.testclient import TestClient

from service import app


def test_api_contract():
    client = TestClient(app)
    assert client.get("/health/live").status_code == 200
    response = client.post("/v1/models", json={"key": "fraud", "payload": {}})
    body = response.json()
    assert response.status_code == 200
    assert body["model"] == "fraud"
    assert body["version"] == "1"
    assert body["stage"] == "registered"
    assert body["evidence"]["decision"] == "ALLOW"
