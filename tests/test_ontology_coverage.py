import json
from pathlib import Path

from sensory_atlas.loaders import load_sensory_objects, read_jsonl


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRIORITY_OBJECTS = {
    "bark",
    "sea_breeze",
    "rain_on_asphalt",
    "rainy_street",
    "leather",
    "suede",
    "black_tea",
    "tobacco_leaf",
    "cedarwood",
    "green_stem",
    "dry_herb",
    "slate",
    "silver_spoon",
    "fresh_linen",
    "clean_room",
    "late_night_air",
    "barrel_cellar",
    "charred_oak",
    "forest_floor",
    "wet_stone",
}


def test_every_sensory_object_has_expanded_examples() -> None:
    objects = load_sensory_objects()

    sparse = [
        (obj.object_id, len(obj.example_expressions or []))
        for obj in objects
        if len(obj.example_expressions or []) < 8
    ]

    assert sparse == []


def test_priority_phrase_cue_objects_are_covered() -> None:
    phrase_cues = json.loads((PROJECT_ROOT / "data" / "core" / "phrase_cues.json").read_text(encoding="utf-8"))

    missing = sorted(PRIORITY_OBJECTS - set(phrase_cues))
    weak = {
        object_id: len(phrase_cues[object_id].get("positive_cues", []))
        for object_id in PRIORITY_OBJECTS & set(phrase_cues)
        if len(phrase_cues[object_id].get("positive_cues", [])) < 8
    }

    assert missing == []
    assert weak == {}


def test_dev_failure_cases_jsonl_is_valid() -> None:
    records = read_jsonl(PROJECT_ROOT / "data" / "regression" / "dev_failure_cases.jsonl")

    assert len(records) >= 20
    for record in records:
        assert record["id"]
        assert record["input"]
        assert record["expected_top_objects"]
        assert isinstance(record["expected_top_objects"], list)
        assert record["notes"]
