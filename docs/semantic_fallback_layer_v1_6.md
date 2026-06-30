# Semantic Fallback Layer v1.6

## 목적

v1.6은 rule-based parser를 대체하지 않고, 낮은 확신 또는 모호한 은유 표현에 대해 보조적인 semantic fallback suggestion을 제공하는 레이어입니다.

기존 parser는 명확한 phrase cue, cue hierarchy, object-level evidence가 있는 표현에서 잘 작동합니다. 하지만 처음 보는 은유나 문장 전체 분위기에서 의미가 생기는 표현은 표면 cue만으로 충분히 해석하기 어렵습니다.

Semantic fallback은 이런 경우 main ontology와 candidate object corpus에서 의미적으로 가까운 후보를 검색해 참고용으로 보여줍니다.

## 왜 필요한가

예를 들어 다음 표현은 표면 단서만으로는 하나의 object를 확정하기 어렵습니다.

```text
새벽 기차역 플랫폼 끝에서 피우는 담배 한 모금 같은 향
```

이 문장에는 시간, 장소, 차가운 공기, 도시적 분위기, 담배 잔향이 함께 들어 있습니다. 단일 keyword보다 문장 전체의 atmosphere가 중요합니다.

Semantic fallback은 이런 표현에서 `late_night_air`, `tobacco_leaf`, `rainy_street` 같은 주변 후보를 보조적으로 검색할 수 있습니다.

## Rule-based Parser와 Semantic Fallback의 역할 분리

- Rule-based parser는 primary parser입니다.
- Anchor object, detected objects, axes merge, axis evidence, confidence는 기존 rule-based 결과를 유지합니다.
- Semantic fallback은 secondary suggestion입니다.
- Semantic similarity는 parser confidence와 다릅니다.
- Semantic fallback은 anchor object를 대체하지 않습니다.
- Semantic match가 있다고 해서 main ontology object가 자동 승격되거나 정답이 되는 것은 아닙니다.

## 사용 데이터

Semantic fallback corpus는 다음 데이터를 사용합니다.

- main sensory objects: `data/core/sensory_objects.jsonl`
- phrase cues: `data/core/phrase_cues.json`
- candidate sensory objects: `data/workflow/sensory_object_candidates.jsonl`
- object label, korean label, definition, family, object role
- core axes
- example expressions
- suggested phrase cues
- related objects

main ontology object는 high-trust source로 표시됩니다. candidate object는 lower-trust suggestion으로만 검색되며, 자동 병합되지 않습니다.

## Backend

v1.6의 기본 backend는 deterministic TF-IDF character n-gram similarity입니다.

```python
TfidfVectorizer(
    analyzer="char_wb",
    ngram_range=(2, 5),
    min_df=1,
)
```

이 방식은 deep embedding model은 아니지만 다음 장점이 있습니다.

- 외부 유료 API가 필요 없습니다.
- 로컬과 Streamlit Cloud에서 재현 가능합니다.
- 테스트하기 쉽습니다.
- 한국어 표현의 부분 문자열과 어절 변형에 비교적 강합니다.

향후 sentence-transformer backend나 LLM-assisted backend를 추가할 수 있도록 semantic fallback은 별도 모듈로 분리되어 있습니다.

## Evaluation

기존 `evaluate --dataset ...` 명령은 rule-based parser 성능만 측정합니다. v1.6은 fallback 평가를 별도 명령으로 분리합니다.

```bash
python -m sensory_atlas.cli evaluate-fallback --dataset holdout
```

fallback evaluation은 다음 지표를 따로 보고합니다.

- `rule_top1`
- `rule_top3`
- `fallback_assist_top1`
- `fallback_assist_top3`
- `fallback_used_count`
- `fallback_helped_count`
- `fallback_hurt_count`
- `low_confidence_count`

이 지표는 fallback이 rule-based parser를 대체한다는 뜻이 아닙니다. 낮은 확신 상황에서 어떤 후보를 보조적으로 제안할 수 있는지 보기 위한 분석입니다.

## 한계

- TF-IDF는 깊은 은유 이해 모델이 아닙니다.
- ontology와 example expression이 빈약하면 검색 품질도 제한됩니다.
- 어휘적으로 비슷하지만 감각적으로 약한 match가 나올 수 있습니다.
- candidate object는 lower-trust source이므로 해석 결과가 아니라 참고 후보입니다.

## 다음 단계

- sentence-transformer backend 실험
- 사용자 feedback case 수집
- semantic match와 rule-based evidence를 분리한 hybrid ranking 실험
- clarification response 저장
- 실제 annotation study 기반 fallback quality 평가
