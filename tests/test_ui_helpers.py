from sensory_atlas.loaders import load_sensory_objects
from sensory_atlas.parser import parse_sentence
from sensory_atlas.ui_helpers import (
    axis_evidence_to_dataframe,
    candidate_detail_for_display,
    candidate_review_rows_to_dataframe,
    curated_shortlist_to_dataframe,
    evaluate_all_datasets,
    format_axis_confidence,
    format_axis_value,
    format_readiness_score,
    get_candidate_lookup,
    get_object_lookup,
    load_candidate_review_for_ui,
    objects_to_dataframe,
    parser_output_to_display_dict,
)


def test_objects_to_dataframe_has_required_columns() -> None:
    objects = load_sensory_objects()
    df = objects_to_dataframe(objects)

    assert not df.empty
    for column in ("object_id", "label", "korean_label", "family"):
        assert column in df.columns


def test_format_axis_value_handles_draft_values() -> None:
    assert format_axis_value("Cold") == "Cold"
    assert format_axis_value(["Clean", "Sharp"]) == "Clean, Sharp"
    assert format_axis_value(None) == ""


def test_format_axis_confidence_handles_empty_and_float_values() -> None:
    assert format_axis_confidence(None) == ""
    assert format_axis_confidence(0.756) == "0.76"


def test_format_readiness_score_handles_empty_and_float_values() -> None:
    assert format_readiness_score(None) == ""
    assert format_readiness_score(0.812) == "0.81"


def test_parser_output_to_display_dict_contains_anchor_and_axes() -> None:
    objects = load_sensory_objects()
    lookup = get_object_lookup(objects)
    output = parse_sentence("해상도는 낮지만 분위기만 남아", objects)

    display = parser_output_to_display_dict(output, lookup)

    assert display["anchor"]
    assert display["axes"]
    assert "axis_evidence_table" in display
    assert "clarification_questions" in display
    assert "Rendering" in display["axes"]


def test_axis_evidence_to_dataframe_contains_display_columns() -> None:
    objects = load_sensory_objects()
    output = parse_sentence("비 온 뒤 숲 바닥처럼 축축하고 초록빛이 도는 향", objects)
    df = axis_evidence_to_dataframe(output)

    assert not df.empty
    for column in ("axis", "inferred_value", "evidence", "axis_confidence"):
        assert column in df.columns


def test_candidate_review_helpers_return_display_data() -> None:
    review = load_candidate_review_for_ui()
    df = candidate_review_rows_to_dataframe(review["rows"])
    lookup = get_candidate_lookup(review["candidates"])
    first_id = review["rows"][0]["candidate_object_id"]
    detail = candidate_detail_for_display(lookup[first_id], review["existing_objects"])

    assert not df.empty
    assert "candidate_object_id" in df.columns
    assert first_id in lookup
    assert "promotion_draft" in detail
    assert "similar_existing_objects" in detail
    assert "shortlist" in review
    assert "shortlist_family_coverage" in review


def test_curated_shortlist_to_dataframe_contains_display_columns() -> None:
    review = load_candidate_review_for_ui()
    df = curated_shortlist_to_dataframe(review["shortlist"])

    assert not df.empty
    for column in ("candidate_object_id", "selection_reason", "promotion_risk"):
        assert column in df.columns


def test_evaluate_all_datasets_returns_reports() -> None:
    reports = evaluate_all_datasets()

    assert set(reports) == {"default", "blind", "holdout"}
    assert reports["default"].total == 20
    assert reports["blind"].total == 30
    assert reports["holdout"].total == 50
