import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from model_domain import ModelCatalog, ModelVersion, Stage
catalog=ModelCatalog(); m=ModelVersion("evidence-model","1.0"); catalog.register(m)
transitions=[]
for target in (Stage.VALIDATED,Stage.STAGING,Stage.PRODUCTION): m.promote(target); transitions.append(m.stage.value)
blocked=False
try: m.promote(Stage.VALIDATED)
except ValueError: blocked=True
report={"registered":catalog.get("evidence-model","1.0") is m,"promotion_path":transitions,"final_stage":m.stage.value,"invalid_transition_blocked":blocked}
if transitions!=["validated","staging","production"] or not blocked: raise SystemExit(report)
print(json.dumps(report, sort_keys=True))
