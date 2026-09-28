from promotion_gate import can_promote


def test_promotion_requires_all_evidence():
    evidence = {"security": True, "quality": True, "cost": True, "provenance": True}
    assert can_promote(evidence, True)
    assert not can_promote({**evidence, "cost": False}, True)
    assert not can_promote(evidence, False)
