import json
from argparse import Namespace
from pathlib import Path

from sensory_atlas.candidate_workflow import (
    generate_curated_shortlist_report,
    load_candidate_objects,
    load_candidate_review_status,
    load_curated_shortlist,
    load_existing_objects,
    select_curated_shortlist,
    write_curated_shortlist_outputs,
)
from sensory_atlas.cli import select_curated_candidates


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOCKED_FILES = [
    PROJECT_ROOT / "data" / "core" / "sensory_objects.jsonl",
    PROJECT_ROOT / "data" / "evaluation" / "test_sentences_20.jsonl",
    PROJECT_ROOT / "data" / "evaluation" / "blind_test_sentences_30.jsonl",
    PROJECT_ROOT / "data" / "evaluation" / "holdout_test_sentences_50.jsonl",
    PROJECT_ROOT / "src" / "sensory_atlas" / "parser.py",
    PROJECT_ROOT / "src" / "sensory_atlas" / "matcher.py",
    PROJECT_ROOT / "src" / "sensory_atlas" / "cue_hierarchy.py",
]


def _shortlist() -> list[dict]:
    return select_curated_shortlist(
        load_candidate_objects(),
        load_existing_objects(),
        load_candidate_review_status(),
    )


def test_select_curated_shortlist_returns_10_to_12_candidates() -> None:
    shortlist = _shortlist()

    assert 10 <= len(shortlist) <= 12


def test_selected_candidates_are_ready_for_curated_merge() -> None:
    status = load_candidate_review_status()
    shortlist = _shortlist()

    for item in shortlist:
        assert status[item["candidate_object_id"]]["recommended_action"] == "ready_for_curated_merge"


def test_selected_candidates_do_not_have_high_note_dictionary_risk() -> None:
    shortlist = _shortlist()

    for item in shortlist:
        assert item["readiness_scores"]["note_dictionary_risk"] < 0.50


def test_selected_candidates_have_required_fields() -> None:
    shortlist = _shortlist()
    required = {
        "candidate_object_id",
        "korean_label",
        "source_domains",
        "family",
        "selection_status",
        "selection_reason",
        "readiness_scores",
        "related_existing_objects",
        "similar_existing_objects",
        "promotion_risk",
        "review_notes",
        "next_action",
    }

    for item in shortlist:
        assert required <= set(item)
        assert item["selection_status"] == "selected_for_v1_5_review"
        assert item["next_action"] == "manual_review_before_v1_5_merge"


def test_shortlist_file_exists_and_has_valid_jsonl_lines() -> None:
    path = PROJECT_ROOT / "data" / "workflow" / "curated_candidate_shortlist_v1_5.jsonl"
    rows = load_curated_shortlist(path)

    assert path.exists()
    assert 10 <= len(rows) <= 12
    for line in path.read_text(encoding="utf-8").splitlines():
        assert json.loads(line)["candidate_object_id"]


def test_curated_shortlist_report_contains_required_sections() -> None:
    report = generate_curated_shortlist_report(
        load_candidate_objects(),
        load_existing_objects(),
        load_candidate_review_status(),
        _shortlist(),
    )

    assert "## Summary" in report
    assert "## Selected Candidates" in report
    assert "## Excluded Ready Candidates" in report
    assert "## Next Step: v1.5 Curated Ontology Expansion" in report


def test_summary_json_includes_selected_count_and_ids() -> None:
    summary_path = PROJECT_ROOT / "outputs" / "curated_candidate_shortlist_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    assert summary["selected_count"] == len(summary["selected_candidate_ids"])
    assert 10 <= summary["selected_count"] <= 12
    assert summary["selection_notes"]


def test_select_curated_candidates_cli_handler_writes_outputs(tmp_path: Path) -> None:
    result = select_curated_candidates(
        Namespace(
            min_count=10,
            max_count=12,
            output=tmp_path / "shortlist.jsonl",
            report=tmp_path / "report.md",
            summary=tmp_path / "summary.json",
        )
    )

    assert result == 0
    assert (tmp_path / "shortlist.jsonl").exists()
    assert (tmp_path / "report.md").exists()
    assert (tmp_path / "summary.json").exists()


def test_write_curated_shortlist_outputs_does_not_modify_locked_files(tmp_path: Path) -> None:
    before = {path: path.read_text(encoding="utf-8") for path in LOCKED_FILES}
    write_curated_shortlist_outputs(
        tmp_path / "shortlist.jsonl",
        tmp_path / "report.md",
        tmp_path / "summary.json",
    )
    after = {path: path.read_text(encoding="utf-8") for path in LOCKED_FILES}

    assert before == after
