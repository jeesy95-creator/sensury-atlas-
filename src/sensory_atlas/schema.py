"""Pydantic schemas for Sensory Atlas."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


AxisValue = str | list[str] | None


class CoreAxes(BaseModel):
    """Draft sensory axes.

    Seed data is intentionally permissive while the ontology is evolving:
    every axis may be a string, a list of strings, or null.
    """

    model_config = ConfigDict(extra="allow")

    material: AxisValue = None
    temperature: AxisValue = None
    texture: AxisValue = None
    light: AxisValue = None
    motion: AxisValue = None
    time: AxisValue = None
    atmosphere: AxisValue = None
    density: AxisValue = None
    rendering: AxisValue = None
    organic_mineral: AxisValue = None

    @field_validator("*", mode="before")
    @classmethod
    def coerce_axis_value(cls, value: Any) -> AxisValue:
        if value is None or isinstance(value, str):
            return value
        if isinstance(value, list):
            return [str(item) for item in value if item is not None]
        return str(value)


OBJECT_ROLES = frozenset({
    "material_anchor",
    "scene_anchor",
    "organic_anchor",
    "mineral_anchor",
    "atmosphere_anchor",
    "texture_finish_anchor",
    "light_density_anchor",
    "rendering_anchor",
    "taste_feel_anchor",
})


class SensoryObject(BaseModel):
    """A semantic sensory object in the ontology."""

    model_config = ConfigDict(extra="allow")

    object_id: str
    label: str
    korean_label: str
    object_type: str
    family: str
    object_role: str | None = None
    definition: str
    core_axes: CoreAxes
    example_expressions: list[str] = Field(default_factory=list)
    related_objects: list[str] = Field(default_factory=list)
    opposite_objects: list[str] = Field(default_factory=list)
    associated_products: list[Any] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    confidence: str | float | int | None = None


class DetectedObject(BaseModel):
    object_id: str
    score: float = Field(ge=0.0, le=1.0)


class ActivatedCueGroup(BaseModel):
    group_id: str
    score: float
    matched_positive_cues: list[str] = Field(default_factory=list)
    matched_negative_cues: list[str] = Field(default_factory=list)


class ParserOutput(BaseModel):
    input_text: str
    detected_objects: list[DetectedObject]
    anchor_object: DetectedObject | None = None
    activated_cue_groups: list[ActivatedCueGroup] = Field(default_factory=list)
    axes: CoreAxes
    axis_evidence: dict[str, list[str]] = Field(default_factory=dict)
    axis_confidence: dict[str, float] = Field(default_factory=dict)
    clarification_questions: list[str] = Field(default_factory=list)
    interpretation_summary: str
    confidence: float = Field(ge=0.0, le=1.0)
    low_confidence: bool = False
    semantic_fallback_used: bool = False
    semantic_fallback_reason: str | None = None
    semantic_fallback_backend: str | None = None
    semantic_matches: list[dict[str, Any]] = Field(default_factory=list)
    parser_version: str
