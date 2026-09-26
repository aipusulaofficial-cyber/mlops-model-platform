import logging

from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from pydantic import BaseModel, Field

from model_domain import ModelVersion
from observability import PrincipalObservabilityMiddleware

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
def live():
    return {"status": "ok"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}


@app.post("/v1/models")
def handle(r: Request):
    with tracer.start_as_current_span("mlops-model-platform.domain"):
        try:
            m = ModelVersion(r.key, r.payload.version)
            return {"model": m.name, "version": m.version, "stage": m.stage}
        except (ValueError, KeyError) as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
