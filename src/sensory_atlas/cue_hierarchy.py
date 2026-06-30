"""Cue hierarchy detection and scoring helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from sensory_atlas.paths import CUE_HIERARCHY_PATH


ACTIVATION_THRESHOLD = 0.2


@dataclass(frozen=True)
class CueGroupActivation:
    group_id: str
    score: float
    matched_positive_cues: list[str]
    matched_negative_cues: list[str]
    boost_objects: dict[str, float]
    penalize_objects: dict[str, float]
    axis_updates: dict[str, Any]


def normalize(text: str) -> str:
    return text.casefold().strip()


@lru_cache(maxsize=1)
def load_cue_hierarchy() -> dict[str, dict[str, Any]]:
    path = CUE_HIERARCHY_PATH
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _cue_score(cue: str) -> float:
    return 0.12 + min(len(cue) / 28, 0.18)


def _matched_cues(normalized_text: str, cues: list[str]) -> list[str]:
    return [cue for cue in cues if normalize(str(cue)) in normalized_text]


def detect_cue_groups(text: str) -> list[CueGroupActivation]:
    normalized_text = normalize(text)
    activations: list[CueGroupActivation] = []
    for group_id, config in load_cue_hierarchy().items():
        positives = _matched_cues(normalized_text, config.get("positive_cues", []))
        if not positives:
            continue
        negatives = _matched_cues(normalized_text, config.get("negative_cues", []))
        positive_score = sum(_cue_score(cue) for cue in positives)
        negative_score = sum(_cue_score(cue) for cue in negatives)
        activation_score = positive_score - negative_score
        if activation_score < ACTIVATION_THRESHOLD:
            continue
        activations.append(
            CueGroupActivation(
                group_id=group_id,
                score=round(activation_score, 4),
                matched_positive_cues=positives,
                matched_negative_cues=negatives,
                boost_objects={
                    str(object_id): float(boost)
                    for object_id, boost in config.get("boost_objects", {}).items()
                },
                penalize_objects={
                    str(object_id): float(penalty)
                    for object_id, penalty in config.get("penalize_objects", {}).items()
                },
                axis_updates=dict(config.get("axis_updates", {})),
            )
        )
    return sorted(activations, key=lambda item: item.score, reverse=True)


def apply_cue_hierarchy_scores(scores: dict[str, float], activations: list[CueGroupActivation]) -> None:
    for activation in activations:
        weight = min(activation.score, 1.0)
        for object_id, boost in activation.boost_objects.items():
            if object_id in scores:
                scores[object_id] = min(scores[object_id] + boost * weight, 1.0)
        for object_id, penalty in activation.penalize_objects.items():
            if object_id in scores:
                scores[object_id] = max(scores[object_id] - penalty * weight, 0.0)
