from sensory_atlas.loaders import load_sensory_objects
from sensory_atlas.parser import parse_sentence


def test_parser_runs_on_sample_sentence() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("11월 말 새벽 공기처럼 차갑고 투명한 느낌", objects)

    assert result.input_text
    assert result.detected_objects
    assert result.anchor_object
    assert result.axes
    assert result.interpretation_summary
    assert result.confidence >= 0
    assert result.parser_version == "rule_based_v0.3"


def test_parser_output_contains_required_fields() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("캐시미어 니트처럼 따뜻하고 포근하게 감싸는 향", objects)
    payload = result.model_dump()

    for field in (
        "input_text",
        "detected_objects",
        "anchor_object",
        "axes",
        "interpretation_summary",
        "confidence",
        "parser_version",
    ):
        assert field in payload


def test_wet_moss_anchor_preserves_identity_axes() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("비 온 뒤 계곡 이끼처럼 차갑고 축축한 초록색 냄새", objects)

    assert result.anchor_object is not None
    assert result.anchor_object.object_id == "wet_moss"
    assert result.axes.material == "Organic"
    assert result.axes.rendering == "Atmosphere-first"
    assert result.axes.organic_mineral == "Vegetal"


def test_four_k_clarity_rendering_cue_beats_granite() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("4K 화면처럼 입자가 다 보이고 차갑게 선명해", objects)

    assert result.anchor_object is not None
    assert result.anchor_object.object_id == "four_k_clarity"
    assert result.detected_objects[0].object_id == "four_k_clarity"
    assert result.axes.rendering == "4K-like"
    assert result.detected_objects[0].object_id != "granite"
