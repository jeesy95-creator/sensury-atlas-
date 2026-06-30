from pathlib import Path
from argparse import Namespace

from sensory_atlas.cli import review_candidates
from sensory_atlas.candidate_workflow import (
    ALLOWED_REVIEW_STATUSES,
    RECOMMENDED_ACTIONS,
    compare_candidate_to_existing,
    compute_candidate_readiness,
    generate_candidate_review_report,
    generate_promotion_draft,
    load_candidate_objects,
    load_candidate_review_status,
    load_existing_objects,
    write_candidate_review_outputs,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVALUATION_DATASETS = [
    PROJECT_ROOT / "data" / "evaluation" / "test_sentences_20.jsonl",
    PROJECT_ROOT / "data" / "evaluation" / "blind_test_sentences_30.jsonl",
    PROJECT_ROOT / "data" / "evaluation" / "holdout_test_sentences_50.jsonl",
]


def test_candidate_objects_load_successfully() -> None:
    candidates = load_candidate_objects()

    assert len(candidates) >= 40
    assert candidates[0]["candidate_object_id"]


def test_existing_objects_load_successfully() -> None:
    existing = load_existing_objects()

    assert len(existing) >= 50
    assert existing[0]["object_id"]


def test_candidate_review_status_exists_and_covers_candidates() -> None:
    path = PROJECT_ROOT / "data" / "workflow" / "candidate_review_status.jsonl"
    candidates = load_candidate_objects()
    status = load_candidate_review_status(path)

    assert path.exists()
    assert set(status) == {candidate["candidate_object_id"] for candidate in candidates}


def test_candidate_review_status_values_are_valid() -> None:
    status = load_candidate_review_status()

    assert status
    for row in status.values():
        assert row["review_status"] in ALLOWED_REVIEW_STATUSES
        assert row["recommended_action"] in RECOMMENDED_ACTIONS
        assert row["priority"] in {"high", "medium", "low"}


def test_compute_candidate_readiness_returns_required_fields() -> None:
    candidate = load_candidate_objects()[0]
    existing = load_existing_objects()
    readiness = compute_candidate_readiness(candidate, existing)

    required = {
        "sensory_archetype_score",
        "cross_domain_reuse_score",
        "distinctiveness_score",
        "example_coverage_score",
        "phrase_cue_readiness_score",
        "negative_cue_readiness_score",
        "note_dictionary_risk",
        "overall_readiness_score",
        "recommended_action",
    }
    assert required <= set(readiness)
    assert readiness["recommended_action"] in RECOMMENDED_ACTIONS


def test_readiness_scores_are_bounded() -> None:
    candidate = load_candidate_objects()[0]
    existing = load_existing_objects()
    readiness = compute_candidate_readiness(candidate, existing)

    for key, value in readiness.items():
        if key.endswith("_score") or key == "note_dictionary_risk":
            assert 0.0 <= value <= 1.0


def test_compare_candidate_to_existing_returns_list() -> None:
    candidate = load_candidate_objects()[0]
    existing = load_existing_objects()
    comparisons = compare_candidate_to_existing(candidate, existing)

    assert isinstance(comparisons, list)
    if comparisons:
        assert "existing_object_id" in comparisons[0]
        assert "similarity_reason" in comparisons[0]
        assert "overlap_score" in comparisons[0]


def test_generate_promotion_draft_does_not_modify_main_ontology() -> None:
    ontology_path = PROJECT_ROOT / "data" / "core" / "sensory_objects.jsonl"
    before = ontology_path.read_text(encoding="utf-8")
    candidate = load_candidate_objects()[0]
    draft = generate_promotion_draft(candidate)
    after = ontology_path.read_text(encoding="utf-8")

    assert draft["object_type"] == "sensory_object_draft"
    assert draft["status"] == "draft_from_candidate"
    assert before == after


def test_generate_candidate_review_report_contains_summary_sections() -> None:
    candidates = load_candidate_objects()
    existing = load_existing_objects()
    status = load_candidate_review_status()
    report = generate_candidate_review_report(candidates, existing, status)

    assert "# Candidate Sensory Object Review Report" in report
    assert "## Summary" in report
    assert "## Ready for Curated Merge" in report
    assert "## Needs Distinction Review" in report
    assert "## Do Not Merge Yet" in report


def test_write_candidate_review_outputs(tmp_path: Path) -> None:
    report_path, summary_path, rows = write_candidate_review_outputs(
        tmp_path / "candidate_review_report.md",
        tmp_path / "candidate_review_summary.json",
    )

    assert report_path.exists()
    assert summary_path.exists()
    assert rows


def test_review_candidates_cli_handler_writes_outputs(tmp_path: Path) -> None:
    result = review_candidates(
        Namespace(
            report_path=tmp_path / "candidate_review_report.md",
            summary_path=tmp_path / "candidate_review_summary.json",
        )
    )

    assert result == 0
    assert (tmp_path / "candidate_review_report.md").exists()
    assert (tmp_path / "candidate_review_summary.json").exists()


def test_evaluation_datasets_still_exist() -> None:
    for path in EVALUATION_DATASETS:
        assert path.exists()
