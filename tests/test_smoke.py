from runtime_evidence import runtime_evidence
import time

def test_platform_contract_smoke():
    e=runtime_evidence(request_id="test",stage="model",decision="ALLOW",started=time.perf_counter())
    assert e["request_id"] == "test"
    assert e["latency_ms"] >= 0
