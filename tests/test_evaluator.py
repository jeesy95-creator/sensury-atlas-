from sensory_atlas.evaluator import evaluate_parser
from sensory_atlas.evaluator import write_eval_report
from sensory_atlas.loaders import load_sensory_objects, load_test_sentences, project_root
from sensory_atlas.cli import resolve_dataset_paths


def test_evaluator_runs() -> None:
    objects = load_sensory_objects()
    sentences = load_test_sentences()

    report = evaluate_parser(sentences, objects, dataset_name="default")

    assert report.dataset_name == "default"
    assert report.total == 20
    assert report.low_confidence_count >= 0
    assert 0 <= report.top1_hit_rate <= 1
    assert 0 <= report.top3_hit_rate <= 1
    assert report.rows


def test_blind_dataset_evaluator_runs() -> None:
    objects = load_sensory_objects()
    sentences = load_test_sentences("data/blind_test_sentences_30.jsonl")

    report = evaluate_parser(sentences, objects, dataset_name="blind")

    assert report.dataset_name == "blind"
    assert report.total == 30
    assert report.low_confidence_count >= 0
    assert 0 <= report.top1_hit_rate <= 1
    assert 0 <= report.top3_hit_rate <= 1


def test_resolve_blind_dataset_paths() -> None:
    tests_path, output_path = resolve_dataset_paths(
        root=project_root(),
        dataset="blind",
        tests_path=None,
        output_path=None,
    )

    assert tests_path.name == "blind_test_sentences_30.jsonl"
    assert output_path.name == "eval_report_blind.md"


def test_holdout_dataset_jsonl_is_valid() -> None:
    sentences = load_test_sentences("data/holdout_test_sentences_50.jsonl")

    assert len(sentences) == 50
    for row in sentences:
        for field in ("test_id", "raw_text", "language", "target_objects"):
            assert field in row
        assert row["test_id"].startswith("holdout_")
        assert row["target_objects"]


def test_holdout_dataset_evaluator_runs() -> None:
    objects = load_sensory_objects()
    sentences = load_test_sentences("data/holdout_test_sentences_50.jsonl")

    report = evaluate_parser(sentences, objects, dataset_name="holdout")

    assert report.dataset_name == "holdout"
    assert report.total == 50
    assert report.low_confidence_count >= 0
    assert 0 <= report.top1_hit_rate <= 1
    assert 0 <= report.top3_hit_rate <= 1


def test_resolve_holdout_dataset_paths() -> None:
    tests_path, output_path = resolve_dataset_paths(
        root=project_root(),
        dataset="holdout",
        tests_path=None,
        output_path=None,
    )

    assert tests_path.name == "holdout_test_sentences_50.jsonl"
    assert output_path.name == "eval_report_holdout.md"


def test_holdout_report_contains_failure_analysis(tmp_path) -> None:
    objects = load_sensory_objects()
    sentences = load_test_sentences("data/holdout_test_sentences_50.jsonl")
    report = evaluate_parser(sentences, objects, dataset_name="holdout")
    report_path = tmp_path / "eval_report_holdout.md"

    write_eval_report(report_path, report)

    content = report_path.read_text(encoding="utf-8")
    assert "## Failure Analysis" in content
    assert "### Common Failure Patterns" in content
