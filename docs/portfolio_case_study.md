# Sensory Atlas — Portfolio Case Study

## Background

Sensory Atlas는 사용자의 은유적 감각 언어를 구조화된 sensory profile로 번역하는 프로젝트입니다. 향, 맛, 질감, 장면, 기억처럼 말로 고정하기 어려운 감각 표현을 `sensory object`와 `sensory axes`로 변환하는 semantic translation layer를 목표로 합니다.

## Problem

일반적인 추천 시스템은 제품 중심 descriptor에 의존하는 경우가 많습니다. 예를 들어 whisky나 perfume 추천에서는 `smoke`, `vanilla`, `oak`, `floral`, `fruity` 같은 tasting note가 자주 사용됩니다.

하지만 실제 사용자는 감각을 더 은유적으로 표현합니다.

```text
11월 말 새벽 공기처럼 차갑고 투명한 느낌
캐시미어 니트처럼 포근하게 감싸는 향
해상도는 낮지만 분위기만 남아 있는 오래된 영화 같은 향
```

Sensory Atlas의 문제의식은 이 표현들을 단순 감성 문장이 아니라 구조화 가능한 감각 신호로 보는 것입니다.

## Approach

처음부터 LLM API나 추천 모델을 붙이지 않고, rule-based parser와 명시적인 ontology를 먼저 만들었습니다.

- 어떤 감각 축이 필요한지 직접 관찰하기 위해
- parser 실패 케이스를 명확하게 분석하기 위해
- 추천 이전에 semantic translation layer를 독립적으로 검증하기 위해
- 작은 데이터셋에서도 재현 가능한 baseline을 만들기 위해

## Data Design

데이터는 세 단계 평가셋으로 나뉩니다.

- `default`: ontology vocabulary와 가까운 sanity check
- `blind`: object name을 피한 phrase-level generalization
- `holdout`: phrase cue와 직접 object name을 최대한 피한 stricter metaphor generalization

이 구조 덕분에 높은 정확도 하나만 보는 대신, parser가 어떤 표현에서 실패하는지 확인할 수 있습니다.

## Ontology Design

Sensory Atlas의 기본 단위는 `sensory object`입니다. 각 object는 material, temperature, texture, light, motion, time, atmosphere, density, rendering, organic/mineral 같은 축을 가집니다.

## Parser Design

```text
input text
→ label / example expression matching
→ cue hierarchy activation
→ phrase cue matching
→ object ranking
→ anchor object selection
→ axes merge
→ parser output
```

Parser output은 `anchor_object`, `detected_objects`, `activated_cue_groups`, `axes`, `confidence`, `low_confidence`를 포함합니다.

## Cue Hierarchy

v0.7에서 cue hierarchy를 추가했습니다. 이 레이어는 surface keyword와 문맥 의미가 충돌할 때 중요합니다.

```text
해상도는 낮지만 분위기만 남아
→ film_like_rendering
→ film_grain
```

## Evaluation

| Dataset | Purpose | Total | Top-1 | Top-3 | Low Confidence |
| --- | --- | ---: | ---: | ---: | ---: |
| default | Ontology sanity check | 20 | 1.00 | 1.00 | 0 |
| blind | Phrase-level generalization | 30 | 1.00 | 1.00 | 1 |
| holdout | Stricter metaphor generalization | 50 | 0.64 | 0.78 | 12 |

Holdout은 일부러 어렵게 유지했습니다. 목적은 성능을 부풀리는 것이 아니라 실패 유형을 드러내는 것입니다.

## Results

- rule-based parser로도 metaphorical sensory language를 구조화할 수 있음을 확인
- cue hierarchy가 film-like vs 4K-like 충돌을 줄임
- `marble_hall_polish`, `mountain_water_flow` 같은 abstract cue group이 zero-match를 완화
- Streamlit demo로 비개발자도 parser와 ontology를 탐색 가능

## What I Learned

- 감각 표현은 단일 descriptor보다 object와 axis의 조합으로 다루는 것이 더 풍부합니다.
- 높은 정확도보다 staged evaluation과 failure taxonomy가 더 많은 정보를 줍니다.
- rule-based baseline은 LLM/embedding으로 넘어가기 전 좋은 설계 도구가 됩니다.
- holdout 성능을 일부러 어렵게 유지하는 것이 과적합을 피하는 데 도움이 됩니다.

## Limitations

- 현재 parser는 rule-based입니다.
- 새로운 은유가 cue hierarchy 밖에 있으면 low-confidence가 발생합니다.
- product recommendation logic은 아직 없습니다.
- axis별 evidence와 confidence는 아직 세분화되지 않았습니다.

## Next Steps

- axis-level confidence 추가
- low-confidence case에 대한 사용자 확인 질문 생성
- candidate sensory object workflow 추가
- LLM-assisted parser를 같은 schema 뒤에 추가
- sensory profile 기반 recommendation interface 설계
