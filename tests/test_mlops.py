from mlops_platform import *
import pytest
def test_promotion_state_machine_and_gate():
    r = Registry()
    r.register(ModelVersion("m", "1", "uri", {"quality": 0.9}))
    for s in [Stage.VALIDATED, Stage.STAGING, Stage.PRODUCTION]:
        r.promote("m", "1", s)
    assert r._items[("m", "1")].stage is Stage.PRODUCTION
def test_quality_gate():
    r = Registry()
    r.register(ModelVersion("m", "1", "u", {"quality": 0.2}))
    r.promote("m", "1", Stage.VALIDATED)
    r.promote("m", "1", Stage.STAGING)
    with pytest.raises(PromotionError):
        r.promote("m", "1", Stage.PRODUCTION)
def test_invalid_transition():
    r = Registry()
    r.register(ModelVersion("m", "1", "u", {"quality": 1}))
    with pytest.raises(PromotionError):
        r.promote("m", "1", Stage.PRODUCTION)
