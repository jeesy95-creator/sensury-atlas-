# Candidate Sensory Object Review Workflow v1.4

## 목적

v1.1에서는 domain vocabulary에서 발견된 잠재적 감각 단위를 `candidate sensory object` 레이어에 쌓았습니다. v1.4는 이 후보들이 main ontology로 들어가기 전에 검토할 수 있는 구조화된 workflow를 추가합니다.

이 workflow의 목적은 ontology 품질을 보호하는 것입니다. Sensory Atlas는 향수, 위스키, 와인, 커피 노트를 모아두는 사전이 아니라, 은유적 감각 언어를 구조화된 감각 객체와 축으로 번역하는 sensory language database/parser입니다.

## 왜 바로 병합하지 않는가

모든 note가 sensory object는 아닙니다.

- 어떤 용어는 domain note입니다.
- 어떤 용어는 axis descriptor입니다.
- 어떤 용어는 기존 object와 너무 가깝습니다.
- 어떤 용어는 example expression이나 negative cue가 부족합니다.
- 어떤 용어는 감각적 원형보다 ingredient 이름에 가깝습니다.

따라서 candidate object는 검토 없이 `data/core/sensory_objects.jsonl`에 자동 병합하지 않습니다.

## 승격 기준

candidate가 main sensory object로 승격되려면 다음 기준을 만족해야 합니다.

1. 단순 note가 아니라 감각적 원형을 가진다.
2. 여러 도메인에서 재사용 가능하다.
3. 기존 object와 충분히 구분된다.
4. example expression과 phrase cue가 충분하다.
5. negative cue가 있어야 한다.
6. axis evidence로 설명 가능하다.
7. user feedback이나 dev cases에서 반복적으로 등장한다.

## Readiness Score

readiness score는 review를 돕는 heuristic 지표입니다. 통계적 확률이나 자동 승인 기준이 아닙니다.

- `sensory_archetype_score`: 후보가 단순 note가 아니라 감각적 장면, 표면, 온도감, 질감, 분위기 등을 갖는지 평가합니다.
- `cross_domain_reuse_score`: 여러 도메인에서 재사용 가능한지 평가합니다.
- `distinctiveness_score`: 기존 ontology object와 충분히 구분되는지 평가합니다.
- `example_coverage_score`: example expression이 충분한지 평가합니다.
- `phrase_cue_readiness_score`: suggested phrase cue가 충분한지 평가합니다.
- `negative_cue_readiness_score`: negative cue가 충분한지 평가합니다.
- `note_dictionary_risk`: 후보가 sensory object보다 note dictionary entry에 가까운 위험을 평가합니다.
- `overall_readiness_score`: 위 점수를 종합한 review aid입니다.

## Recommended Actions

- `ready_for_curated_merge`: 수동 검토 후 curated merge 후보로 볼 수 있습니다.
- `needs_more_examples`: 방향은 좋지만 example expression이나 phrase cue가 부족합니다.
- `needs_distinction_review`: 기존 object와 너무 가까워 구분 검토가 필요합니다.
- `keep_as_candidate`: 흥미로운 후보지만 아직 승격하기 이릅니다.
- `keep_as_axis_descriptor`: object보다 axis descriptor나 modifier에 가깝습니다.
- `do_not_merge_yet`: 너무 넓거나 note-like risk가 높아 아직 병합하지 않습니다.

## Streamlit Candidate Review Tab

Streamlit demo에는 read-only Candidate Review tab이 추가됩니다.

이 탭에서는 다음을 확인할 수 있습니다.

- candidate object 목록
- source domain / recommended action / review status 필터
- readiness score와 note dictionary risk
- 기존 object와의 유사 후보
- promotion draft JSON

이 탭은 검토 전용입니다. 여기서 main ontology에 자동 병합하지 않습니다.

## 다음 단계

- v1.5 curated ontology expansion batch
- top candidate 수동 검토
- curated merge PR 생성
- 승격 object의 phrase cue와 regression test 추가
- curated merge 이후에만 evaluation 업데이트
