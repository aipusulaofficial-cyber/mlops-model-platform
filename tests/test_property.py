from hypothesis import given,strategies as st
from fastapi.testclient import TestClient
from service import app
@given(st.text(min_size=1,max_size=50))
def test_model_identifier(value):assert TestClient(app).post("/v1/models",json={"model":value}).status_code==200
