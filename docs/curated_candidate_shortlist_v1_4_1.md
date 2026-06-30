# Curated Candidate Shortlist v1.4.1

## 목적

v1.4에서는 candidate sensory object review workflow를 만들고, 47개 후보에 대해 readiness score와 recommended action을 계산했습니다.

v1.4.1은 그중 `ready_for_curated_merge`로 분류된 후보에서 작은 curated batch를 선별하는 단계입니다. 이 shortlist는 v1.5 ontology expansion을 위한 수동 검토 대상이며, 어떤 candidate도 자동으로 main ontology에 병합하지 않습니다.

## 왜 17개를 모두 승격하지 않는가

Sensory Atlas에서는 object 수보다 ontology 품질이 더 중요합니다. 준비된 후보를 한 번에 많이 추가하면 프로젝트가 감각 언어 구조화 시스템이 아니라 generic note dictionary처럼 보일 위험이 있습니다.

첫 번째 curated batch는 여러 도메인에서 재사용 가능한 sensory archetype을 우선해야 합니다. 또한 clean/skin, powder/softness, smoke/resin, wet/earth, mineral/glass, warm/density, finish/dryness처럼 family diversity도 고려해야 합니다.

## 선정 기준

- sensory archetype strength
- cross-domain reuse
- distinctiveness from existing objects
- example/phrase cue coverage
- negative cue availability
- low note dictionary risk
- family diversity

## 제외 기준

- too note-like
- too close to existing object
- too domain-specific
- weak metaphorical sensory structure
- insufficient cues/examples
- lower priority for batch 1

## 산출물

- `data/workflow/curated_candidate_shortlist_v1_5.jsonl`
- `outputs/curated_candidate_shortlist_report.md`
- `outputs/curated_candidate_shortlist_summary.json`

이 산출물은 v1.5 수동 ontology expansion을 위한 검토 자료입니다.

## 다음 단계

v1.5에서는 shortlist에 포함된 candidate만 수동으로 검토합니다.

- selected candidate를 하나씩 main ontology에 추가할지 판단
- 승격하는 object에 phrase cue 추가
- negative cue와 regression case 추가
- holdout dataset은 잠근 상태로 유지
- 승격 후 default / blind / holdout evaluation을 분리 확인
