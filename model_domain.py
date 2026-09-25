from dataclasses import dataclass
from enum import StrEnum


class Stage(StrEnum):
    REGISTERED = "registered"
    VALIDATED = "validated"
    STAGING = "staging"
    PRODUCTION = "production"
    ARCHIVED = "archived"


@dataclass
class ModelVersion:
    name: str
    version: str
    stage: Stage = Stage.REGISTERED

    def promote(self, target: Stage) -> None:
        allowed = {
            Stage.REGISTERED: {Stage.VALIDATED},
            Stage.VALIDATED: {Stage.STAGING},
            Stage.STAGING: {Stage.PRODUCTION, Stage.ARCHIVED},
            Stage.PRODUCTION: {Stage.ARCHIVED},
            Stage.ARCHIVED: set(),
        }
        if target not in allowed[self.stage]:
            raise ValueError(f"invalid promotion {self.stage}->{target}")
        self.stage = target


class ModelCatalog:
    def __init__(self):
        self._models = {}

    def register(self, m: ModelVersion) -> None:
        key = (m.name, m.version)
        if key in self._models:
            raise ValueError("model version already exists")
        self._models[key] = m

    def get(self, name, version):
        return self._models[(name, version)]
