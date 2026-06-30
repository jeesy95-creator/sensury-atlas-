"""Rule-based parser for Sensory Atlas MVP."""

from __future__ import annotations

import json
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any

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
QUESTION_CONFIDENCE_THRESHOLD = 0.35
WEAK_AXIS_CONFIDENCE_THRESHOLD = 0.45


def _normalize(text: str) -> str:
    return text.casefold().strip()


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


@lru_cache(maxsize=1)
def _load_axis_descriptor_terms() -> dict[str, list[str]]:
    path = _project_root() / "data" / "sensory_axis_descriptors.json"
    if not path.exists():
        return {}

    data = json.loads(path.read_text(encoding="utf-8"))
    terms_by_axis: dict[str, list[str]] = {}
    for axis, axis_payload in data.get("axes", {}).items():
        terms: list[str] = []
        for descriptor in axis_payload.get("descriptors", {}).values():
            for key in ("korean_terms", "example_patterns"):
                terms.extend(str(item) for item in descriptor.get(key, []) if item)
        terms_by_axis[axis] = _dedupe(terms)
    return terms_by_axis


@lru_cache(maxsize=1)
def _load_modifier_terms() -> dict[str, dict[str, Any]]:
    path = _project_root() / "data" / "sensory_modifier_groups.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8")).get("modifier_groups", {})


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        normalized = _normalize(str(value))
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(str(value))
    return deduped


def _term_variants(term: str) -> list[str]:
    normalized = _normalize(term)
    variants = [normalized]
    for suffix in ("한", "운", "은", "는", "의"):
        if normalized.endswith(suffix) and len(normalized) > len(suffix) + 1:
            variants.append(normalized[: -len(suffix)])
    if normalized.endswith("보이는"):
        variants.append(normalized[:-1])
    return _dedupe(variants)


def _term_in_text(term: str, normalized_text: str) -> bool:
    return any(variant and variant in normalized_text for variant in _term_variants(term))


def _add_evidence(axis_evidence: dict[str, list[str]], axis: str, evidence: str) -> None:
    if not axis or not evidence:
        return
    items = axis_evidence.setdefault(axis, [])
    normalized_items = {_normalize(item) for item in items}
    if _normalize(evidence) not in normalized_items:
        items.append(evidence)


def _activation_axis_updates(activation: Any) -> dict[str, Any]:
    if isinstance(activation, CueGroupActivation):
        return activation.axis_updates
    if isinstance(activation, ActivatedCueGroup):
        return {}
    if isinstance(activation, dict):
        return dict(activation.get("axis_updates", {}))
    return {}


def _activation_positive_cues(activation: Any) -> list[str]:
    if isinstance(activation, CueGroupActivation | ActivatedCueGroup):
        return list(activation.matched_positive_cues)
    if isinstance(activation, dict):
        return [str(item) for item in activation.get("matched_positive_cues", []) if item]
    return []


def _activation_group_id(activation: Any) -> str:
    if isinstance(activation, CueGroupActivation | ActivatedCueGroup):
        return activation.group_id
    if isinstance(activation, dict):
        return str(activation.get("group_id", ""))
    return ""


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


def build_axis_evidence(
    text: str,
    axes: CoreAxes | dict[str, Any],
    activated_cue_groups: list[Any],
) -> dict[str, list[str]]:
    normalized_text = _normalize(text)
    axis_evidence: dict[str, list[str]] = {}

    for axis, terms in _load_axis_descriptor_terms().items():
        for term in terms:
            if _term_in_text(term, normalized_text):
                _add_evidence(axis_evidence, axis, term)

    for group in _load_modifier_terms().values():
        matched_terms = [
            term
            for term in [*group.get("terms", []), *group.get("example_phrases", [])]
            if _term_in_text(str(term), normalized_text)
        ]
        for axis in group.get("axis_combination", []):
            for term in matched_terms:
                _add_evidence(axis_evidence, str(axis), str(term))

    for activation in activated_cue_groups:
        cues = _activation_positive_cues(activation)
        group_id = _activation_group_id(activation)
        for axis in _activation_axis_updates(activation):
            for cue in cues:
                _add_evidence(axis_evidence, axis, cue)
            if not cues and group_id:
                _add_evidence(axis_evidence, axis, group_id)

    axis_payload = axes.model_dump() if isinstance(axes, CoreAxes) else axes
    for axis, value in axis_payload.items():
        if value is None:
            continue
        for axis_value in _as_list(value):
            if _term_in_text(str(axis_value), normalized_text):
                _add_evidence(axis_evidence, axis, str(axis_value))

    return {axis: _dedupe(items) for axis, items in axis_evidence.items() if items}


def build_axis_confidence(
    axis_evidence: dict[str, list[str]],
    axes: CoreAxes | dict[str, Any],
    activated_cue_groups: list[Any],
) -> dict[str, float]:
    axis_payload = axes.model_dump() if isinstance(axes, CoreAxes) else axes
    axis_update_support = {
        axis
        for activation in activated_cue_groups
        for axis in _activation_axis_updates(activation)
    }
    axes_to_score = set(axis_evidence) | {
        axis for axis, value in axis_payload.items() if value is not None
    }

    confidence: dict[str, float] = {}
    for axis in sorted(axes_to_score):
        evidence_count = len(axis_evidence.get(axis, []))
        cue_group_support = 1 if axis in axis_update_support else 0
        axis_value_presence = 1 if axis_payload.get(axis) is not None else 0
        value = 0.35 + 0.15 * evidence_count + 0.10 * cue_group_support + 0.10 * axis_value_presence
        confidence[axis] = round(min(value, 1.0), 2)
    return confidence


def generate_clarification_questions(
    text: str,
    axes: CoreAxes,
    axis_confidence: dict[str, float],
    detected_objects: list[MatchResult],
    low_confidence: bool,
) -> list[str]:
    questions: list[str] = []
    close_candidates = detected_objects[:3]
    top_gap = (
        close_candidates[0].score - close_candidates[1].score
        if len(close_candidates) > 1
        else 1.0
    )
    ambiguous_objects = len(close_candidates) > 1 and top_gap < 0.08
    weak_axes = [
        axis
        for axis in ("temperature", "texture", "atmosphere", "rendering")
        if getattr(axes, axis, None) is not None
        and axis_confidence.get(axis, 0.0) < WEAK_AXIS_CONFIDENCE_THRESHOLD
    ]

    if not (low_confidence or ambiguous_objects or weak_axes):
        return []

    if ambiguous_objects:
        first = close_candidates[0].object.korean_label
        second = close_candidates[1].object.korean_label
        questions.append(f"이 표현은 더 '{first}' 쪽에 가까운가요, 아니면 '{second}' 쪽에 가까운가요?")

    if "temperature" in weak_axes or (low_confidence and axes.temperature is None):
        questions.append("이 표현은 더 차갑고 선명한 느낌인가요, 아니면 따뜻하고 포근한 느낌인가요?")
    if "texture" in weak_axes or (low_confidence and axes.texture is None):
        questions.append("질감은 더 보송한 쪽인가요, 축축한 쪽인가요, 매끈한 쪽인가요?")
    if "atmosphere" in weak_axes or (low_confidence and axes.atmosphere is None):
        questions.append("분위기는 더 자연적이고 숲에 가까운가요, 도시적이고 인공적인 쪽인가요?")

    if low_confidence and not questions:
        questions.append("이 표현에서 더 중요한 감각은 온도감인가요, 질감인가요, 분위기인가요?")

    return _dedupe(questions)[:3]


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
    use_semantic_fallback: bool = True,
) -> ParserOutput:
    matches = match_objects(text, sensory_objects, limit=limit)
    activations = detect_cue_groups(text)
    axes = apply_axis_updates(merge_axes(matches), activations)
    confidence = round(sum(match.score for match in matches[:3]) / max(min(len(matches), 3), 1), 2)
    top1_score = matches[0].score if matches else 0.0
    low_confidence = top1_score < LOW_CONFIDENCE_THRESHOLD
    if not matches:
        confidence = 0.0
    axis_evidence = build_axis_evidence(text, axes, activations)
    axis_confidence = build_axis_confidence(axis_evidence, axes, activations)
    clarification_questions = generate_clarification_questions(
        text,
        axes,
        axis_confidence,
        matches,
        low_confidence or confidence < QUESTION_CONFIDENCE_THRESHOLD,
    )

    output = ParserOutput(
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
        axis_evidence=axis_evidence,
        axis_confidence=axis_confidence,
        clarification_questions=clarification_questions,
        interpretation_summary=summarize(text, matches, axes, low_confidence),
        confidence=min(confidence, 1.0),
        low_confidence=low_confidence,
        parser_version=PARSER_VERSION,
    )
    if use_semantic_fallback:
        from sensory_atlas.semantic_fallback import run_semantic_fallback

        fallback = run_semantic_fallback(text, output)
        output.semantic_fallback_used = bool(fallback["fallback_used"])
        output.semantic_fallback_reason = fallback["fallback_reason"]
        output.semantic_fallback_backend = fallback["backend"]
        output.semantic_matches = fallback["matches"]
    return output
