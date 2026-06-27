"""Deterministic sensory object matcher."""

from __future__ import annotations

import re
from dataclasses import dataclass

from sensory_atlas.schema import SensoryObject


TOKEN_RE = re.compile(r"[A-Za-z0-9가-힣]+")
STOPWORDS = {
    "같다",
    "처럼",
    "느낌",
    "냄새",
    "향",
    "살짝",
    "약간",
    "있는",
    "없는",
    "감각",
    "객체",
    "듯한",
    "그리고",
    "the",
    "and",
    "with",
}
FOUR_K_CLARITY_CUES = [
    "4k",
    "고해상도",
    "해상도",
    "선명도",
    "선명",
    "또렷",
    "윤곽",
    "초점",
    "디테일",
    "입자가 다 보",
    "입자가 보",
    "화면",
    "렌즈",
    "클리어",
    "깨끗하게 보",
]
VISUAL_PARTICLE_CONTEXT = [
    "보이고",
    "보인다",
    "다 보",
    "화면",
    "4k",
    "해상도",
    "선명",
    "디테일",
    "초점",
]
MINERAL_SPECIFIC_CUES = [
    "화강암",
    "돌",
    "바위",
    "석재",
    "암석",
    "회색",
    "거친 돌",
    "단단한 돌",
    "차가운 돌",
]


@dataclass(frozen=True)
class MatchResult:
    object: SensoryObject
    score: float


def normalize(text: str) -> str:
    return text.casefold().strip()


def tokenize(text: str) -> set[str]:
    tokens = {token.casefold() for token in TOKEN_RE.findall(text)}
    return {token for token in tokens if len(token) > 1 and token not in STOPWORDS}


def _candidate_terms(obj: SensoryObject) -> list[str]:
    terms = [obj.object_id.replace("_", " "), obj.label, obj.korean_label]
    terms.extend(obj.example_expressions)
    terms.extend(tokenize(obj.definition))
    return [term for term in terms if term]


def has_rendering_cue(normalized_text: str) -> bool:
    return any(cue.casefold() in normalized_text for cue in FOUR_K_CLARITY_CUES)


def has_visual_particle_context(normalized_text: str) -> bool:
    return "입자" in normalized_text and any(
        cue.casefold() in normalized_text for cue in VISUAL_PARTICLE_CONTEXT
    )


def has_mineral_specific_cue(normalized_text: str) -> bool:
    return any(cue.casefold() in normalized_text for cue in MINERAL_SPECIFIC_CUES)


def score_object(text: str, obj: SensoryObject) -> float:
    normalized = normalize(text)
    text_tokens = tokenize(text)
    rendering_cue = has_rendering_cue(normalized)
    visual_particle_context = has_visual_particle_context(normalized)
    score = 0.0

    for strong_term in (obj.korean_label, obj.label, obj.object_id.replace("_", " ")):
        term = normalize(strong_term)
        if term and term in normalized:
            score += 0.55

    for expression in obj.example_expressions:
        expression_norm = normalize(expression)
        expression_tokens = tokenize(expression)
        if expression_norm and expression_norm in normalized:
            score += 0.35
        elif expression_tokens:
            overlap = len(text_tokens & expression_tokens) / len(expression_tokens)
            score += min(overlap * 0.22, 0.22)

    definition_tokens = tokenize(obj.definition)
    if definition_tokens:
        overlap = len(text_tokens & definition_tokens) / max(len(text_tokens), 1)
        score += min(overlap * 0.35, 0.35)

    object_tokens = set()
    for term in _candidate_terms(obj):
        object_tokens.update(tokenize(term))
    if object_tokens:
        score += min((len(text_tokens & object_tokens) / len(object_tokens)) * 0.25, 0.25)

    if rendering_cue and obj.object_type == "visual_rendering_object":
        score += 0.25

    if obj.object_id == "four_k_clarity":
        if "4k" in normalized:
            score += 0.60
        if visual_particle_context:
            score += 0.25
        for cue in FOUR_K_CLARITY_CUES:
            if cue.casefold() in normalized:
                score += 0.08

    if obj.object_id == "granite":
        if visual_particle_context:
            score *= 0.75
        if not has_mineral_specific_cue(normalized):
            score *= 0.65

    return round(min(score, 1.0), 4)


def match_objects(
    text: str,
    sensory_objects: list[SensoryObject],
    *,
    limit: int = 5,
    min_score: float = 0.08,
) -> list[MatchResult]:
    object_by_id = {obj.object_id: obj for obj in sensory_objects}
    scores = {obj.object_id: score_object(text, obj) for obj in sensory_objects}

    # A sensory expression often names one object while implying adjacent ones.
    # Seed ontology relations let the fallback parser preserve that bridge.
    for obj in sensory_objects:
        source_score = scores[obj.object_id]
        if source_score < min_score:
            continue
        for related_id in obj.related_objects:
            if related_id in object_by_id:
                scores[related_id] = min(scores[related_id] + source_score * 0.35, 1.0)

    matches = [
        MatchResult(object=obj, score=round(scores[obj.object_id], 4))
        for obj in sensory_objects
    ]
    matches = [match for match in matches if match.score >= min_score]
    return sorted(matches, key=lambda item: item.score, reverse=True)[:limit]
