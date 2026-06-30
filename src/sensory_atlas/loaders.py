"""JSONL loaders and validation helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from sensory_atlas.paths import PROJECT_ROOT, SENSORY_OBJECTS_PATH, TEST_SENTENCES_DEFAULT_PATH
from sensory_atlas.schema import SensoryObject


T = TypeVar("T", bound=BaseModel)


class JsonlValidationError(ValueError):
    """Raised when a JSONL row cannot be decoded or validated."""


def project_root() -> Path:
    return PROJECT_ROOT


def read_jsonl(path: str | Path) -> list[dict]:
    path = Path(path)
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise JsonlValidationError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
    return records


def load_model_jsonl(path: str | Path, model: type[T]) -> list[T]:
    items: list[T] = []
    for line_number, record in enumerate(read_jsonl(path), start=1):
        try:
            items.append(model.model_validate(record))
        except ValidationError as exc:
            raise JsonlValidationError(f"{Path(path)}:{line_number}: schema error: {exc}") from exc
    return items


def load_sensory_objects(path: str | Path | None = None) -> list[SensoryObject]:
    path = Path(path) if path else SENSORY_OBJECTS_PATH
    return load_model_jsonl(path, SensoryObject)


def load_test_sentences(path: str | Path | None = None) -> list[dict]:
    path = Path(path) if path else TEST_SENTENCES_DEFAULT_PATH
    records = read_jsonl(path)
    missing = [idx for idx, record in enumerate(records, start=1) if "raw_text" not in record]
    if missing:
        raise JsonlValidationError(f"{path}: missing raw_text in rows {missing}")
    return records


def write_jsonl(path: str | Path, records: list[BaseModel | dict]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            if isinstance(record, BaseModel):
                payload = record.model_dump(mode="json", exclude_none=True)
            else:
                payload = record
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
