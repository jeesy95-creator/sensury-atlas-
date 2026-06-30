"""Candidate sensory object review workflow utilities."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from sensory_atlas.loaders import project_root, read_jsonl


ALLOWED_REVIEW_STATUSES = {
    "unreviewed",
    "reviewing",
    "approved_for_curated_merge",
    "needs_more_examples",
    "needs_distinction_review",
    "rejected",
    "merged",
}
ALLOWED_PRIORITIES = {"high", "medium", "low"}
RECOMMENDED_ACTIONS = {
    "ready_for_curated_merge",
    "needs_more_examples",
    "needs_distinction_review",
    "keep_as_candidate",
    "keep_as_axis_descriptor",
    "do_not_merge_yet",
}
NOTE_LIKE_TERMS = {
    "bergamot",
    "neroli",
    "orange",
    "musk",
    "amber",
    "oak",
    "vanilla",
    "fruit",
    "spice",
    "herbal",
    "coffee",
    "wine",
    "whisky",
    "jasmine",
    "rose",
}
SENSORY_AXIS_KEYS = {
    "material",
    "temperature",
    "texture",
    "light",
    "motion",
    "time",
    "atmosphere",
    "density",
    "rendering",
    "organic_mineral",
}
ARCHETYPE_WORDS = {
    "air",
    "skin",
    "surface",
    "warmth",
    "coolness",
    "texture",
    "atmosphere",
    "glow",
    "density",
    "body",
    "finish",
    "flow",
    "spark",
    "smoke",
    "softness",
    "clarity",
    "edge",
    "depth",
}


def _resolve(path: str | Path) -> Path:
    path = Path(path)
    if path.is_absolute():
        return path
    return project_root() / path


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item is not None]
    return [str(value)]


def _tokenize(value: Any) -> set[str]:
    text = " ".join(_as_list(value)).casefold()
    return {token for token in re.findall(r"[a-z0-9가-힣]+", text) if len(token) >= 2}


def _score_from_count(count: int, high: int, medium: int) -> float:
    if count >= high:
        return 1.0
    if count >= medium:
        return 0.65
    if count > 0:
        return 0.35
    return 0.0


def load_candidate_objects(path: str | Path = "data/sensory_object_candidates.jsonl") -> list[dict[str, Any]]:
    return read_jsonl(_resolve(path))


def load_existing_objects(path: str | Path = "data/sensory_objects.jsonl") -> list[dict[str, Any]]:
    return read_jsonl(_resolve(path))


def load_candidate_review_status(
    path: str | Path = "data/candidate_review_status.jsonl",
) -> dict[str, dict[str, Any]]:
    status_path = _resolve(path)
    if not status_path.exists():
        return {}
    rows = read_jsonl(status_path)
    return {str(row["candidate_object_id"]): row for row in rows}


def _axis_overlap(candidate: dict[str, Any], existing: dict[str, Any]) -> float:
    candidate_axes = candidate.get("core_axes", {}) or {}
    existing_axes = existing.get("core_axes", {}) or {}
    if not candidate_axes or not existing_axes:
        return 0.0

    overlap = 0
    total = len(set(candidate_axes) | set(existing_axes))
    for axis, candidate_value in candidate_axes.items():
        existing_value = existing_axes.get(axis)
        if not existing_value:
            continue
        if set(_as_list(candidate_value)) & set(_as_list(existing_value)):
            overlap += 1
    return overlap / max(total, 1)


def _family_overlap(candidate: dict[str, Any], existing: dict[str, Any]) -> float:
    candidate_tokens = _tokenize(candidate.get("family", ""))
    existing_tokens = _tokenize(existing.get("family", ""))
    if not candidate_tokens or not existing_tokens:
        return 0.0
    return len(candidate_tokens & existing_tokens) / len(candidate_tokens | existing_tokens)


def _text_overlap(candidate: dict[str, Any], existing: dict[str, Any]) -> float:
    candidate_tokens = _tokenize(
        [
            candidate.get("definition", ""),
            *candidate.get("example_expressions", []),
            *candidate.get("suggested_phrase_cues", []),
        ]
    )
    existing_tokens = _tokenize(
        [
            existing.get("definition", ""),
            *existing.get("example_expressions", []),
            existing.get("label", ""),
            existing.get("korean_label", ""),
        ]
    )
    if not candidate_tokens or not existing_tokens:
        return 0.0
    return len(candidate_tokens & existing_tokens) / len(candidate_tokens | existing_tokens)


def compare_candidate_to_existing(
    candidate: dict[str, Any],
    existing_objects: list[dict[str, Any]],
    *,
    limit: int = 5,
) -> list[dict[str, Any]]:
    related = set(candidate.get("related_existing_objects", []))
    rows: list[dict[str, Any]] = []
    for existing in existing_objects:
        reasons: list[str] = []
        object_id = str(existing.get("object_id", ""))
        family_score = _family_overlap(candidate, existing)
        axis_score = _axis_overlap(candidate, existing)
        text_score = _text_overlap(candidate, existing)
        related_score = 1.0 if object_id in related else 0.0

        if related_score:
            reasons.append("related_existing_object")
        if family_score >= 0.15:
            reasons.append("family_overlap")
        if axis_score >= 0.20:
            reasons.append("axis_overlap")
        if text_score >= 0.03:
            reasons.append("keyword_overlap")

        overlap_score = min(
            1.0,
            0.35 * related_score + 0.25 * family_score + 0.25 * axis_score + 0.15 * text_score,
        )
        if overlap_score <= 0:
            continue
        rows.append(
            {
                "existing_object_id": object_id,
                "similarity_reason": reasons,
                "overlap_score": round(overlap_score, 2),
            }
        )

    return sorted(rows, key=lambda row: row["overlap_score"], reverse=True)[:limit]


def _note_dictionary_risk(candidate: dict[str, Any]) -> float:
    label_tokens = _tokenize([candidate.get("label", ""), candidate.get("candidate_object_id", "")])
    definition_tokens = _tokenize(candidate.get("definition", ""))
    note_hits = len(label_tokens & NOTE_LIKE_TERMS)
    has_archetype_language = bool((label_tokens | definition_tokens) & ARCHETYPE_WORDS)
    risk = min(1.0, 0.25 + 0.18 * note_hits)
    if has_archetype_language:
        risk -= 0.20
    if len(candidate.get("source_domains", [])) > 1:
        risk -= 0.10
    return round(max(0.0, min(risk, 1.0)), 2)


def compute_candidate_readiness(
    candidate: dict[str, Any],
    existing_objects: list[dict[str, Any]],
) -> dict[str, Any]:
    axes = candidate.get("core_axes", {}) or {}
    axis_count = len(set(axes) & SENSORY_AXIS_KEYS)
    definition_tokens = _tokenize(candidate.get("definition", ""))
    label_tokens = _tokenize([candidate.get("label", ""), candidate.get("candidate_object_id", "")])
    has_archetype_language = bool((definition_tokens | label_tokens) & ARCHETYPE_WORDS)

    sensory_archetype_score = min(1.0, 0.25 + 0.12 * axis_count + (0.20 if has_archetype_language else 0.0))
    cross_domain_reuse_score = _score_from_count(len(candidate.get("source_domains", [])), high=3, medium=2)
    example_coverage_score = _score_from_count(len(candidate.get("example_expressions", [])), high=5, medium=3)
    phrase_cue_readiness_score = _score_from_count(len(candidate.get("suggested_phrase_cues", [])), high=5, medium=3)
    negative_cue_readiness_score = _score_from_count(len(candidate.get("negative_cues", [])), high=3, medium=1)
    similar = compare_candidate_to_existing(candidate, existing_objects)
    max_overlap = similar[0]["overlap_score"] if similar else 0.0
    distinctiveness_score = round(max(0.0, 1.0 - max_overlap), 2)
    note_dictionary_risk = _note_dictionary_risk(candidate)

    positive_scores = [
        sensory_archetype_score,
        cross_domain_reuse_score,
        distinctiveness_score,
        example_coverage_score,
        phrase_cue_readiness_score,
        negative_cue_readiness_score,
    ]
    overall = sum(positive_scores) / len(positive_scores)
    overall = max(0.0, overall - note_dictionary_risk * 0.18)

    if note_dictionary_risk >= 0.70 or sensory_archetype_score < 0.45:
        recommended_action = "do_not_merge_yet"
    elif phrase_cue_readiness_score < 0.65 or example_coverage_score < 0.65:
        recommended_action = "needs_more_examples"
    elif distinctiveness_score < 0.55:
        recommended_action = "needs_distinction_review"
    elif "descriptor" in str(candidate.get("family", "")).casefold():
        recommended_action = "keep_as_axis_descriptor"
    elif overall >= 0.72 and note_dictionary_risk <= 0.45:
        recommended_action = "ready_for_curated_merge"
    else:
        recommended_action = "keep_as_candidate"

    return {
        "sensory_archetype_score": round(sensory_archetype_score, 2),
        "cross_domain_reuse_score": round(cross_domain_reuse_score, 2),
        "distinctiveness_score": distinctiveness_score,
        "example_coverage_score": round(example_coverage_score, 2),
        "phrase_cue_readiness_score": round(phrase_cue_readiness_score, 2),
        "negative_cue_readiness_score": round(negative_cue_readiness_score, 2),
        "note_dictionary_risk": note_dictionary_risk,
        "overall_readiness_score": round(overall, 2),
        "recommended_action": recommended_action,
        "similar_existing_objects": similar,
    }


def candidate_to_review_row(candidate: dict[str, Any], status: dict[str, Any] | None = None) -> dict[str, Any]:
    status = status or {}
    return {
        "candidate_object_id": candidate.get("candidate_object_id"),
        "korean_label": candidate.get("korean_label"),
        "label": candidate.get("label"),
        "source_domains": candidate.get("source_domains", []),
        "family": candidate.get("family"),
        "review_status": status.get("review_status", "unreviewed"),
        "recommended_action": status.get("recommended_action", "keep_as_candidate"),
        "priority": status.get("priority", "medium"),
        "reviewer_notes": status.get("reviewer_notes", ""),
        "promoted_to_object_id": status.get("promoted_to_object_id"),
        "reviewed_at": status.get("reviewed_at"),
    }


def generate_promotion_draft(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "object_id": candidate.get("candidate_object_id"),
        "label": candidate.get("label"),
        "korean_label": candidate.get("korean_label"),
        "object_type": "sensory_object_draft",
        "family": candidate.get("family"),
        "definition": candidate.get("definition"),
        "core_axes": candidate.get("core_axes", {}),
        "example_expressions": candidate.get("example_expressions", []),
        "related_objects": candidate.get("related_existing_objects", []),
        "opposite_objects": [],
        "associated_products": [],
        "evidence_refs": ["candidate_v1.1"],
        "status": "draft_from_candidate",
    }


def build_candidate_review_rows(
    candidates: list[dict[str, Any]],
    existing_objects: list[dict[str, Any]],
    review_status: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    review_status = review_status or {}
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        readiness = compute_candidate_readiness(candidate, existing_objects)
        status = dict(review_status.get(str(candidate["candidate_object_id"]), {}))
        status.setdefault("recommended_action", readiness["recommended_action"])
        row = candidate_to_review_row(candidate, status)
        row.update(readiness)
        rows.append(row)
    return rows


def summarize_candidate_actions(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(str(row.get("recommended_action", "keep_as_candidate")) for row in rows)
    return {action: counts.get(action, 0) for action in sorted(RECOMMENDED_ACTIONS)}


def _family_bucket(candidate: dict[str, Any]) -> str:
    text = " ".join(
        [
            str(candidate.get("family", "")),
            str(candidate.get("label", "")),
            str(candidate.get("korean_label", "")),
            str(candidate.get("definition", "")),
        ]
    ).casefold()
    buckets = [
        ("clean / skin / musk", {"clean", "skin", "musk", "laundry", "soap", "비누", "세탁", "살갗"}),
        ("powder / textile / softness", {"powder", "soft", "textile", "milk", "lactonic", "가루", "부드", "우유"}),
        ("smoke / resin / wood", {"smoke", "resin", "oak", "wood", "peat", "incense", "연기", "수지", "오크"}),
        ("wet / earth / green", {"wet", "soil", "green", "leaf", "earth", "fig", "흙", "잎", "초록"}),
        ("mineral / glass / clarity", {"mineral", "glass", "clarity", "stone", "cold", "광물", "유리"}),
        ("warm / amber / density", {"amber", "golden", "density", "syrup", "glow", "앰버", "금빛", "밀도"}),
        ("finish / dryness / texture", {"finish", "dry", "astringent", "tannin", "body", "드라이", "수렴", "마무리"}),
    ]
    for bucket, keywords in buckets:
        if any(keyword in text for keyword in keywords):
            return bucket
    return "other sensory archetype"


def _selection_reasons(row: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if row["sensory_archetype_score"] >= 0.8:
        reasons.append("strong sensory archetype")
    if row["cross_domain_reuse_score"] >= 0.65:
        reasons.append("cross-domain reusable")
    if row["note_dictionary_risk"] <= 0.35:
        reasons.append("low note dictionary risk")
    if row["distinctiveness_score"] >= 0.55:
        reasons.append("distinct from existing ontology")
    if row["phrase_cue_readiness_score"] >= 0.65:
        reasons.append("phrase cue ready")
    if row["negative_cue_readiness_score"] >= 1.0:
        reasons.append("negative cues available")
    return reasons or ["selected for manual ontology review"]


def _promotion_risk(row: dict[str, Any]) -> str:
    if row["note_dictionary_risk"] >= 0.45 or row["distinctiveness_score"] < 0.60:
        return "medium"
    return "low"


def _selection_priority(row: dict[str, Any]) -> float:
    bucket_bonus = 0.04 if _family_bucket(row) != "other sensory archetype" else 0.0
    return round(
        row["overall_readiness_score"] * 0.34
        + row["sensory_archetype_score"] * 0.18
        + row["cross_domain_reuse_score"] * 0.14
        + row["distinctiveness_score"] * 0.16
        + row["negative_cue_readiness_score"] * 0.08
        - row["note_dictionary_risk"] * 0.18
        + bucket_bonus,
        4,
    )


def _shortlist_row(candidate: dict[str, Any], review_row: dict[str, Any]) -> dict[str, Any]:
    score_keys = [
        "overall_readiness_score",
        "sensory_archetype_score",
        "cross_domain_reuse_score",
        "distinctiveness_score",
        "example_coverage_score",
        "phrase_cue_readiness_score",
        "negative_cue_readiness_score",
        "note_dictionary_risk",
    ]
    return {
        "candidate_object_id": candidate["candidate_object_id"],
        "korean_label": candidate.get("korean_label", ""),
        "source_domains": candidate.get("source_domains", []),
        "family": candidate.get("family", ""),
        "selection_status": "selected_for_v1_5_review",
        "selection_reason": _selection_reasons(review_row),
        "readiness_scores": {key: review_row[key] for key in score_keys},
        "related_existing_objects": candidate.get("related_existing_objects", []),
        "similar_existing_objects": review_row.get("similar_existing_objects", []),
        "promotion_risk": _promotion_risk(review_row),
        "review_notes": (
            "Good candidate for curated ontology expansion, but should remain distinct "
            "from related existing sensory objects."
        ),
        "next_action": "manual_review_before_v1_5_merge",
    }


def select_curated_shortlist(
    candidates: list[dict[str, Any]],
    existing_objects: list[dict[str, Any]],
    review_status: dict[str, dict[str, Any]],
    min_count: int = 10,
    max_count: int = 12,
) -> list[dict[str, Any]]:
    rows = build_candidate_review_rows(candidates, existing_objects, review_status)
    candidate_lookup = {candidate["candidate_object_id"]: candidate for candidate in candidates}
    ready_rows = [
        row
        for row in rows
        if row["recommended_action"] == "ready_for_curated_merge"
        and row["note_dictionary_risk"] < 0.50
    ]
    ranked = sorted(
        ready_rows,
        key=lambda row: (
            -_selection_priority(row),
            row["note_dictionary_risk"],
            row["candidate_object_id"],
        ),
    )

    selected: list[dict[str, Any]] = []
    bucket_counts: Counter[str] = Counter()
    for row in ranked:
        bucket = _family_bucket(row)
        if bucket_counts[bucket] >= 2 and len(selected) < min_count:
            continue
        selected.append(row)
        bucket_counts[bucket] += 1
        if len(selected) >= max_count:
            break

    if len(selected) < min_count:
        selected_ids = {row["candidate_object_id"] for row in selected}
        for row in ranked:
            if row["candidate_object_id"] in selected_ids:
                continue
            selected.append(row)
            selected_ids.add(row["candidate_object_id"])
            if len(selected) >= min_count:
                break

    return [
        _shortlist_row(candidate_lookup[row["candidate_object_id"]], row)
        for row in selected[:max_count]
    ]


def load_curated_shortlist(
    path: str | Path = "data/curated_candidate_shortlist_v1_5.jsonl",
) -> list[dict[str, Any]]:
    shortlist_path = _resolve(path)
    if not shortlist_path.exists():
        return []
    return read_jsonl(shortlist_path)


def summarize_shortlist_family_coverage(shortlist: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(_family_bucket(row) for row in shortlist)
    return dict(sorted(counts.items()))


def _shortlist_summary(
    candidates: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    shortlist: list[dict[str, Any]],
) -> dict[str, Any]:
    ready_rows = [row for row in rows if row["recommended_action"] == "ready_for_curated_merge"]
    selected_ids = [row["candidate_object_id"] for row in shortlist]
    selected_risks = [
        row["readiness_scores"]["note_dictionary_risk"]
        for row in shortlist
    ]
    return {
        "version": "v1.4.1",
        "total_candidates": len(candidates),
        "ready_for_curated_merge_reviewed": len(ready_rows),
        "selected_count": len(shortlist),
        "excluded_ready_count": len(ready_rows) - len(shortlist),
        "selected_candidate_ids": selected_ids,
        "family_coverage": summarize_shortlist_family_coverage(shortlist),
        "highest_readiness_candidate": max(
            shortlist,
            key=lambda row: row["readiness_scores"]["overall_readiness_score"],
        )["candidate_object_id"] if shortlist else None,
        "highest_risk_candidate_among_selected": shortlist[
            selected_risks.index(max(selected_risks))
        ]["candidate_object_id"] if shortlist else None,
        "selection_notes": (
            "Shortlist created for v1.5 manual ontology expansion review. "
            "No candidates were merged into the main ontology."
        ),
    }


def generate_curated_shortlist_report(
    candidates: list[dict[str, Any]],
    existing_objects: list[dict[str, Any]],
    review_status: dict[str, dict[str, Any]],
    shortlist: list[dict[str, Any]],
) -> str:
    rows = build_candidate_review_rows(candidates, existing_objects, review_status)
    ready_rows = [row for row in rows if row["recommended_action"] == "ready_for_curated_merge"]
    selected_ids = {row["candidate_object_id"] for row in shortlist}
    excluded_ready = [row for row in ready_rows if row["candidate_object_id"] not in selected_ids]
    candidate_lookup = {candidate["candidate_object_id"]: candidate for candidate in candidates}
    summary = _shortlist_summary(candidates, rows, shortlist)

    lines = [
        "# Curated Candidate Shortlist Report v1.4.1",
        "",
        "## Summary",
        f"- Total candidates: {summary['total_candidates']}",
        f"- Ready-for-merge candidates reviewed: {summary['ready_for_curated_merge_reviewed']}",
        f"- Selected candidates: {summary['selected_count']}",
        f"- Excluded ready candidates: {summary['excluded_ready_count']}",
        f"- Families covered: {len(summary['family_coverage'])}",
        f"- Highest readiness candidate: {summary['highest_readiness_candidate']}",
        f"- Highest risk candidate among selected: {summary['highest_risk_candidate_among_selected']}",
        "",
        "## Selection Principles",
        "This is a shortlist, not an ontology merge. Candidates are selected for manual v1.5 review only.",
        "Selection prioritizes reusable sensory archetypes, cross-domain usefulness, low note dictionary risk, distinctiveness, and family diversity.",
        "",
        "## Selected Candidates",
        "",
        "| candidate_object_id | korean_label | family | overall_readiness_score | note_dictionary_risk | promotion_risk | selection_reason |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in shortlist:
        scores = row["readiness_scores"]
        lines.append(
            f"| {row['candidate_object_id']} | {row['korean_label']} | {row['family']} | {scores['overall_readiness_score']:.2f} | {scores['note_dictionary_risk']:.2f} | {row['promotion_risk']} | {', '.join(row['selection_reason'])} |"
        )

    lines.extend(["", "## Family Coverage"])
    for family, count in summary["family_coverage"].items():
        lines.append(f"- {family}: {count}")

    lines.extend(["", "## Excluded Ready Candidates"])
    if not excluded_ready:
        lines.append("- No ready candidates were excluded.")
    for row in excluded_ready:
        reasons: list[str] = []
        if row["note_dictionary_risk"] >= 0.35:
            reasons.append("too note-like for batch 1")
        if row["distinctiveness_score"] < 0.65:
            reasons.append("too close to existing object")
        if row["cross_domain_reuse_score"] < 0.65:
            reasons.append("less cross-domain reusable")
        if not reasons:
            reasons.append("lower priority for batch 1")
        lines.append(f"- {row['candidate_object_id']}: {', '.join(reasons)}")

    lines.extend(["", "## Candidate Details"])
    for row in shortlist:
        candidate = candidate_lookup[row["candidate_object_id"]]
        lines.extend(
            [
                "",
                f"### {row['candidate_object_id']} / {row['korean_label']}",
                f"- definition: {candidate.get('definition', '')}",
                f"- core axes: `{json.dumps(candidate.get('core_axes', {}), ensure_ascii=False)}`",
                f"- example expressions: {', '.join(candidate.get('example_expressions', []))}",
                f"- suggested phrase cues: {', '.join(candidate.get('suggested_phrase_cues', []))}",
                f"- negative cues: {', '.join(candidate.get('negative_cues', []))}",
                f"- related existing objects: {', '.join(candidate.get('related_existing_objects', []))}",
                f"- similar existing objects: {json.dumps(row.get('similar_existing_objects', []), ensure_ascii=False)}",
                f"- promotion risks: {row['promotion_risk']}",
                f"- recommended next action: {row['next_action']}",
            ]
        )

    lines.extend(
        [
            "",
            "## Next Step: v1.5 Curated Ontology Expansion",
            "- Manually review selected candidates.",
            "- Add only selected candidates to main ontology in v1.5.",
            "- Add phrase cues and negative cues for promoted objects.",
            "- Add regression tests for promoted objects.",
            "- Do not modify holdout during curated expansion.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_curated_shortlist_outputs(
    output_path: str | Path = "data/curated_candidate_shortlist_v1_5.jsonl",
    report_path: str | Path = "outputs/curated_candidate_shortlist_report.md",
    summary_path: str | Path = "outputs/curated_candidate_shortlist_summary.json",
    *,
    min_count: int = 10,
    max_count: int = 12,
) -> tuple[Path, Path, Path, list[dict[str, Any]], dict[str, Any]]:
    candidates = load_candidate_objects()
    existing_objects = load_existing_objects()
    review_status = load_candidate_review_status()
    rows = build_candidate_review_rows(candidates, existing_objects, review_status)
    shortlist = select_curated_shortlist(
        candidates,
        existing_objects,
        review_status,
        min_count=min_count,
        max_count=max_count,
    )
    report = generate_curated_shortlist_report(candidates, existing_objects, review_status, shortlist)
    summary = _shortlist_summary(candidates, rows, shortlist)

    resolved_output_path = _resolve(output_path)
    resolved_report_path = _resolve(report_path)
    resolved_summary_path = _resolve(summary_path)
    for path in (resolved_output_path, resolved_report_path, resolved_summary_path):
        path.parent.mkdir(parents=True, exist_ok=True)

    resolved_output_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in shortlist),
        encoding="utf-8",
    )
    resolved_report_path.write_text(report, encoding="utf-8")
    resolved_summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return resolved_output_path, resolved_report_path, resolved_summary_path, shortlist, summary


def generate_candidate_review_report(
    candidates: list[dict[str, Any]],
    existing_objects: list[dict[str, Any]],
    review_status: dict[str, dict[str, Any]] | None = None,
) -> str:
    rows = build_candidate_review_rows(candidates, existing_objects, review_status)
    action_counts = summarize_candidate_actions(rows)
    lookup = {candidate["candidate_object_id"]: candidate for candidate in candidates}

    lines = [
        "# Candidate Sensory Object Review Report",
        "",
        "## Summary",
        f"- Total candidates: {len(rows)}",
    ]
    for action, count in action_counts.items():
        lines.append(f"- {action}: {count}")

    high_priority = [row for row in rows if row.get("priority") == "high"]
    lines.extend(
        [
            "",
            "## High-Priority Candidates",
            "",
            "| candidate_object_id | korean_label | source_domains | recommended_action | readiness_score | note_dictionary_risk |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in high_priority:
        source_domains = ", ".join(row.get("source_domains", []))
        lines.append(
            f"| {row['candidate_object_id']} | {row['korean_label']} | {source_domains} | {row['recommended_action']} | {row['overall_readiness_score']:.2f} | {row['note_dictionary_risk']:.2f} |"
        )
    if not high_priority:
        lines.append("| - | - | - | - | - | - |")

    ready_rows = [row for row in rows if row["recommended_action"] == "ready_for_curated_merge"]
    lines.extend(["", "## Ready for Curated Merge"])
    if not ready_rows:
        lines.append("- No candidates currently recommended for curated merge.")
    for row in ready_rows:
        candidate = lookup[row["candidate_object_id"]]
        lines.extend(
            [
                "",
                f"### {candidate['candidate_object_id']} / {candidate.get('korean_label', '')}",
                f"- definition: {candidate.get('definition', '')}",
                f"- core axes: `{json.dumps(candidate.get('core_axes', {}), ensure_ascii=False)}`",
                f"- example expressions: {', '.join(candidate.get('example_expressions', []))}",
                f"- suggested phrase cues: {', '.join(candidate.get('suggested_phrase_cues', []))}",
                f"- negative cues: {', '.join(candidate.get('negative_cues', []))}",
                f"- related existing objects: {', '.join(candidate.get('related_existing_objects', []))}",
                f"- similar existing objects: {json.dumps(row.get('similar_existing_objects', []), ensure_ascii=False)}",
                "",
                "```json",
                json.dumps(generate_promotion_draft(candidate), ensure_ascii=False, indent=2),
                "```",
            ]
        )

    lines.extend(["", "## Needs Distinction Review"])
    distinction_rows = [row for row in rows if row["recommended_action"] == "needs_distinction_review"]
    if not distinction_rows:
        lines.append("- No candidates currently require distinction review.")
    for row in distinction_rows:
        lines.append(
            f"- {row['candidate_object_id']}: similar={json.dumps(row.get('similar_existing_objects', []), ensure_ascii=False)}"
        )

    lines.extend(["", "## Do Not Merge Yet"])
    do_not_merge_rows = [row for row in rows if row["recommended_action"] == "do_not_merge_yet"]
    if not do_not_merge_rows:
        lines.append("- No candidates currently marked do_not_merge_yet.")
    for row in do_not_merge_rows:
        lines.append(
            f"- {row['candidate_object_id']}: risk={row['note_dictionary_risk']:.2f}, readiness={row['overall_readiness_score']:.2f}"
        )

    return "\n".join(lines) + "\n"


def write_candidate_review_outputs(
    report_path: str | Path = "outputs/candidate_review_report.md",
    summary_path: str | Path = "outputs/candidate_review_summary.json",
) -> tuple[Path, Path, list[dict[str, Any]]]:
    candidates = load_candidate_objects()
    existing_objects = load_existing_objects()
    review_status = load_candidate_review_status()
    rows = build_candidate_review_rows(candidates, existing_objects, review_status)
    report = generate_candidate_review_report(candidates, existing_objects, review_status)

    resolved_report_path = _resolve(report_path)
    resolved_summary_path = _resolve(summary_path)
    resolved_report_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_summary_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_report_path.write_text(report, encoding="utf-8")
    resolved_summary_path.write_text(
        json.dumps(
            {
                "total_candidates": len(rows),
                "recommended_actions": summarize_candidate_actions(rows),
                "rows": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return resolved_report_path, resolved_summary_path, rows
