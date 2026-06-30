"""Tests for ontology structural integrity: object_role, family taxonomy, phrase_cues coverage."""

from __future__ import annotations

import json

import pytest

from sensory_atlas.loaders import load_sensory_objects
from sensory_atlas.paths import (
    CORE_DATA_DIR,
    VOCABULARY_DATA_DIR,
    SENSORY_OBJECTS_PATH,
    PHRASE_CUES_PATH,
    CUE_HIERARCHY_PATH,
    AXIS_MAPPING_PATH,
)
from sensory_atlas.schema import OBJECT_ROLES


@pytest.fixture(scope="module")
def sensory_objects():
    return load_sensory_objects()


@pytest.fixture(scope="module")
def phrase_cues():
    return json.loads(PHRASE_CUES_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def axis_mapping():
    return json.loads(AXIS_MAPPING_PATH.read_text(encoding="utf-8"))


# --- core data files exist ---

def test_core_data_files_exist():
    for path in (SENSORY_OBJECTS_PATH, PHRASE_CUES_PATH, CUE_HIERARCHY_PATH):
        assert path.exists(), f"Missing core data file: {path}"


def test_axis_mapping_file_exists():
    assert AXIS_MAPPING_PATH.exists()


# --- object_role ---

def test_all_objects_have_object_role(sensory_objects):
    missing = [obj.object_id for obj in sensory_objects if not obj.object_role]
    assert not missing, f"Missing object_role: {missing}"


def test_all_object_roles_are_valid(sensory_objects):
    invalid = [
        (obj.object_id, obj.object_role)
        for obj in sensory_objects
        if obj.object_role not in OBJECT_ROLES
    ]
    assert not invalid, f"Invalid object_role values: {invalid}"


def test_rendering_anchors_are_visual_rendering_family(sensory_objects):
    rendering = [obj for obj in sensory_objects if obj.object_role == "rendering_anchor"]
    assert rendering, "Expected at least one rendering_anchor"
    for obj in rendering:
        assert obj.family == "Visual_Rendering", (
            f"{obj.object_id} is rendering_anchor but family={obj.family}"
        )


def test_taste_feel_anchors_are_food_texture_family(sensory_objects):
    food = [obj for obj in sensory_objects if obj.object_role == "taste_feel_anchor"]
    assert food, "Expected at least one taste_feel_anchor"
    for obj in food:
        assert obj.family == "Food_Texture", (
            f"{obj.object_id} is taste_feel_anchor but family={obj.family}"
        )


def test_atmosphere_anchors_assigned(sensory_objects):
    atmosphere = [obj.object_id for obj in sensory_objects if obj.object_role == "atmosphere_anchor"]
    assert "winter_dawn" in atmosphere
    assert "late_night_air" in atmosphere
    assert "old_library" in atmosphere
    assert "rain_on_asphalt" in atmosphere


def test_mineral_anchors_assigned(sensory_objects):
    mineral = [obj.object_id for obj in sensory_objects if obj.object_role == "mineral_anchor"]
    assert "marble" in mineral
    assert "cut_diamond" in mineral
    assert "cold_metal" in mineral


def test_organic_anchors_assigned(sensory_objects):
    organic = [obj.object_id for obj in sensory_objects if obj.object_role == "organic_anchor"]
    assert "wet_moss" in organic
    assert "cedarwood" in organic
    assert "green_leaf_crush" in organic


# --- v1.5 new objects have correct roles and families ---

def test_lactonic_milk_softness(sensory_objects):
    obj = next(o for o in sensory_objects if o.object_id == "lactonic_milk_softness")
    assert obj.family == "Food_Texture"
    assert obj.object_role == "texture_finish_anchor"


def test_tea_like_clarity(sensory_objects):
    obj = next(o for o in sensory_objects if o.object_id == "tea_like_clarity")
    assert obj.family == "Food_Texture"
    assert obj.object_role == "light_density_anchor"


def test_golden_density(sensory_objects):
    obj = next(o for o in sensory_objects if o.object_id == "golden_density")
    assert obj.family == "Food_Texture"
    assert obj.object_role == "light_density_anchor"


def test_amber_glow(sensory_objects):
    obj = next(o for o in sensory_objects if o.object_id == "amber_glow")
    assert obj.object_role == "light_density_anchor"


def test_astringent_dryness(sensory_objects):
    obj = next(o for o in sensory_objects if o.object_id == "astringent_dryness")
    assert obj.object_role == "texture_finish_anchor"


# --- phrase_cues coverage ---

def test_every_object_has_phrase_cues(sensory_objects, phrase_cues):
    missing = [obj.object_id for obj in sensory_objects if obj.object_id not in phrase_cues]
    assert not missing, f"Objects missing phrase_cues: {missing}"


def test_phrase_cues_have_positive_cues(phrase_cues):
    empty = [oid for oid, cfg in phrase_cues.items() if not cfg.get("positive_cues")]
    assert not empty, f"Empty positive_cues: {empty}"


def test_six_new_phrase_cue_entries(phrase_cues):
    expected = {"marble", "pine_resin", "winter_dawn", "after_rain_garden", "summer_noon", "old_wood"}
    missing = expected - set(phrase_cues)
    assert not missing, f"Missing phrase_cues entries: {missing}"


# --- axis mapping ---

def test_axis_mapping_has_all_extended_axes(axis_mapping):
    expected = {"clarity", "finish", "space", "shape", "edge", "moisture", "balance"}
    present = set(axis_mapping["extended_to_canonical"].keys())
    assert expected == present


def test_axis_mapping_canonical_targets_are_valid(axis_mapping):
    canonical = set(axis_mapping["canonical_axes"])
    for ext, config in axis_mapping["extended_to_canonical"].items():
        for target in config["maps_to"]:
            assert target in canonical, (
                f"Extended axis '{ext}' maps to '{target}' which is not a canonical axis"
            )


# --- family taxonomy ---

KNOWN_FAMILIES = {
    "Textile", "Leather", "Mineral", "Metal", "Organic", "Wood", "Resin",
    "Texture", "Time_Season", "Water_Air", "Space_Scene", "Food_Texture",
    "Smoke_Ash", "Visual_Rendering",
}


def test_all_families_are_known(sensory_objects):
    unknown = {obj.family for obj in sensory_objects} - KNOWN_FAMILIES
    assert not unknown, f"Unknown family values: {unknown}"


def test_family_names_are_capitalized(sensory_objects):
    bad = [obj.object_id for obj in sensory_objects if not obj.family[0].isupper()]
    assert not bad, f"Family names must start with uppercase: {bad}"


# --- parser compatibility copies ---

def test_parser_compat_copies_match_vocabulary_source():
    """Root-level copies must stay byte-identical to vocabulary source files.

    parser.py hardcodes data/sensory_axis_descriptors.json and
    data/sensory_modifier_groups.json. These are kept as compatibility copies
    until parser.py is migrated to paths.py. This test fails if the copies
    drift from the source of truth in data/vocabulary/.
    """
    from sensory_atlas.paths import PROJECT_ROOT, VOCABULARY_DATA_DIR
    compat_files = [
        "sensory_axis_descriptors.json",
        "sensory_modifier_groups.json",
    ]
    for filename in compat_files:
        compat = PROJECT_ROOT / "data" / filename
        source = VOCABULARY_DATA_DIR / filename
        assert compat.exists(), f"Compat copy missing: {compat}"
        assert source.exists(), f"Vocabulary source missing: {source}"
        assert compat.read_bytes() == source.read_bytes(), (
            f"Compat copy out of sync with source: {filename}\n"
            f"  compat:  {compat}\n"
            f"  source:  {source}\n"
            "Update the compat copy or the source to match."
        )
