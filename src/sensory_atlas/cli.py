"""CLI for Sensory Atlas MVP."""

from __future__ import annotations

import argparse
from pathlib import Path

from sensory_atlas.loaders import (
    JsonlValidationError,
    load_sensory_objects,
    load_test_sentences,
    project_root,
    write_jsonl,
)
from sensory_atlas.paths import (
    PROJECT_ROOT,
    SENSORY_OBJECTS_PATH,
    EVALUATION_DATASET_PATHS,
    CURATED_SHORTLIST_PATH,
)
from sensory_atlas.evaluator import evaluate_parser, write_eval_report
from sensory_atlas.parser import parse_sentence
from sensory_atlas.semantic_fallback import (
    evaluate_semantic_fallback,
    load_semantic_documents,
    search_semantic_matches,
    write_fallback_report,
)
from sensory_atlas.candidate_workflow import (
    write_candidate_review_outputs,
    write_curated_shortlist_outputs,
)

OUTPUTS_DIR = PROJECT_ROOT / "outputs"


def resolve_dataset_paths(
    dataset: str,
    tests_path: Path | None,
    output_path: Path | None,
) -> tuple[Path, Path]:
    report_names = {
        "default": "eval_report.md",
        "blind": "eval_report_blind.md",
        "holdout": "eval_report_holdout.md",
    }
    if dataset not in EVALUATION_DATASET_PATHS:
        allowed = ", ".join(sorted(EVALUATION_DATASET_PATHS))
        raise ValueError(f"Unknown dataset '{dataset}'. Expected one of: {allowed}")
    return (
        tests_path or EVALUATION_DATASET_PATHS[dataset],
        output_path or OUTPUTS_DIR / report_names[dataset],
    )


def validate_data(args: argparse.Namespace) -> int:
    try:
        objects = load_sensory_objects(args.objects_path)
    except JsonlValidationError as exc:
        print(f"Schema validation failed: {exc}")
        return 1
    print(f"Validated {len(objects)} sensory objects")
    return 0


def dry_run(args: argparse.Namespace) -> int:
    objects_path = args.objects_path or SENSORY_OBJECTS_PATH
    tests_path = args.tests_path or EVALUATION_DATASET_PATHS["default"]
    output_path = args.output_path or OUTPUTS_DIR / "parser_results.jsonl"

    objects = load_sensory_objects(objects_path)
    sentences = load_test_sentences(tests_path)
    results = [parse_sentence(record["raw_text"], objects) for record in sentences]
    write_jsonl(output_path, results)

    parsed_count = sum(1 for result in results if result.detected_objects)
    print(f"Test sentences: {len(sentences)}")
    print(f"Successfully parsed: {parsed_count}")
    print(f"Output file: {Path(output_path).resolve()}")
    return 0


def evaluate(args: argparse.Namespace) -> int:
    objects_path = args.objects_path or SENSORY_OBJECTS_PATH
    try:
        tests_path, output_path = resolve_dataset_paths(
            args.dataset, args.tests_path, args.output_path
        )
    except ValueError as exc:
        print(exc)
        return 1

    objects = load_sensory_objects(objects_path)
    sentences = load_test_sentences(tests_path)
    report = evaluate_parser(sentences, objects, dataset_name=args.dataset)
    write_eval_report(output_path, report)

    print(f"Dataset: {report.dataset_name}")
    print(f"Total test sentences: {report.total}")
    print(f"Top-1 hit rate: {report.top1_hit_rate:.2f}")
    print(f"Top-3 hit rate: {report.top3_hit_rate:.2f}")
    print(f"Low confidence cases: {report.low_confidence_count}")
    print(f"Report saved to {Path(output_path).resolve()}")
    return 0


def semantic_search(args: argparse.Namespace) -> int:
    documents = load_semantic_documents(include_candidates=args.include_candidates)
    matches = search_semantic_matches(
        args.query,
        documents,
        top_k=args.top_k,
        backend=args.backend,
    )
    print(f"Query: {args.query}")
    print(f"Backend: {args.backend}")
    print(f"Documents searched: {len(documents)}")
    for match in matches:
        print(
            f"{match['rank']}. {match['object_id']} "
            f"({match['object_source']}, similarity={match['similarity']:.2f}) "
            f"- {match.get('korean_label', '')}"
        )
    return 0


def evaluate_fallback(args: argparse.Namespace) -> int:
    objects_path = args.objects_path or SENSORY_OBJECTS_PATH
    try:
        tests_path, _ = resolve_dataset_paths(args.dataset, args.tests_path, None)
    except ValueError as exc:
        print(exc)
        return 1

    report_path = args.report_path or OUTPUTS_DIR / f"semantic_fallback_report_{args.dataset}.md"
    summary_path = args.summary_path or OUTPUTS_DIR / f"semantic_fallback_summary_{args.dataset}.json"
    objects = load_sensory_objects(objects_path)
    sentences = load_test_sentences(tests_path)
    report = evaluate_semantic_fallback(
        sentences,
        objects,
        dataset_name=args.dataset,
        top_k=args.top_k,
        include_candidates=args.include_candidates,
    )
    write_fallback_report(report_path, summary_path, report)

    print(f"Dataset: {report.dataset_name}")
    print(f"Total test sentences: {report.total}")
    print(f"Rule Top-1 hit rate: {report.rule_top1_hit_rate:.2f}")
    print(f"Rule Top-3 hit rate: {report.rule_top3_hit_rate:.2f}")
    print(f"Fallback assist Top-1 hit rate: {report.fallback_assist_top1_hit_rate:.2f}")
    print(f"Fallback assist Top-3 hit rate: {report.fallback_assist_top3_hit_rate:.2f}")
    print(f"Fallback used count: {report.fallback_used_count}")
    print(f"Fallback helped count: {report.fallback_helped_count}")
    print(f"Fallback hurt count: {report.fallback_hurt_count}")
    print(f"Low confidence cases: {report.low_confidence_count}")
    print(f"Report saved to {Path(report_path).resolve()}")
    print(f"Summary saved to {Path(summary_path).resolve()}")
    return 0


def review_candidates(args: argparse.Namespace) -> int:
    report_path, summary_path, rows = write_candidate_review_outputs(
        args.report_path,
        args.summary_path,
    )
    ready_count = sum(1 for row in rows if row["recommended_action"] == "ready_for_curated_merge")
    distinction_count = sum(1 for row in rows if row["recommended_action"] == "needs_distinction_review")
    print(f"Total candidates: {len(rows)}")
    print(f"Ready for curated merge: {ready_count}")
    print(f"Needs distinction review: {distinction_count}")
    print(f"Report saved to {report_path.resolve()}")
    print(f"Summary saved to {summary_path.resolve()}")
    return 0


def select_curated_candidates(args: argparse.Namespace) -> int:
    output_path, report_path, summary_path, shortlist, summary = write_curated_shortlist_outputs(
        args.output,
        args.report,
        args.summary,
        min_count=args.min_count,
        max_count=args.max_count,
    )
    print(f"Total candidates: {summary['total_candidates']}")
    print(f"Ready-for-merge candidates reviewed: {summary['ready_for_curated_merge_reviewed']}")
    print(f"Selected candidates: {len(shortlist)}")
    print(f"Excluded ready candidates: {summary['excluded_ready_count']}")
    print(f"Shortlist saved to {output_path.resolve()}")
    print(f"Report saved to {report_path.resolve()}")
    print(f"Summary saved to {summary_path.resolve()}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sensory-atlas")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate-data", help="Validate sensory object JSONL data")
    validate.add_argument("--objects-path", type=Path, default=None)
    validate.set_defaults(func=validate_data)

    dry = subparsers.add_parser("dry-run", help="Parse bundled test sentences")
    dry.add_argument("--objects-path", type=Path, default=None)
    dry.add_argument("--tests-path", type=Path, default=None)
    dry.add_argument("--output-path", type=Path, default=None)
    dry.set_defaults(func=dry_run)

    eval_parser = subparsers.add_parser("evaluate", help="Evaluate parser against target objects")
    eval_parser.add_argument("--dataset", choices=sorted(EVALUATION_DATASET_PATHS), default="default")
    eval_parser.add_argument("--objects-path", type=Path, default=None)
    eval_parser.add_argument("--tests-path", type=Path, default=None)
    eval_parser.add_argument("--output-path", type=Path, default=None)
    eval_parser.set_defaults(func=evaluate)

    semantic = subparsers.add_parser("semantic-search", help="Search semantic fallback candidates")
    semantic.add_argument("query")
    semantic.add_argument("--top-k", type=int, default=5)
    semantic.add_argument("--include-candidates", action="store_true", default=False)
    semantic.add_argument("--backend", default="tfidf_char_ngram")
    semantic.set_defaults(func=semantic_search)

    fallback = subparsers.add_parser("evaluate-fallback", help="Evaluate semantic fallback separately")
    fallback.add_argument("--dataset", choices=sorted(EVALUATION_DATASET_PATHS), default="holdout")
    fallback.add_argument("--objects-path", type=Path, default=None)
    fallback.add_argument("--tests-path", type=Path, default=None)
    fallback.add_argument("--top-k", type=int, default=5)
    fallback.add_argument("--include-candidates", action=argparse.BooleanOptionalAction, default=True)
    fallback.add_argument("--report-path", type=Path, default=None)
    fallback.add_argument("--summary-path", type=Path, default=None)
    fallback.set_defaults(func=evaluate_fallback)

    review = subparsers.add_parser("review-candidates", help="Generate candidate object review report")
    review.add_argument("--report-path", type=Path, default=OUTPUTS_DIR / "candidate_review_report.md")
    review.add_argument("--summary-path", type=Path, default=OUTPUTS_DIR / "candidate_review_summary.json")
    review.set_defaults(func=review_candidates)

    shortlist = subparsers.add_parser("select-curated-candidates", help="Generate v1.5 curated candidate shortlist")
    shortlist.add_argument("--min-count", type=int, default=10)
    shortlist.add_argument("--max-count", type=int, default=12)
    shortlist.add_argument("--output", type=Path, default=CURATED_SHORTLIST_PATH)
    shortlist.add_argument("--report", type=Path, default=OUTPUTS_DIR / "curated_candidate_shortlist_report.md")
    shortlist.add_argument("--summary", type=Path, default=OUTPUTS_DIR / "curated_candidate_shortlist_summary.json")
    shortlist.set_defaults(func=select_curated_candidates)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
