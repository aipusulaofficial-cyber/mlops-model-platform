from hypothesis import given, strategies as st
from fastapi.testclient import TestClient
from service import app

c = TestClient(app)


def test_contract():
    assert c.get("/health/live").status_code == 200


@given(
    st.text(
        alphabet=st.characters(blacklist_categories=("Cs",)), min_size=1, max_size=32
    )
)


def test_property(v):
    assert (
        c.post("/v1/models", json={"key": v, "payload": {"version": v}}).status_code
        == 200
    )
