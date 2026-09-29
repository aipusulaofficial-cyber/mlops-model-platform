import math

import pytest

from mlops_platform import ModelVersion, Registry, Stage
from persistent_registry import PersistentRegistry


@pytest.mark.parametrize("quality", [math.nan, math.inf, -0.1, 1.1, "high", None])
def test_production_gate_fails_closed_in_memory_and_persistent(tmp_path, quality):
    model = ModelVersion("model", "v1", "artifact", {"quality": quality}, Stage.STAGING)

    memory = Registry()
    memory.register(model)
    with pytest.raises(ValueError, match="quality gate"):
        # Memory registry raises PromotionError, not ValueError.
        memory.promote("model", "v1", Stage.PRODUCTION)

    persistent = PersistentRegistry(str(tmp_path / "models.db"))
    persistent.register(model)
    with pytest.raises(ValueError, match="quality gate"):
        persistent.promote("model", "v1", Stage.PRODUCTION)
    assert persistent.get("model", "v1").stage == Stage.STAGING


def test_valid_quality_can_promote(tmp_path):
    model = ModelVersion("model", "v1", "artifact", {"quality": 0.91}, Stage.STAGING)
    memory = Registry()
    memory.register(model)
    assert memory.promote("model", "v1", Stage.PRODUCTION).stage == Stage.PRODUCTION
    persistent = PersistentRegistry(str(tmp_path / "models.db"))
    persistent.register(model)
    assert persistent.promote("model", "v1", Stage.PRODUCTION).stage == Stage.PRODUCTION
