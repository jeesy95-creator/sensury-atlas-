"""Rule-based parser for Sensory Atlas MVP."""

from __future__ import annotations

from collections import Counter

from sensory_atlas.cue_hierarchy import CueGroupActivation, detect_cue_groups
from sensory_atlas.matcher import MatchResult, match_objects
from sensory_atlas.schema import ActivatedCueGroup, CoreAxes, DetectedObject, ParserOutput, SensoryObject


PARSER_VERSION = "rule_based_v0.7"
LOW_CONFIDENCE_THRESHOLD = 0.20
CUE_AXIS_UPDATE_THRESHOLD = 0.2
AXIS_FIELDS = (
    "material",
    "temperature",
    "texture",
    "light",
    "motion",
    "time",
    "atmosphere",
    "density",
    "rendering",
    "organic_mineral",
)
ANCHOR_FIRST_FIELDS = {"material", "density", "rendering", "organic_mineral"}
WEIGHTED_UNION_LIMITS = {"texture": 4, "light": 3, "motion": 3}
THRESHOLD_UNION_LIMITS = {"time": 3, "atmosphere": 3}
MERGE_SCORE_THRESHOLD = 0.45
MERGE_CANDIDATE_LIMIT = 3
DOMINANT_ANCHOR_SCORE = 0.85
DOMINANT_ANCHOR_GAP = 0.30
ANCHOR_PRIOR_WEIGHT = 0.75


def _as_list(value: str | list[str] | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if item]
    return [value]


def _weighted_values(matches: list[MatchResult], field: str) -> list[str]:
    weighted: Counter[str] = Counter()
    first_seen: dict[str, int] = {}
    for match_index, match in enumerate(matches):
        for value in _as_list(getattr(match.object.core_axes, field)):
            weighted[value] += match.score
            if match_index == 0:
                weighted[value] += match.score * ANCHOR_PRIOR_WEIGHT
            first_seen.setdefault(value, match_index)

    if not weighted:
        return []

    return sorted(weighted, key=lambda value: (-weighted[value], first_seen[value], value))


def select_merge_candidates(matches: list[MatchResult]) -> list[MatchResult]:
    if not matches:
        return []

    anchor = matches[0]
    top2_score = matches[1].score if len(matches) > 1 else 0.0
    if anchor.score >= DOMINANT_ANCHOR_SCORE and anchor.score - top2_score >= DOMINANT_ANCHOR_GAP:
        return [anchor]

    candidates = [match for match in matches if match.score >= MERGE_SCORE_THRESHOLD]
    if not candidates:
        return [anchor]
    return candidates[:MERGE_CANDIDATE_LIMIT]


def _anchor_axis(anchor: MatchResult, field: str) -> str | list[str] | None:
    return getattr(anchor.object.core_axes, field)


def _merge_axis(anchor: MatchResult, candidates: list[MatchResult], field: str) -> str | list[str] | None:
    anchor_value = _anchor_axis(anchor, field)
    if field in ANCHOR_FIRST_FIELDS:
        return anchor_value

    values = _weighted_values(candidates, field)
    if not values:
        return anchor_value

    if field == "temperature":
        return values[0]
    if field in WEIGHTED_UNION_LIMITS:
        return values[: WEIGHTED_UNION_LIMITS[field]]
    if field in THRESHOLD_UNION_LIMITS:
        return values[: THRESHOLD_UNION_LIMITS[field]]
    return anchor_value


def merge_axes(matches: list[MatchResult]) -> CoreAxes:
    if not matches:
        return CoreAxes()

    anchor = matches[0]
    candidates = select_merge_candidates(matches)
    payload = {field: _merge_axis(anchor, candidates, field) for field in AXIS_FIELDS}
    return CoreAxes.model_validate(payload)


def apply_axis_updates(axes: CoreAxes, activations: list[CueGroupActivation]) -> CoreAxes:
    payload = axes.model_dump()
    for activation in sorted(activations, key=lambda item: item.score):
        if activation.score < CUE_AXIS_UPDATE_THRESHOLD:
            continue
        for field, value in activation.axis_updates.items():
            if field in AXIS_FIELDS:
                payload[field] = value
    return CoreAxes.model_validate(payload)


def summarize(text: str, matches: list[MatchResult], axes: CoreAxes, low_confidence: bool) -> str:
    if not matches:
        return "이 표현은 기존 sensory object와 약하게만 연결됩니다. 해석 신뢰도가 낮아 사용자 확인이 필요합니다."

    anchor = matches[0]
    fragments: list[str] = []
    if axes.temperature:
        fragments.append(f"{axes.temperature} 온도감")
    if axes.texture:
        fragments.append(f"{', '.join(_as_list(axes.texture)[:2])} 질감")
    if axes.light:
        fragments.append(f"{', '.join(_as_list(axes.light)[:2])} 빛")
    if axes.atmosphere:
        fragments.append(f"{', '.join(_as_list(axes.atmosphere)[:2])} 분위기")

    core = ", ".join(fragments) if fragments else "복합적인 감각"
    summary = f"이 표현의 중심 감각은 {anchor.object.korean_label}입니다. {core}이 핵심으로 해석됩니다."

    supporting = [match.object.korean_label for match in matches[1:3] if match.score >= MERGE_SCORE_THRESHOLD]
    if supporting:
        summary += f" 보조적으로 {', '.join(supporting)}와 연결됩니다."
    if low_confidence:
        summary += " 해석 신뢰도가 낮아 사용자 확인이 필요합니다."
    return summary


def parse_sentence(
    text: str,
    sensory_objects: list[SensoryObject],
    *,
    limit: int = 5,
) -> ParserOutput:
    matches = match_objects(text, sensory_objects, limit=limit)
    activations = detect_cue_groups(text)
    axes = apply_axis_updates(merge_axes(matches), activations)
    confidence = round(sum(match.score for match in matches[:3]) / max(min(len(matches), 3), 1), 2)
    top1_score = matches[0].score if matches else 0.0
    low_confidence = top1_score < LOW_CONFIDENCE_THRESHOLD
    if not matches:
        confidence = 0.0

    return ParserOutput(
        input_text=text,
        detected_objects=[
            DetectedObject(object_id=match.object.object_id, score=round(match.score, 2))
            for match in matches
        ],
        anchor_object=(
            DetectedObject(object_id=matches[0].object.object_id, score=round(matches[0].score, 2))
            if matches
            else None
        ),
        activated_cue_groups=[
            ActivatedCueGroup(
                group_id=activation.group_id,
                score=round(activation.score, 2),
                matched_positive_cues=activation.matched_positive_cues,
                matched_negative_cues=activation.matched_negative_cues,
            )
            for activation in activations
        ],
        axes=axes,
        interpretation_summary=summarize(text, matches, axes, low_confidence),
        confidence=min(confidence, 1.0),
        low_confidence=low_confidence,
        parser_version=PARSER_VERSION,
    )
