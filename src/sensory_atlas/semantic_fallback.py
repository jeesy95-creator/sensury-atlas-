"""Semantic fallback search for low-confidence sensory parses."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sensory_atlas.loaders import read_jsonl
from sensory_atlas.paths import (
    CANDIDATE_OBJECTS_PATH,
    PHRASE_CUES_PATH,
    SENSORY_OBJECTS_PATH,
)
from sensory_atlas.schema import ParserOutput, SensoryObject


BACKEND_TFIDF = "tfidf_char_ngram"
DEFAULT_FALLBACK_CONFIDENCE = 0.55


@dataclass(frozen=True)
class SemanticSearchIndex:
    documents: list[dict[str, Any]]
    backend: str = BACKEND_TFIDF


class FallbackEvaluationRow(BaseModel):
    test_id: str
    input_text: str
    target_objects: list[str] = Field(default_factory=list)
    rule_detected_objects: list[str] = Field(default_factory=list)
    rule_top1_hit: bool
    rule_top3_hit: bool
    fallback_used: bool
    fallback_reason: str | None = None
    semantic_matches: list[str] = Field(default_factory=list)
    fallback_top1_hit: bool
    fallback_top3_hit: bool
    fallback_helped: bool
    fallback_hurt: bool


class FallbackEvaluationReport(BaseModel):
    dataset_name: str
    total: int
    rule_top1_hits: int
    rule_top3_hits: int
    fallback_assist_top1_hits: int
    fallback_assist_top3_hits: int
    fallback_used_count: int
    fallback_helped_count: int
    fallback_hurt_count: int
    low_confidence_count: int
    rule_top1_hit_rate: float
    rule_top3_hit_rate: float
    fallback_assist_top1_hit_rate: float
    fallback_assist_top3_hit_rate: float
    rows: list[FallbackEvaluationRow] = Field(default_factory=list)


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item is not None]
    if isinstance(value, dict):
        return [str(item) for item in value.values() if item is not None]
    return [str(value)]


def _flatten_text(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, dict):
        items: list[str] = []
        for key, nested in value.items():
            items.append(str(key))
            items.extend(_flatten_text(nested))
        return items
    if isinstance(value, list):
        items: list[str] = []
        for nested in value:
            items.extend(_flatten_text(nested))
        return items
    return [str(value)]


def _load_phrase_cues(path: str | Path | None = None) -> dict[str, Any]:
    cues_path = Path(path) if path else PHRASE_CUES_PATH
    if not cues_path.exists():
        return {}
    return json.loads(cues_path.read_text(encoding="utf-8"))


def _phrase_cues_for_object(phrase_cues: dict[str, Any] | None, object_id: str) -> list[str]:
    if not phrase_cues:
        return []
    payload = phrase_cues.get(object_id, {})
    if isinstance(payload, list):
        return _flatten_text(payload)
    if isinstance(payload, dict):
        return _flatten_text(payload.get("positive_cues", []))
    return []


def _document_id(record: dict[str, Any]) -> str:
    return str(record.get("object_id") or record.get("candidate_object_id") or "")


def build_document_text(doc: dict[str, Any]) -> str:
    fields = [
        doc.get("object_id"),
        doc.get("label"),
        doc.get("korean_label"),
        doc.get("family"),
        doc.get("object_role"),
        doc.get("definition"),
        doc.get("document_source_note"),
    ]
    fields.extend(_flatten_text(doc.get("core_axes")))
    fields.extend(_flatten_text(doc.get("example_expressions")))
    fields.extend(_flatten_text(doc.get("phrase_cues")))
    fields.extend(_flatten_text(doc.get("suggested_phrase_cues")))
    fields.extend(_flatten_text(doc.get("related_existing_objects")))
    fields.extend(_flatten_text(doc.get("related_objects")))
    fields.extend(_flatten_text(doc.get("source_domains")))
    return " ".join(item for item in _flatten_text(fields) if item).strip()


def build_semantic_documents(
    main_objects: list[SensoryObject | dict[str, Any]],
    candidate_objects: list[dict[str, Any]] | None = None,
    phrase_cues: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    documents: list[dict[str, Any]] = []
    main_object_ids: set[str] = set()

    for item in main_objects:
        record = item.model_dump(mode="json") if isinstance(item, SensoryObject) else dict(item)
        object_id = _document_id(record)
        main_object_ids.add(object_id)
        doc = {
            "object_id": object_id,
            "object_source": "main_ontology",
            "label": record.get("label", ""),
            "korean_label": record.get("korean_label", ""),
            "family": record.get("family", ""),
            "object_role": record.get("object_role", ""),
            "definition": record.get("definition", ""),
            "core_axes": record.get("core_axes", {}),
            "example_expressions": record.get("example_expressions", []),
            "phrase_cues": _phrase_cues_for_object(phrase_cues, object_id),
            "related_objects": record.get("related_objects", []),
            "document_source_note": "trusted main sensory ontology",
        }
        doc["document_text"] = build_document_text(doc)
        documents.append(doc)

    for record in candidate_objects or []:
        object_id = _document_id(record)
        if object_id in main_object_ids:
            continue
        doc = {
            "object_id": object_id,
            "object_source": "candidate_object",
            "label": record.get("label", ""),
            "korean_label": record.get("korean_label", ""),
            "family": record.get("family", ""),
            "object_role": "candidate",
            "definition": record.get("definition", ""),
            "core_axes": record.get("core_axes", {}),
            "example_expressions": record.get("example_expressions", []),
            "suggested_phrase_cues": record.get("suggested_phrase_cues", []),
            "related_existing_objects": record.get("related_existing_objects", []),
            "source_domains": record.get("source_domains", []),
            "document_source_note": "lower-trust candidate object",
        }
        doc["document_text"] = build_document_text(doc)
        documents.append(doc)

    return [doc for doc in documents if doc.get("object_id") and doc.get("document_text")]


def load_semantic_documents(include_candidates: bool = True) -> list[dict[str, Any]]:
    objects = [
        SensoryObject.model_validate(record)
        for record in read_jsonl(SENSORY_OBJECTS_PATH)
    ]
    candidates = read_jsonl(CANDIDATE_OBJECTS_PATH) if include_candidates and CANDIDATE_OBJECTS_PATH.exists() else []
    return build_semantic_documents(objects, candidates, _load_phrase_cues())


def _match_reason(query: str, doc: dict[str, Any]) -> list[str]:
    normalized_query = query.casefold()
    reasons = ["semantic text similarity"]
    for field_name, label in (
        ("korean_label", "matched object label language"),
        ("family", "matched family language"),
        ("definition", "matched definition language"),
        ("document_text", "matched ontology/example language"),
    ):
        for token in _as_list(doc.get(field_name)):
            if len(token) >= 2 and token.casefold() in normalized_query:
                reasons.append(label)
                return reasons
    return reasons


def search_semantic_matches(
    query: str,
    documents: list[dict[str, Any]],
    top_k: int = 5,
    backend: str = BACKEND_TFIDF,
) -> list[dict[str, Any]]:
    if backend != BACKEND_TFIDF:
        raise ValueError(f"Unsupported semantic fallback backend: {backend}")
    if not query.strip() or not documents:
        return []

    corpus = [doc.get("document_text", "") for doc in documents]
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=1)
    matrix = vectorizer.fit_transform([query, *corpus])
    scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    ranked = sorted(enumerate(scores), key=lambda item: (-item[1], item[0]))[:top_k]
    matches: list[dict[str, Any]] = []
    for rank, (index, score) in enumerate(ranked, start=1):
        doc = documents[index]
        example = _as_list(doc.get("example_expressions"))
        matches.append(
            {
                "rank": rank,
                "object_id": doc["object_id"],
                "object_source": doc["object_source"],
                "korean_label": doc.get("korean_label", ""),
                "label": doc.get("label", ""),
                "family": doc.get("family", ""),
                "object_role": doc.get("object_role", ""),
                "similarity": round(float(score), 4),
                "match_reason": _match_reason(query, doc),
                "definition": doc.get("definition", ""),
                "example_expression": example[0] if example else "",
            }
        )
    return matches


def should_use_semantic_fallback(
    parser_output: ParserOutput,
    min_confidence: float = DEFAULT_FALLBACK_CONFIDENCE,
    low_confidence_only: bool = True,
) -> tuple[bool, str | None]:
    top_score = parser_output.anchor_object.score if parser_output.anchor_object else 0.0
    if parser_output.low_confidence:
        return True, "low_confidence"
    if parser_output.confidence < min_confidence:
        return True, "confidence_below_threshold"
    if not parser_output.detected_objects or top_score <= 0.0:
        return True, "no_strong_detected_object"
    if parser_output.clarification_questions and parser_output.confidence < 0.75:
        return True, "ambiguous_with_clarification_questions"
    if not low_confidence_only:
        return True, "forced"
    return False, None


def run_semantic_fallback(
    query: str,
    parser_output: ParserOutput,
    top_k: int = 5,
    include_candidates: bool = True,
    backend: str = BACKEND_TFIDF,
    *,
    force: bool = False,
) -> dict[str, Any]:
    fallback_used, reason = should_use_semantic_fallback(parser_output, low_confidence_only=not force)
    if force:
        fallback_used = True
        reason = reason or "forced"
    if not fallback_used:
        return {
            "fallback_used": False,
            "fallback_reason": None,
            "backend": backend,
            "query": query,
            "matches": [],
        }

    documents = load_semantic_documents(include_candidates=include_candidates)
    return {
        "fallback_used": True,
        "fallback_reason": reason,
        "backend": backend,
        "query": query,
        "matches": search_semantic_matches(query, documents, top_k=top_k, backend=backend),
    }


def evaluate_semantic_fallback(
    test_records: list[dict[str, Any]],
    sensory_objects: list[SensoryObject],
    *,
    dataset_name: str,
    top_k: int = 5,
    include_candidates: bool = True,
) -> FallbackEvaluationReport:
    documents = load_semantic_documents(include_candidates=include_candidates)
    rows: list[FallbackEvaluationRow] = []

    for index, record in enumerate(test_records, start=1):
        input_text = record["raw_text"]
        targets = list(record.get("target_objects", []))
        parser_output = __import__("sensory_atlas.parser", fromlist=["parse_sentence"]).parse_sentence(
            input_text,
            sensory_objects,
            use_semantic_fallback=False,
        )
        detected = [item.object_id for item in parser_output.detected_objects]
        rule_top1_hit = bool(set(detected[:1]) & set(targets))
        rule_top3_hit = bool(set(detected[:3]) & set(targets))
        fallback_used, reason = should_use_semantic_fallback(parser_output)
        matches = search_semantic_matches(input_text, documents, top_k=top_k) if fallback_used else []
        semantic_ids = [match["object_id"] for match in matches]
        fallback_top1_hit = bool(set(semantic_ids[:1]) & set(targets)) if fallback_used else False
        fallback_top3_hit = bool(set(semantic_ids[:3]) & set(targets)) if fallback_used else False
        rows.append(
            FallbackEvaluationRow(
                test_id=record.get("test_id", f"test_{index:03d}"),
                input_text=input_text,
                target_objects=targets,
                rule_detected_objects=detected,
                rule_top1_hit=rule_top1_hit,
                rule_top3_hit=rule_top3_hit,
                fallback_used=fallback_used,
                fallback_reason=reason,
                semantic_matches=semantic_ids,
                fallback_top1_hit=fallback_top1_hit,
                fallback_top3_hit=fallback_top3_hit,
                fallback_helped=(not rule_top3_hit and fallback_top3_hit),
                fallback_hurt=(rule_top3_hit and fallback_used and not fallback_top3_hit),
            )
        )

    total = len(rows)
    fallback_used_count = sum(row.fallback_used for row in rows)
    fallback_top1 = sum(row.fallback_top1_hit for row in rows)
    fallback_top3 = sum(row.fallback_top3_hit for row in rows)
    return FallbackEvaluationReport(
        dataset_name=dataset_name,
        total=total,
        rule_top1_hits=sum(row.rule_top1_hit for row in rows),
        rule_top3_hits=sum(row.rule_top3_hit for row in rows),
        fallback_assist_top1_hits=fallback_top1,
        fallback_assist_top3_hits=fallback_top3,
        fallback_used_count=fallback_used_count,
        fallback_helped_count=sum(row.fallback_helped for row in rows),
        fallback_hurt_count=sum(row.fallback_hurt for row in rows),
        low_confidence_count=sum(row.fallback_reason == "low_confidence" for row in rows),
        rule_top1_hit_rate=round(sum(row.rule_top1_hit for row in rows) / total, 2) if total else 0.0,
        rule_top3_hit_rate=round(sum(row.rule_top3_hit for row in rows) / total, 2) if total else 0.0,
        fallback_assist_top1_hit_rate=round(fallback_top1 / fallback_used_count, 2) if fallback_used_count else 0.0,
        fallback_assist_top3_hit_rate=round(fallback_top3 / fallback_used_count, 2) if fallback_used_count else 0.0,
        rows=rows,
    )


def write_fallback_report(
    report_path: str | Path,
    summary_path: str | Path,
    report: FallbackEvaluationReport,
) -> None:
    report_path = Path(report_path)
    summary_path = Path(summary_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Semantic Fallback Evaluation Report",
        "",
        f"- Dataset: {report.dataset_name}",
        f"- Total test sentences: {report.total}",
        f"- Rule Top-1 hit rate: {report.rule_top1_hit_rate:.2f}",
        f"- Rule Top-3 hit rate: {report.rule_top3_hit_rate:.2f}",
        f"- Fallback assist Top-1 hit rate: {report.fallback_assist_top1_hit_rate:.2f}",
        f"- Fallback assist Top-3 hit rate: {report.fallback_assist_top3_hit_rate:.2f}",
        f"- Fallback used count: {report.fallback_used_count}",
        f"- Fallback helped count: {report.fallback_helped_count}",
        f"- Fallback hurt count: {report.fallback_hurt_count}",
        f"- Low confidence count: {report.low_confidence_count}",
        "",
        "| Test ID | Fallback Used | Reason | Targets | Rule Top 3 | Semantic Top 3 | Helped | Hurt |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in report.rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.test_id,
                    str(row.fallback_used),
                    row.fallback_reason or "",
                    ", ".join(row.target_objects),
                    ", ".join(row.rule_detected_objects[:3]),
                    ", ".join(row.semantic_matches[:3]),
                    str(row.fallback_helped),
                    str(row.fallback_hurt),
                ]
            )
            + " |"
        )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    summary_path.write_text(
        json.dumps(report.model_dump(mode="json", exclude={"rows"}), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
