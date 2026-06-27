"""Evaluation helpers for parser smoke metrics."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from sensory_atlas.parser import parse_sentence
from sensory_atlas.schema import SensoryObject


class EvaluationRow(BaseModel):
    test_id: str
    input_text: str
    target_objects: list[str] = Field(default_factory=list)
    detected_objects: list[str] = Field(default_factory=list)
    top1_hit: bool
    top3_hit: bool


class EvaluationReport(BaseModel):
    total: int
    top1_hits: int
    top3_hits: int
    top1_hit_rate: float
    top3_hit_rate: float
    rows: list[EvaluationRow]


def evaluate_parser(test_records: list[dict], sensory_objects: list[SensoryObject]) -> EvaluationReport:
    rows: list[EvaluationRow] = []

    for index, record in enumerate(test_records, start=1):
        input_text = record["raw_text"]
        targets = list(record.get("target_objects", []))
        result = parse_sentence(input_text, sensory_objects)
        detected = [item.object_id for item in result.detected_objects]
        top1 = detected[:1]
        top3 = detected[:3]

        rows.append(
            EvaluationRow(
                test_id=record.get("test_id", f"test_{index:03d}"),
                input_text=input_text,
                target_objects=targets,
                detected_objects=detected,
                top1_hit=bool(set(top1) & set(targets)),
                top3_hit=bool(set(top3) & set(targets)),
            )
        )

    total = len(rows)
    top1_hits = sum(row.top1_hit for row in rows)
    top3_hits = sum(row.top3_hit for row in rows)
    return EvaluationReport(
        total=total,
        top1_hits=top1_hits,
        top3_hits=top3_hits,
        top1_hit_rate=round(top1_hits / total, 2) if total else 0.0,
        top3_hit_rate=round(top3_hits / total, 2) if total else 0.0,
        rows=rows,
    )


def write_eval_report(path: str | Path, report: EvaluationReport) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Sensory Atlas Evaluation Report",
        "",
        f"- Total test sentences: {report.total}",
        f"- Top-1 hit rate: {report.top1_hit_rate:.2f}",
        f"- Top-3 hit rate: {report.top3_hit_rate:.2f}",
        "",
        "| Test ID | Top-1 | Top-3 | Targets | Detected top 3 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in report.rows:
        targets = ", ".join(row.target_objects)
        detected = ", ".join(row.detected_objects[:3])
        lines.append(
            f"| {row.test_id} | {row.top1_hit} | {row.top3_hit} | {targets} | {detected} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
