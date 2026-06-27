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
from sensory_atlas.evaluator import evaluate_parser, write_eval_report
from sensory_atlas.parser import parse_sentence


def validate_data(args: argparse.Namespace) -> int:
    try:
        objects = load_sensory_objects(args.objects_path)
    except JsonlValidationError as exc:
        print(f"Schema validation failed: {exc}")
        return 1

    print(f"Validated {len(objects)} sensory objects")
    return 0


def dry_run(args: argparse.Namespace) -> int:
    root = project_root()
    objects_path = args.objects_path or root / "data" / "sensory_objects.jsonl"
    tests_path = args.tests_path or root / "data" / "test_sentences_20.jsonl"
    output_path = args.output_path or root / "outputs" / "parser_results.jsonl"

    objects = load_sensory_objects(objects_path)
    sentences = load_test_sentences(tests_path)
    results = [
        parse_sentence(record["raw_text"], objects)
        for record in sentences
    ]
    write_jsonl(output_path, results)

    parsed_count = sum(1 for result in results if result.detected_objects)
    print(f"Test sentences: {len(sentences)}")
    print(f"Successfully parsed: {parsed_count}")
    print(f"Output file: {Path(output_path).resolve()}")
    return 0


def evaluate(args: argparse.Namespace) -> int:
    root = project_root()
    objects_path = args.objects_path or root / "data" / "sensory_objects.jsonl"
    tests_path = args.tests_path or root / "data" / "test_sentences_20.jsonl"
    output_path = args.output_path or root / "outputs" / "eval_report.md"

    objects = load_sensory_objects(objects_path)
    sentences = load_test_sentences(tests_path)
    report = evaluate_parser(sentences, objects)
    write_eval_report(output_path, report)

    print(f"Total test sentences: {report.total}")
    print(f"Top-1 hit rate: {report.top1_hit_rate:.2f}")
    print(f"Top-3 hit rate: {report.top3_hit_rate:.2f}")
    print(f"Report saved to {Path(output_path).resolve()}")
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
    eval_parser.add_argument("--objects-path", type=Path, default=None)
    eval_parser.add_argument("--tests-path", type=Path, default=None)
    eval_parser.add_argument("--output-path", type=Path, default=None)
    eval_parser.set_defaults(func=evaluate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
