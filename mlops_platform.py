"""MLOps control-plane core: versioned models and guarded promotion state machine."""
from dataclasses import dataclass
from enum import Enum
import sys

class Stage(str,Enum): REGISTERED="registered"; VALIDATED="validated"; STAGING="staging"; PRODUCTION="production"; ARCHIVED="archived"
@dataclass(frozen=True)
class ModelVersion:
    model:str; version:str; artifact_uri:str; metrics:dict[str,float]; stage:Stage=Stage.REGISTERED
class PromotionError(Exception): pass
class Registry:
    def __init__(self): self._items={}
    def register(self,m): 
        key=(m.model,m.version)
        if key in self._items: raise PromotionError("version already exists")
        self._items[key]=m
        return m
    def promote(self,model,version,target):
        m=self._items[(model,version)]
        allowed={Stage.REGISTERED:{Stage.VALIDATED},Stage.VALIDATED:{Stage.STAGING},Stage.STAGING:{Stage.PRODUCTION},Stage.PRODUCTION:{Stage.ARCHIVED},Stage.ARCHIVED:set()}
        if target not in allowed[m.stage]: raise PromotionError(f"invalid transition {m.stage}->{target}")
        if target==Stage.PRODUCTION and m.metrics.get("quality",0)<0.8: raise PromotionError("quality gate failed")
        n=ModelVersion(m.model,m.version,m.artifact_uri,m.metrics,target); self._items[(model,version)]=n; return n
def main():
    r=Registry(); r.register(ModelVersion("fraud","1","s3://models/fraud/1",{"quality":.91}))
    for s in [Stage.VALIDATED,Stage.STAGING,Stage.PRODUCTION]: print(r.promote("fraud","1",s))
if __name__=="__main__": main()
