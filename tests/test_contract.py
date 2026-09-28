from fastapi.testclient import TestClient
from service import app

def test_api_contract():
    c=TestClient(app)
    assert c.get("/health/live").status_code == 200
    r=c.post("/v1/models",json={"key":"fraud","payload":{}})
    b=r.json()
    assert r.status_code == 200
    assert b["model"] == "fraud"
    assert b["version"] == "1"
    assert b["stage"] == "registered"
    assert b["evidence"]["decision"] == "ALLOW"
