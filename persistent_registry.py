import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from threading import RLock

from mlops_platform import ModelVersion, Stage


class PersistentRegistry:
    """Transactional SQLite registry for single-node or shared-volume deployments."""

    def __init__(self, path: str = "models.db") -> None:
        self._path = str(Path(path))
        self._lock = RLock()
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS models (
                model TEXT NOT NULL,
                version TEXT NOT NULL,
                artifact_uri TEXT NOT NULL,
                metrics TEXT NOT NULL,
                stage TEXT NOT NULL,
                PRIMARY KEY(model, version)
            )""")

    def _connect(self):
        db = sqlite3.connect(self._path, timeout=10, isolation_level="IMMEDIATE")
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA busy_timeout=10000")
        return db

    def register(self, model: ModelVersion) -> ModelVersion:
        with self._lock, self._connect() as db:
            db.execute(
                "INSERT INTO models VALUES (?, ?, ?, ?, ?)",
                (
                    model.model,
                    model.version,
                    model.artifact_uri,
                    json.dumps(model.metrics),
                    model.stage.value,
                ),
            )
        return model

    def get(self, model: str, version: str) -> ModelVersion:
        with self._connect() as db:
            row = db.execute(
                "SELECT model, version, artifact_uri, metrics, stage FROM models WHERE model=? AND version=?",
                (model, version),
            ).fetchone()
        if row is None:
            raise KeyError((model, version))
        return ModelVersion(row[0], row[1], row[2], json.loads(row[3]), Stage(row[4]))

    def promote(self, model: str, version: str, target: Stage) -> ModelVersion:
        with self._lock, self._connect() as db:
            row = db.execute(
                "SELECT model, version, artifact_uri, metrics, stage FROM models WHERE model=? AND version=?",
                (model, version),
            ).fetchone()
            if row is None:
                raise KeyError((model, version))
            current = Stage(row[4])
            allowed = {
                Stage.REGISTERED: {Stage.VALIDATED},
                Stage.VALIDATED: {Stage.STAGING},
                Stage.STAGING: {Stage.PRODUCTION},
                Stage.PRODUCTION: {Stage.ARCHIVED},
                Stage.ARCHIVED: set(),
            }
            if target not in allowed[current]:
                raise ValueError(f"invalid transition {current}->{target}")
            metrics = json.loads(row[3])
            if target == Stage.PRODUCTION and metrics.get("quality", 0) < 0.8:
                raise ValueError("quality gate failed")
            db.execute(
                "UPDATE models SET stage=? WHERE model=? AND version=?",
                (target.value, model, version),
            )
            return ModelVersion(row[0], row[1], row[2], metrics, target)
