import logging
import time

from fastapi import FastAPI, HTTPException, Request as FastAPIRequest
from opentelemetry import trace
from pydantic import BaseModel, Field

from model_domain import ModelVersion
from observability import PrincipalObservabilityMiddleware
from runtime_evidence import request_id_from_headers, runtime_evidence

try:
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    p = TracerProvider(resource=Resource.create({"service.name": "mlops-model-platform"}))
    p.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(p)
except (ImportError, RuntimeError) as exc:
    logging.getLogger(__name__).warning("OpenTelemetry setup failed: %s", exc)

app = FastAPI(title="mlops-model-platform", version="1.0.0")
tracer = trace.get_tracer("mlops-model-platform")
app.add_middleware(PrincipalObservabilityMiddleware)

class ModelPayload(BaseModel):
    version: str = Field(default="1", min_length=1, max_length=64)
class Request(BaseModel):
    key: str = Field(min_length=1, max_length=128)
    payload: ModelPayload = Field(default_factory=ModelPayload)

@app.get("/health/live")
def live(): return {"status": "ok"}
@app.get("/health/ready")
def ready(): return {"status": "ready"}

@app.post("/v1/models")
def handle(r: Request, http_request: FastAPIRequest):
    started = time.perf_counter(); request_id = request_id_from_headers(http_request.headers)
    with tracer.start_as_current_span("mlops-model-platform.domain"):
        try:
            m = ModelVersion(r.key, r.payload.version)
            return {"model": m.name, "version": m.version, "stage": m.stage,
                    "evidence": runtime_evidence(request_id=request_id, stage="model.resolve", decision="ALLOW", started=started)}
        except (ValueError, KeyError) as e:
            evidence = runtime_evidence(request_id=request_id, stage="model.resolve", decision="DENY", started=started, error=str(e))
            raise HTTPException(status_code=400, detail={"error": str(e), "evidence": evidence}) from e
