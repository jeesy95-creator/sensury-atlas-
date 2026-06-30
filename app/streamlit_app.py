from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from sensory_atlas.loaders import load_test_sentences
from sensory_atlas.parser import parse_sentence
from sensory_atlas.paths import SENSORY_OBJECTS_PATH
from sensory_atlas.ui_helpers import (
    candidate_detail_for_display,
    candidate_review_rows_to_dataframe,
    curated_shortlist_to_dataframe,
    evaluate_all_datasets,
    get_object_lookup,
    get_candidate_lookup,
    load_candidate_review_for_ui,
    load_objects_for_ui,
    objects_to_dataframe,
    parser_output_to_display_dict,
)


EXAMPLE_INPUTS = [
    "11월 말 새벽 공기처럼 코가 쨍하게 시리고 투명한 느낌",
    "캐시미어 니트처럼 따뜻하고 포근하게 감싸는 향",
    "비 온 뒤 계곡 이끼처럼 차갑고 축축한 초록색 냄새",
    "4K 화면처럼 입자가 다 보이고 차갑게 선명해",
    "해상도는 낮지만 분위기만 남아",
    "차가운 큰 홀의 매끈한 바닥처럼 고요하고 윤이 나",
    "바위틈 사이로 차가운 물줄기가 흐르는 듯한 향",
]


@st.cache_data
def cached_objects():
    return load_objects_for_ui(SENSORY_OBJECTS_PATH)


@st.cache_data
def cached_evaluation():
    return evaluate_all_datasets()


@st.cache_data
def cached_candidate_review():
    return load_candidate_review_for_ui()


def render_axes(axes: dict[str, str]) -> None:
    rows = [{"axis": key, "value": value} for key, value in axes.items() if value]
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)


def render_parse_demo(objects, object_lookup) -> None:
    st.subheader("Parse Demo")
    selected = st.selectbox("Example inputs", EXAMPLE_INPUTS, index=4)
    input_text = st.text_area(
        "어떤 향, 맛, 장면, 질감이 떠오르나요?",
        value=selected,
        placeholder="예: 해상도는 낮지만 분위기만 남아 있는 오래된 영화 같은 향",
        height=110,
    )

    if st.button("Parse", type="primary"):
        output = parse_sentence(input_text, objects)
        display = parser_output_to_display_dict(output, object_lookup)

        st.markdown("### Interpretation Summary")
        st.info(display["summary"])

        st.markdown("### Anchor Object")
        anchor = display["anchor"]
        if anchor:
            with st.container(border=True):
                cols = st.columns(3)
                cols[0].metric("object_id", anchor["object_id"])
                cols[1].metric("score", f"{anchor['score']:.2f}")
                cols[2].metric("family", anchor["family"])
                st.write(f"**{anchor['korean_label']} / {anchor['label']}**")
                st.caption(anchor["definition"])
        else:
            st.warning("No anchor object detected.")

        st.markdown("### Detected Objects Top 5")
        st.dataframe(pd.DataFrame(display["detected_objects"][:5]), hide_index=True, use_container_width=True)

        st.markdown("### Sensory Axes")
        render_axes(display["axes"])

        st.markdown("### Axis Evidence")
        if not display["axis_evidence_table"].empty:
            st.dataframe(display["axis_evidence_table"], hide_index=True, use_container_width=True)
        else:
            st.caption("No axis-level evidence detected.")

        st.markdown("### Activated Cue Groups")
        if display["activated_cue_groups"]:
            st.dataframe(pd.DataFrame(display["activated_cue_groups"]), hide_index=True, use_container_width=True)
        else:
            st.caption("No cue hierarchy group activated.")

        st.markdown("### Confidence")
        col1, col2 = st.columns(2)
        col1.metric("confidence", f"{display['confidence']:.2f}")
        col2.metric("low_confidence", str(display["low_confidence"]))
        if display["low_confidence"]:
            st.warning("해석 신뢰도가 낮습니다. 사용자 확인 또는 추가 표현이 필요합니다.")

        if display["clarification_questions"]:
            st.markdown("### 더 정확한 해석을 위한 질문")
            for question in display["clarification_questions"]:
                st.info(question)
        else:
            st.caption("현재 입력은 충분히 명확하게 해석되었습니다.")

        with st.expander("Raw parser JSON"):
            st.json(display["raw"])


def render_evaluation_dashboard() -> None:
    st.subheader("Evaluation Dashboard")
    reports = cached_evaluation()
    metric_rows = [
        {
            "dataset": name,
            "total test sentences": report.total,
            "top1 hit rate": report.top1_hit_rate,
            "top3 hit rate": report.top3_hit_rate,
            "low confidence cases": report.low_confidence_count,
        }
        for name, report in reports.items()
    ]
    metrics_df = pd.DataFrame(metric_rows)
    st.dataframe(metrics_df, hide_index=True, use_container_width=True)

    st.markdown("### Top-1 Hit Rate by Dataset")
    st.bar_chart(metrics_df.set_index("dataset")["top1 hit rate"])
    st.markdown("### Top-3 Hit Rate by Dataset")
    st.bar_chart(metrics_df.set_index("dataset")["top3 hit rate"])
    st.markdown("### Low Confidence Cases by Dataset")
    st.bar_chart(metrics_df.set_index("dataset")["low confidence cases"])

    holdout = reports["holdout"]
    st.markdown("### Holdout Failure Analysis")
    cols = st.columns(3)
    cols[0].metric("Top-1 failures", holdout.total - holdout.top1_hits)
    cols[1].metric("Top-3 failures", holdout.total - holdout.top3_hits)
    cols[2].metric("Low confidence", holdout.low_confidence_count)
    error_counts: dict[str, int] = {}
    for row in holdout.rows:
        if row.error_type != "none":
            error_counts[row.error_type] = error_counts.get(row.error_type, 0) + 1
    if error_counts:
        st.dataframe(
            pd.DataFrame(
                [{"error_type": key, "count": value} for key, value in sorted(error_counts.items())]
            ),
            hide_index=True,
            use_container_width=True,
        )

    report_path = PROJECT_ROOT / "outputs" / "eval_report_holdout.md"
    if report_path.exists():
        with st.expander("outputs/eval_report_holdout.md"):
            st.markdown(report_path.read_text(encoding="utf-8"))


def render_ontology_browser(objects) -> None:
    st.subheader("Ontology Browser")
    df = objects_to_dataframe(objects)
    family_options = ["All"] + sorted(df["family"].dropna().unique().tolist())
    type_options = ["All"] + sorted(df["object_type"].dropna().unique().tolist())
    status_options = ["All"] + sorted(str(item) for item in df["status"].dropna().unique().tolist())

    col1, col2, col3 = st.columns(3)
    query = col1.text_input("Search object")
    family = col2.selectbox("Family", family_options)
    object_type = col3.selectbox("Object type", type_options)
    status = st.selectbox("Status", status_options)

    filtered = df.copy()
    if query:
        q = query.casefold()
        mask = (
            filtered["object_id"].str.casefold().str.contains(q, na=False)
            | filtered["label"].str.casefold().str.contains(q, na=False)
            | filtered["korean_label"].str.casefold().str.contains(q, na=False)
            | filtered["definition"].str.casefold().str.contains(q, na=False)
        )
        filtered = filtered[mask]
    if family != "All":
        filtered = filtered[filtered["family"] == family]
    if object_type != "All":
        filtered = filtered[filtered["object_type"] == object_type]
    if status != "All":
        filtered = filtered[filtered["status"].astype(str) == status]

    st.markdown("### Family Counts")
    st.dataframe(df["family"].value_counts().rename_axis("family").reset_index(name="count"), hide_index=True)

    st.markdown("### Objects")
    st.dataframe(filtered[["object_id", "korean_label", "label", "family", "object_type"]], hide_index=True, use_container_width=True)

    if not filtered.empty:
        selected_id = st.selectbox("Select object", filtered["object_id"].tolist())
        selected = next(obj for obj in objects if obj.object_id == selected_id)
        st.markdown("### Object Detail")
        st.write(f"**{selected.korean_label} / {selected.label}**")
        st.caption(selected.definition)
        st.dataframe(
            pd.DataFrame(
                [
                    {"field": "object_id", "value": selected.object_id},
                    {"field": "object_type", "value": selected.object_type},
                    {"field": "family", "value": selected.family},
                    {"field": "confidence", "value": selected.confidence},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        with st.expander("Core axes"):
            st.json(selected.core_axes.model_dump(exclude_none=True))
        st.write("**Example expressions**", selected.example_expressions)
        st.write("**Related objects**", selected.related_objects)
        st.write("**Opposite objects**", selected.opposite_objects)
        st.write("**Evidence refs**", selected.evidence_refs)


def render_candidate_review() -> None:
    st.subheader("Candidate Review")
    st.warning("이 탭은 candidate object 검토용입니다. 여기서 main ontology에 자동 병합하지 않습니다.")

    review = cached_candidate_review()
    rows = review["rows"]
    shortlist = review["shortlist"]
    candidates = review["candidates"]
    existing_objects = review["existing_objects"]
    candidate_lookup = get_candidate_lookup(candidates)
    df = candidate_review_rows_to_dataframe(rows)

    summary = review["summary"]
    metric_keys = [
        "ready_for_curated_merge",
        "needs_more_examples",
        "needs_distinction_review",
        "keep_as_candidate",
        "do_not_merge_yet",
    ]
    metric_cols = st.columns(6)
    metric_cols[0].metric("total candidates", len(rows))
    for col, key in zip(metric_cols[1:], metric_keys, strict=False):
        col.metric(key, summary.get(key, 0))

    st.markdown("### Curated Shortlist for v1.5")
    st.warning("이 shortlist는 v1.5 수동 검토용입니다. 어떤 candidate도 자동으로 main ontology에 병합하지 않습니다.")
    if shortlist:
        shortlist_cols = st.columns(2)
        shortlist_cols[0].metric("selected candidates", len(shortlist))
        shortlist_cols[1].metric("families covered", len(review["shortlist_family_coverage"]))
        st.dataframe(curated_shortlist_to_dataframe(shortlist), hide_index=True, use_container_width=True)
        with st.expander("Family coverage"):
            st.dataframe(
                pd.DataFrame(
                    [
                        {"family_bucket": family, "count": count}
                        for family, count in review["shortlist_family_coverage"].items()
                    ]
                ),
                hide_index=True,
                use_container_width=True,
            )
    else:
        st.info(
            "아직 curated shortlist가 생성되지 않았습니다. CLI에서 `python -m sensory_atlas.cli select-curated-candidates`를 실행해 생성할 수 있습니다."
        )

    all_domains = sorted({domain for row in rows for domain in row.get("source_domains", [])})
    all_actions = sorted({row.get("recommended_action", "") for row in rows})
    all_statuses = sorted({row.get("review_status", "") for row in rows})

    col1, col2, col3 = st.columns(3)
    domain_filter = col1.selectbox("Source domain", ["All"] + all_domains)
    action_filter = col2.selectbox("Recommended action", ["All"] + all_actions)
    status_filter = col3.selectbox("Review status", ["All"] + all_statuses)
    query = st.text_input("Search candidate")

    filtered = df.copy()
    if domain_filter != "All":
        filtered = filtered[filtered["source_domains"].str.contains(domain_filter, na=False)]
    if action_filter != "All":
        filtered = filtered[filtered["recommended_action"] == action_filter]
    if status_filter != "All":
        filtered = filtered[filtered["review_status"] == status_filter]
    if query:
        q = query.casefold()
        mask = (
            filtered["candidate_object_id"].str.casefold().str.contains(q, na=False)
            | filtered["korean_label"].str.casefold().str.contains(q, na=False)
        )
        filtered = filtered[mask]

    st.markdown("### Candidate Table")
    st.dataframe(filtered, hide_index=True, use_container_width=True)

    if filtered.empty:
        st.caption("No candidates match the current filters.")
        return

    selected_id = st.selectbox("Select candidate", filtered["candidate_object_id"].tolist())
    selected = candidate_lookup[selected_id]
    selected_row = next(row for row in rows if row["candidate_object_id"] == selected_id)
    detail = candidate_detail_for_display(selected, existing_objects)

    st.markdown("### Candidate Detail")
    st.write(f"**{selected.get('korean_label')} / {selected.get('label')}**")
    st.caption(selected.get("definition", ""))
    cols = st.columns(4)
    cols[0].metric("recommended_action", selected_row["recommended_action"])
    cols[1].metric("readiness", f"{selected_row['overall_readiness_score']:.2f}")
    cols[2].metric("note risk", f"{selected_row['note_dictionary_risk']:.2f}")
    cols[3].metric("review_status", selected_row["review_status"])

    with st.expander("Core axes", expanded=True):
        st.json(selected.get("core_axes", {}))
    st.write("**Example expressions**", selected.get("example_expressions", []))
    st.write("**Suggested phrase cues**", selected.get("suggested_phrase_cues", []))
    st.write("**Negative cues**", selected.get("negative_cues", []))
    st.write("**Related existing objects**", selected.get("related_existing_objects", []))

    st.markdown("### Similar Existing Objects")
    similar = detail["similar_existing_objects"]
    if similar:
        st.dataframe(pd.DataFrame(similar), hide_index=True, use_container_width=True)
    else:
        st.caption("No similar existing objects found by the rule-based comparison.")

    with st.expander("Promotion draft JSON"):
        st.json(detail["promotion_draft"])


def main() -> None:
    st.set_page_config(page_title="Sensory Atlas", layout="wide")
    st.title("Sensory Atlas")
    st.caption("Translate metaphorical sensory language into structured sensory profiles.")

    objects = cached_objects()
    object_lookup = get_object_lookup(objects)
    parse_tab, eval_tab, ontology_tab, candidate_tab = st.tabs(
        ["Parse Demo", "Evaluation Dashboard", "Ontology Browser", "Candidate Review"]
    )

    with parse_tab:
        render_parse_demo(objects, object_lookup)
    with eval_tab:
        render_evaluation_dashboard()
    with ontology_tab:
        render_ontology_browser(objects)
    with candidate_tab:
        render_candidate_review()


if __name__ == "__main__":
    main()
