import pytest

from mlops_platform import ModelVersion, Stage
from persistent_registry import PersistentRegistry


@pytest.mark.parametrize("quality", [float("nan"), float("inf"), 0.5, 1.5, "high"])
def test_production_promotion_rejects_invalid_quality(tmp_path, quality):
    registry = PersistentRegistry(str(tmp_path / "models.db"))
    model = ModelVersion("demo", "v1", "file://model", {"quality": quality}, Stage.REGISTERED)
    registry.register(model)
    registry.promote("demo", "v1", Stage.VALIDATED)
    registry.promote("demo", "v1", Stage.STAGING)
    with pytest.raises(ValueError):
        registry.promote("demo", "v1", Stage.PRODUCTION)
