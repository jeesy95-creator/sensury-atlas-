import json
from pathlib import Path

from sensory_atlas.loaders import load_sensory_objects, read_jsonl
from sensory_atlas.parser import parse_sentence


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMOTED_OBJECT_IDS = {
    "green_leaf_crush",
    "wet_soil",
    "astringent_dryness",
    "amber_glow",
    "dark_resin",
    "lactonic_milk_softness",
    "tea_like_clarity",
    "golden_density",
}
DEFERRED_SHORTLIST_IDS = {
    "fig_leaf_green",
    "stone_fruit_glow",
    "iodine_coast",
    "syrupy_body",
}
LOCKED_FILES = [
    PROJECT_ROOT / "data" / "evaluation" / "test_sentences_20.jsonl",
    PROJECT_ROOT / "data" / "evaluation" / "blind_test_sentences_30.jsonl",
    PROJECT_ROOT / "data" / "evaluation" / "holdout_test_sentences_50.jsonl",
    PROJECT_ROOT / "src" / "sensory_atlas" / "parser.py",
    PROJECT_ROOT / "src" / "sensory_atlas" / "matcher.py",
    PROJECT_ROOT / "src" / "sensory_atlas" / "cue_hierarchy.py",
]


def _object_lookup() -> dict[str, dict]:
    return {obj.object_id: obj.model_dump(mode="json") for obj in load_sensory_objects()}


def _phrase_cues() -> dict:
    return json.loads((PROJECT_ROOT / "data" / "core" / "phrase_cues.json").read_text(encoding="utf-8"))


def _review_status() -> dict[str, dict]:
    return {
        row["candidate_object_id"]: row
        for row in read_jsonl(PROJECT_ROOT / "data" / "workflow" / "candidate_review_status.jsonl")
    }


def test_promoted_objects_exist_in_main_ontology() -> None:
    objects = _object_lookup()

    assert PROMOTED_OBJECT_IDS <= set(objects)


def test_promoted_objects_have_required_fields_and_examples() -> None:
    objects = _object_lookup()

    for object_id in PROMOTED_OBJECT_IDS:
        obj = objects[object_id]
        for field in (
            "object_id",
            "label",
            "korean_label",
            "object_type",
            "family",
            "definition",
            "core_axes",
            "example_expressions",
            "related_objects",
            "opposite_objects",
            "evidence_refs",
            "confidence",
            "status",
        ):
            assert obj[field] is not None
        assert len(obj["example_expressions"]) >= 8
        assert "ontology_expansion_v1.5" in obj["evidence_refs"]
        assert obj["confidence"] == "curated"
        assert obj["status"] == "active"


def test_promoted_objects_have_phrase_cues() -> None:
    cues = _phrase_cues()

    for object_id in PROMOTED_OBJECT_IDS:
        assert object_id in cues
        assert len(cues[object_id]["positive_cues"]) >= 8
        assert len(cues[object_id]["negative_cues"]) >= 3
        assert cues[object_id]["boost"] > 0


def test_promoted_objects_are_marked_merged_in_candidate_status() -> None:
    status = _review_status()

    for object_id in PROMOTED_OBJECT_IDS:
        row = status[object_id]
        assert row["review_status"] == "merged"
        assert row["priority"] == "high"
        assert row["promoted_to_object_id"] == object_id
        assert row["reviewed_at"] == "2026-07-01"


def test_deferred_shortlist_candidates_are_not_in_main_ontology() -> None:
    objects = _object_lookup()
    status = _review_status()

    assert not (DEFERRED_SHORTLIST_IDS & set(objects))
    for object_id in DEFERRED_SHORTLIST_IDS:
        assert status[object_id]["recommended_action"] == "defer_to_future_batch"
        assert status[object_id]["promoted_to_object_id"] is None


def test_v1_5_regression_cases_exist_and_cover_promoted_objects() -> None:
    path = PROJECT_ROOT / "data" / "regression" / "ontology_expansion_v1_5_cases.jsonl"
    rows = read_jsonl(path)
    counts = {object_id: 0 for object_id in PROMOTED_OBJECT_IDS}

    assert path.exists()
    assert len(rows) >= len(PROMOTED_OBJECT_IDS) * 3
    for row in rows:
        assert row["id"]
        assert row["input"]
        assert row["expected_top_objects"]
        for object_id in PROMOTED_OBJECT_IDS:
            if object_id in row["expected_top_objects"]:
                counts[object_id] += 1
    assert all(count >= 3 for count in counts.values())


def test_clear_promoted_object_examples_appear_in_top3() -> None:
    objects = load_sensory_objects()
    examples = {
        "green_leaf_crush": "손으로 으깬 초록 잎처럼 풋내가 선명하게 올라오는 향",
        "wet_soil": "비 온 뒤 흙냄새처럼 낮고 축축하게 올라오는 향",
        "astringent_dryness": "입 안을 조이는 건조함이 끝에 남는 느낌",
        "amber_glow": "앰버의 따뜻한 금빛 잔향처럼 오래 남아",
        "dark_resin": "어둡고 낮게 깔리는 수지처럼 끈적하게 남는 향",
        "lactonic_milk_softness": "우유처럼 하얗고 둥근 부드러움이 있어",
        "tea_like_clarity": "차처럼 맑고 건조한 투명감이 깨끗하게 지나가",
        "golden_density": "금빛으로 두껍게 남는 달콤한 밀도가 있어",
    }

    for object_id, text in examples.items():
        result = parse_sentence(text, objects)
        detected = {item.object_id for item in result.detected_objects[:3]}
        assert object_id in detected


def test_locked_evaluation_and_parser_files_exist() -> None:
    for path in LOCKED_FILES:
        assert path.exists()
