from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
from otel_setup import tracer
app=FastAPI(title="mlops-model-platform",version="1.0.0")
class ModelRequest(BaseModel): model:str; payload:dict[str,Any]={}
@app.get("/health/live")
def live(): return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready"}
@app.post("/v1/models")
def models(r:ModelRequest):
 with tracer.start_as_current_span("model-operation") as s:s.set_attribute("model",r.model)
 return {"status":"accepted","model":r.model}
