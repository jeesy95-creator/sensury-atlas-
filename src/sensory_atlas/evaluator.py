"""Evaluation helpers for parser smoke metrics."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from sensory_atlas.parser import parse_sentence
from sensory_atlas.schema import SensoryObject


RENDERING_OBJECTS = {"film_grain", "four_k_clarity"}
VISUAL_CLARITY_OBJECTS = {"four_k_clarity", "cut_diamond", "crystal"}
MINERAL_OBJECTS = {"cut_diamond", "crystal", "granite", "slate", "marble", "wet_stone", "cold_metal", "silver_spoon"}
TEXTILE_OBJECTS = {"cashmere", "warm_cotton", "wool_blanket", "fresh_linen", "organza", "silk", "velvet"}
FOOD_OBJECTS = {"butter_toast", "vanilla_cream", "roasted_almond", "burnt_sugar", "honeycomb", "dark_chocolate"}
ATMOSPHERE_OBJECTS = {
    "winter_dawn",
    "mountain_stream",
    "sea_breeze",
    "cold_fog",
    "summer_noon",
    "late_night_air",
    "rainy_street",
    "old_library",
    "barrel_cellar",
    "clean_room",
}
TIME_SEASON_OBJECTS = {"winter_dawn", "summer_noon", "late_night_air", "cold_fog"}


class EvaluationRow(BaseModel):
    test_id: str
    input_text: str
    target_objects: list[str] = Field(default_factory=list)
    detected_objects: list[str] = Field(default_factory=list)
    detected_scores: list[float] = Field(default_factory=list)
    top1_hit: bool
    top3_hit: bool
    low_confidence: bool = False
    error_type: str = "none"
    error_notes: str = ""
    activated_cue_groups: list[str] = Field(default_factory=list)


class EvaluationReport(BaseModel):
    dataset_name: str = "default"
    total: int
    top1_hits: int
    top3_hits: int
    low_confidence_count: int
    top1_hit_rate: float
    top3_hit_rate: float
    cue_group_counts: dict[str, int] = Field(default_factory=dict)
    rows: list[EvaluationRow]


def _intersects(items: list[str], group: set[str]) -> bool:
    return bool(set(items) & group)


def classify_error(
    input_text: str,
    targets: list[str],
    detected: list[str],
    *,
    low_confidence: bool = False,
) -> tuple[str, str]:
    if low_confidence:
        return "low_confidence", "Top-1 score is below the low-confidence threshold."
    if not detected:
        return "phrase_cue_missing", "No object scored above the matcher threshold."

    top3 = detected[:3]
    normalized = input_text.casefold()
    target_rendering = _intersects(targets, RENDERING_OBJECTS)
    detected_rendering = _intersects(top3, RENDERING_OBJECTS)
    target_visual = _intersects(targets, VISUAL_CLARITY_OBJECTS)
    detected_mineral = _intersects(top3, MINERAL_OBJECTS)
    target_mineral = _intersects(targets, MINERAL_OBJECTS)
    detected_visual = _intersects(top3, VISUAL_CLARITY_OBJECTS)
    target_textile = _intersects(targets, TEXTILE_OBJECTS)
    detected_food = _intersects(top3, FOOD_OBJECTS)
    target_food = _intersects(targets, FOOD_OBJECTS)
    detected_textile = _intersects(top3, TEXTILE_OBJECTS)
    detected_atmosphere = _intersects(top3, ATMOSPHERE_OBJECTS)
    target_time = _intersects(targets, TIME_SEASON_OBJECTS)

    if target_rendering and not detected_rendering:
        return "rendering_vs_material_confusion", "Rendering target was not represented in detected top 3."
    if target_visual and detected_mineral and "입자" in normalized:
        return "mineral_vs_visual_confusion", "Visual clarity language may have been interpreted as material texture."
    if target_mineral and detected_visual and not detected_mineral:
        return "mineral_vs_visual_confusion", "Material/mineral target was pulled toward visual clarity objects."
    if target_textile and detected_food:
        return "food_vs_textile_confusion", "Soft comfort language may have been pulled toward food comfort."
    if target_food and detected_textile:
        return "food_vs_textile_confusion", "Warm/round comfort language may have been pulled toward textiles."
    if detected_atmosphere and not _intersects(targets, ATMOSPHERE_OBJECTS):
        return "atmosphere_overmatch", "Atmospheric object dominated a material/object target."
    if target_time and not _intersects(top3, TIME_SEASON_OBJECTS):
        return "time_season_underweighted", "Time or season cue did not survive into top 3."
    if len(normalized.split()) < 4 or not top3:
        return "phrase_cue_missing", "Input has too little lexical overlap with known cues."
    return "abstract_metaphor_too_broad", "Metaphor is broad enough to map to multiple sensory families."


def evaluate_parser(
    test_records: list[dict],
    sensory_objects: list[SensoryObject],
    *,
    dataset_name: str = "default",
) -> EvaluationReport:
    rows: list[EvaluationRow] = []

    for index, record in enumerate(test_records, start=1):
        input_text = record["raw_text"]
        targets = list(record.get("target_objects", []))
        result = parse_sentence(input_text, sensory_objects)
        detected = [item.object_id for item in result.detected_objects]
        detected_scores = [item.score for item in result.detected_objects]
        activated_cue_groups = [item.group_id for item in result.activated_cue_groups]
        top1 = detected[:1]
        top3 = detected[:3]
        top1_hit = bool(set(top1) & set(targets))
        top3_hit = bool(set(top3) & set(targets))
        error_type, error_notes = ("none", "")
        if not top3_hit or not top1_hit or result.low_confidence:
            error_type, error_notes = classify_error(
                input_text,
                targets,
                detected,
                low_confidence=result.low_confidence,
            )

        rows.append(
            EvaluationRow(
                test_id=record.get("test_id", f"test_{index:03d}"),
                input_text=input_text,
                target_objects=targets,
                detected_objects=detected,
                detected_scores=detected_scores,
                top1_hit=top1_hit,
                top3_hit=top3_hit,
                low_confidence=result.low_confidence,
                error_type=error_type,
                error_notes=error_notes,
                activated_cue_groups=activated_cue_groups,
            )
        )

    total = len(rows)
    top1_hits = sum(row.top1_hit for row in rows)
    top3_hits = sum(row.top3_hit for row in rows)
    low_confidence_count = sum(row.low_confidence for row in rows)
    cue_group_counts: dict[str, int] = {}
    for row in rows:
        for group_id in row.activated_cue_groups:
            cue_group_counts[group_id] = cue_group_counts.get(group_id, 0) + 1
    return EvaluationReport(
        dataset_name=dataset_name,
        total=total,
        top1_hits=top1_hits,
        top3_hits=top3_hits,
        low_confidence_count=low_confidence_count,
        top1_hit_rate=round(top1_hits / total, 2) if total else 0.0,
        top3_hit_rate=round(top3_hits / total, 2) if total else 0.0,
        cue_group_counts=cue_group_counts,
        rows=rows,
    )


def write_eval_report(path: str | Path, report: EvaluationReport) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Sensory Atlas Evaluation Report",
        "",
        f"- Dataset: {report.dataset_name}",
        f"- Total test sentences: {report.total}",
        f"- Top-1 hit rate: {report.top1_hit_rate:.2f}",
        f"- Top-3 hit rate: {report.top3_hit_rate:.2f}",
        f"- Low confidence cases: {report.low_confidence_count}",
        "",
        "| Test ID | Top-1 | Top-3 | Low confidence | Targets | Detected top 3 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in report.rows:
        targets = ", ".join(row.target_objects)
        detected = ", ".join(row.detected_objects[:3])
        lines.append(
            f"| {row.test_id} | {row.top1_hit} | {row.top3_hit} | {row.low_confidence} | {targets} | {detected} |"
        )

    if report.cue_group_counts:
        lines.extend(
            [
                "",
                "## Cue Group Analysis",
                "",
                "| Cue Group | Count |",
                "| --- | --- |",
            ]
        )
        for group_id, count in sorted(report.cue_group_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {group_id} | {count} |")

    misses = [row for row in report.rows if not row.top3_hit]
    top1_misses = [row for row in report.rows if not row.top1_hit]
    low_confidence_rows = [row for row in report.rows if row.low_confidence]

    if top1_misses or misses or low_confidence_rows:
        lines.extend(
            [
                "",
                "## Failure Analysis",
                "",
                "### Top-1 failures",
                "",
                "| Test ID | Input | Targets | Detected top 3 | Activated cue groups | Error Type | Notes |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in top1_misses:
            targets = ", ".join(row.target_objects)
            detected = ", ".join(row.detected_objects[:3])
            groups = ", ".join(row.activated_cue_groups)
            lines.append(
                f"| {row.test_id} | {row.input_text} | {targets} | {detected} | {groups} | {row.error_type} | {row.error_notes} |"
            )

    if misses:
        lines.extend(
            [
                "",
                "### Top-3 failures",
                "",
                "| Test ID | Input | Targets | Detected top 3 | Activated cue groups | Error Type | Notes |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in misses:
            targets = ", ".join(row.target_objects)
            detected = ", ".join(row.detected_objects[:3])
            groups = ", ".join(row.activated_cue_groups)
            lines.append(
                f"| {row.test_id} | {row.input_text} | {targets} | {detected} | {groups} | {row.error_type} | {row.error_notes} |"
            )

    if low_confidence_rows:
        lines.extend(
            [
                "",
                "### Low confidence cases",
                "",
                f"Low confidence case count: {len(low_confidence_rows)}",
                "",
                "| Test ID | Input | Top-1 | Score | Notes |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for row in low_confidence_rows:
            top1 = row.detected_objects[0] if row.detected_objects else ""
            score = f"{row.detected_scores[0]:.2f}" if row.detected_scores else "0.00"
            lines.append(f"| {row.test_id} | {row.input_text} | {top1} | {score} | {row.error_notes} |")

    if top1_misses or misses or low_confidence_rows:
        lines.extend(
            [
                "",
                "### Common Failure Patterns",
                "",
                "- phrase cue missing",
                "- abstract metaphor too broad",
                "- rendering cue confused with material cue",
                "- textile comfort confused with food comfort",
                "- mineral cue confused with visual clarity",
                "- atmosphere cue over-matched",
                "- time/season cue too weak",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
