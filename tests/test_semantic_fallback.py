from __future__ import annotations

import sys

from sensory_atlas import cli
from sensory_atlas.loaders import load_sensory_objects, load_test_sentences
from sensory_atlas.parser import parse_sentence
from sensory_atlas.paths import TEST_SENTENCES_HOLDOUT_PATH
from sensory_atlas.semantic_fallback import (
    build_semantic_documents,
    evaluate_semantic_fallback,
    load_semantic_documents,
    run_semantic_fallback,
    search_semantic_matches,
    should_use_semantic_fallback,
)


def test_semantic_documents_are_built_from_main_ontology() -> None:
    objects = load_sensory_objects()
    docs = build_semantic_documents(objects)

    assert docs
    assert len(docs) == len(objects)
    first = docs[0]
    assert first["object_id"]
    assert first["object_source"] == "main_ontology"
    assert first["document_text"]


def test_candidate_documents_are_lower_trust_when_included() -> None:
    objects = load_sensory_objects()
    candidate = {
        "candidate_object_id": "imaginary_candidate",
        "label": "Imaginary Candidate",
        "korean_label": "상상 후보",
        "definition": "아직 main ontology에 들어가지 않은 후보 감각 객체",
        "family": "Candidate",
        "example_expressions": ["상상 후보처럼 흐릿한 향"],
        "suggested_phrase_cues": ["상상 후보"],
    }

    docs = build_semantic_documents(objects, [candidate])
    candidate_docs = [doc for doc in docs if doc["object_id"] == "imaginary_candidate"]

    assert candidate_docs
    assert candidate_docs[0]["object_source"] == "candidate_object"
    assert "lower-trust" in candidate_docs[0]["document_text"]


def test_promoted_candidate_duplicate_is_not_added_twice() -> None:
    objects = load_sensory_objects()
    docs = load_semantic_documents(include_candidates=True)
    object_ids = [doc["object_id"] for doc in docs]

    assert object_ids.count("lactonic_milk_softness") == 1
    assert len(docs) >= len(objects)


def test_semantic_search_returns_top_k_with_normalized_similarity() -> None:
    docs = load_semantic_documents(include_candidates=True)
    matches = search_semantic_matches("비 온 뒤 젖은 흙 같은 향", docs, top_k=3)

    assert len(matches) == 3
    assert any(match["object_id"] in {"wet_soil", "after_rain_garden"} for match in matches)
    assert all(0 <= match["similarity"] <= 1 for match in matches)


def test_milk_softness_query_returns_lactonic_object() -> None:
    docs = load_semantic_documents(include_candidates=True)
    matches = search_semantic_matches("우유처럼 부드럽고 크리미한 향", docs, top_k=3)

    assert matches[0]["object_id"] == "lactonic_milk_softness"


def test_parser_output_includes_semantic_fallback_fields() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("캐시미어 니트처럼 따뜻하고 포근하게 감싸는 향", objects)
    payload = result.model_dump()

    for field in (
        "semantic_fallback_used",
        "semantic_fallback_reason",
        "semantic_fallback_backend",
        "semantic_matches",
    ):
        assert field in payload


def test_high_confidence_parse_does_not_need_fallback() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("4K 화면처럼 초점이 맞고 입자가 다 보이는 선명한 느낌", objects)

    assert result.anchor_object is not None
    assert result.anchor_object.object_id == "four_k_clarity"
    assert not result.semantic_fallback_used
    assert result.semantic_matches == []


def test_low_confidence_parse_uses_fallback_without_replacing_anchor() -> None:
    objects = load_sensory_objects()
    result = parse_sentence("새벽 기차역 플랫폼 끝에서 피우는 담배 한 모금 같은 향", objects)
    original_anchor = result.anchor_object.object_id if result.anchor_object else None

    assert result.semantic_fallback_used
    assert result.semantic_fallback_reason
    assert result.semantic_matches
    assert (result.anchor_object.object_id if result.anchor_object else None) == original_anchor


def test_forced_fallback_can_run_for_parser_output() -> None:
    objects = load_sensory_objects()
    result = parse_sentence(
        "캐시미어 니트처럼 따뜻하고 포근하게 감싸는 향",
        objects,
        use_semantic_fallback=False,
    )
    should_use, _ = should_use_semantic_fallback(result)
    fallback = run_semantic_fallback(result.input_text, result, force=True)

    assert not should_use
    assert fallback["fallback_used"]
    assert fallback["matches"]


def test_fallback_evaluation_runs_separately() -> None:
    objects = load_sensory_objects()
    sentences = load_test_sentences(TEST_SENTENCES_HOLDOUT_PATH)[:5]
    report = evaluate_semantic_fallback(sentences, objects, dataset_name="holdout_sample")

    assert report.dataset_name == "holdout_sample"
    assert report.total == 5
    assert 0 <= report.rule_top1_hit_rate <= 1
    assert 0 <= report.fallback_assist_top3_hit_rate <= 1


def test_cli_semantic_search_runs(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "sensory-atlas",
            "semantic-search",
            "우유처럼 부드럽고 크리미한 향",
            "--top-k",
            "2",
            "--include-candidates",
        ],
    )

    assert cli.main() == 0
    captured = capsys.readouterr()
    assert "lactonic_milk_softness" in captured.out
