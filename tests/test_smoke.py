import time

from runtime_evidence import runtime_evidence


def test_platform_contract_smoke():
    evidence = runtime_evidence(request_id="test", stage="model", decision="ALLOW", started=time.perf_counter())
    assert evidence["request_id"] == "test"
    assert evidence["latency_ms"] >= 0
