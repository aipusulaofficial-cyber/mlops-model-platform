from fastapi.testclient import TestClient
from service import app
def test_api_contract():
 c=TestClient(app);assert c.get("/health/live").status_code==200
 r=c.post("/v1/models",json={"model":"fraud","payload":{}});assert r.status_code==200 and r.json()["status"]=="accepted"
