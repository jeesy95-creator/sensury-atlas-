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
    assert result.parser_version == "rule_based_v0.7"


def test_parser_output_contains_required_fields() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("캐시미어 니트처럼 따뜻하고 포근하게 감싸는 향", objects)
    payload = result.model_dump()

    for field in (
        "input_text",
        "detected_objects",
        "anchor_object",
        "activated_cue_groups",
        "axes",
        "axis_evidence",
        "axis_confidence",
        "clarification_questions",
        "interpretation_summary",
        "confidence",
        "low_confidence",
        "semantic_fallback_used",
        "semantic_fallback_reason",
        "semantic_fallback_backend",
        "semantic_matches",
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


def test_phrase_cue_cashmere() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("목도리를 오래 감고 있다가 맡는 체온 섞인 부드러운 냄새", objects)
    detected = {item.object_id for item in result.detected_objects[:3]}

    assert detected & {"cashmere", "warm_cotton", "wool_blanket"}
    assert result.anchor_object is not None
    assert result.anchor_object.object_id in {"cashmere", "warm_cotton", "wool_blanket"}


def test_food_context_not_textile() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("버터 바른 빵이 따뜻하게 감싸는 고소한 냄새", objects)
    detected = {item.object_id for item in result.detected_objects[:3]}

    assert detected & {"butter_toast", "vanilla_cream", "roasted_almond"}
    assert result.anchor_object is not None
    assert result.anchor_object.object_id != "cashmere"


def test_film_not_4k() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("오래된 영화 필름처럼 흐릿하지만 감정이 남는 향", objects)

    assert result.anchor_object is not None
    assert result.anchor_object.object_id == "film_grain"
    assert result.axes.rendering == "Film-like"
    assert result.anchor_object.object_id != "four_k_clarity"


def test_4k_not_film() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("4K 화면처럼 초점이 맞고 입자가 다 보이는 선명한 느낌", objects)

    assert result.anchor_object is not None
    assert result.anchor_object.object_id == "four_k_clarity"
    assert result.axes.rendering == "4K-like"


def test_film_low_resolution_not_4k() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("해상도는 낮지만 분위기만 남아", objects)
    detected = {item.object_id for item in result.detected_objects[:3]}
    groups = {item.group_id for item in result.activated_cue_groups}

    assert result.anchor_object is not None
    assert result.anchor_object.object_id != "four_k_clarity"
    assert "film_grain" in detected
    assert result.axes.rendering == "Film-like"
    assert "film_like_rendering" in groups


def test_four_k_high_resolution_not_film() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("고해상도 화면처럼 초점이 정확하고 윤곽이 또렷해", objects)
    groups = {item.group_id for item in result.activated_cue_groups}

    assert result.anchor_object is not None
    assert result.anchor_object.object_id == "four_k_clarity"
    assert result.axes.rendering == "4K-like"
    assert "four_k_clarity" in groups


def test_marble_hall_polish() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("차가운 큰 홀의 매끈한 바닥처럼 고요하고 윤이 나", objects)
    detected = {item.object_id for item in result.detected_objects[:3]}
    groups = {item.group_id for item in result.activated_cue_groups}

    assert "marble" in detected
    assert result.anchor_object is not None
    assert result.anchor_object.object_id == "marble"
    assert "marble_hall_polish" in groups


def test_mountain_water_flow() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("바위틈 사이로 차가운 물줄기가 흐르는 듯한 향", objects)
    detected = {item.object_id for item in result.detected_objects[:3]}
    groups = {item.group_id for item in result.activated_cue_groups}

    assert detected & {"mountain_stream", "wet_stone"}
    assert "mountain_water_flow" in groups


def test_cold_metal_tension() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("차가운 창틀에 손을 댔을 때처럼 조용한 긴장감이 있어", objects)
    detected = {item.object_id for item in result.detected_objects[:3]}
    groups = {item.group_id for item in result.activated_cue_groups}

    assert detected & {"cold_metal", "crystal"}
    assert "cold_metal_tension" in groups
