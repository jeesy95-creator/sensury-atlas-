import csv
import json
from pathlib import Path

from sensory_atlas.loaders import read_jsonl


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_AXES = {
    "temperature",
    "texture",
    "density",
    "light",
    "clarity",
    "motion",
    "time",
    "finish",
    "space",
    "atmosphere",
    "shape",
    "edge",
    "moisture",
    "organic",
    "mineral",
    "rendering",
    "balance",
}
REQUIRED_COLUMNS = {
    "term",
    "korean_label",
    "english_gloss",
    "part_of_speech",
    "primary_axis",
    "secondary_axes",
    "descriptor_type",
    "polarity",
    "intensity",
    "synonym_group",
    "opposite_terms",
    "example_phrases",
    "mapped_existing_objects",
    "candidate_objects",
    "integration_status",
    "notes",
}
ALLOWED_INTEGRATION_STATUSES = {
    "axis_descriptor",
    "modifier_candidate",
    "pattern_candidate",
    "do_not_integrate_yet",
}
REQUIRED_MODIFIER_GROUPS = {
    "cold_clear",
    "cold_metallic",
    "warm_soft",
    "warm_sweet",
    "soft_powdery",
    "soft_textile",
    "wet_green",
    "wet_mineral",
    "dry_woody",
    "dry_smoky",
    "heavy_dark",
    "light_airy",
    "sharp_bright",
    "round_mellow",
    "transparent_clean",
    "cloudy_muted",
    "dense_resinous",
    "thin_linear",
    "spreading_air",
    "wrapping_body",
    "rising_topnote",
    "settling_baseline",
    "long_lingering",
    "short_clean_finish",
    "film_like_mood",
    "four_k_precision",
    "urban_wet",
    "forest_wet",
    "mineral_sparkle",
    "skin_like_softness",
}


def test_general_sensory_vocabulary_csv_shape() -> None:
    path = PROJECT_ROOT / "data" / "vocabulary" / "general_sensory_vocabulary.csv"

    assert path.exists()
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) >= 160
    assert set(rows[0]) == REQUIRED_COLUMNS
    assert REQUIRED_AXES <= {row["primary_axis"] for row in rows}
    assert {row["integration_status"] for row in rows} <= ALLOWED_INTEGRATION_STATUSES


def test_sensory_axis_descriptors_json_shape() -> None:
    path = PROJECT_ROOT / "data" / "vocabulary" / "sensory_axis_descriptors.json"

    assert path.exists()
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["version"] == "v1.2"
    assert REQUIRED_AXES <= set(payload["axes"])
    for axis in REQUIRED_AXES:
        assert len(payload["axes"][axis]["descriptors"]) >= 5


def test_sensory_modifier_groups_json_shape() -> None:
    path = PROJECT_ROOT / "data" / "vocabulary" / "sensory_modifier_groups.json"

    assert path.exists()
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["version"] == "v1.2"
    assert REQUIRED_MODIFIER_GROUPS <= set(payload["modifier_groups"])


def test_sensory_expression_patterns_jsonl_shape() -> None:
    path = PROJECT_ROOT / "data" / "vocabulary" / "sensory_expression_patterns.jsonl"
    records = read_jsonl(path)

    assert path.exists()
    assert len(records) >= 40
    for record in records:
        assert record["pattern_id"]
        assert record["pattern_name"]
        assert record["korean_pattern"]
        assert record["description"]
        assert record["example_inputs"]
        assert record["interpretation_rule"]
        assert record["related_axes"]
        assert record["candidate_parser_use"]
