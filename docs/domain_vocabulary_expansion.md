# Domain Vocabulary Expansion v1.1

## 목적

이 문서는 Sensory Atlas의 초기 handcrafted ontology를 향수, 위스키, 와인, 커피, cross-domain tasting language로 확장하기 위한 후보 vocabulary layer를 설명한다.

v1.1의 목표는 domain vocabulary를 곧바로 parser나 main ontology에 병합하는 것이 아니다. 일반적인 note, accord, tasting descriptor를 Sensory Atlas식으로 다시 구조화하여 다음 항목으로 나누어 보관한다.

- 기존 sensory object와 연결 가능한 term
- 향후 검토할 candidate sensory object
- object가 아니라 axis에 영향을 주는 descriptor
- 아직 통합하지 말아야 할 넓거나 모호한 vocabulary

## 왜 바로 ontology에 병합하지 않는가

Sensory Atlas는 generic note dictionary가 아니다. 모든 note가 sensory object가 되면 ontology가 빠르게 지저분해지고, parser는 단어 사전처럼 작동하게 된다.

예를 들어 `rose`, `bergamot`, `tannin`, `powdery`, `clean finish`는 모두 유용한 감각 vocabulary지만 성격이 다르다.

- 어떤 term은 특정 domain note다.
- 어떤 term은 sensory axis descriptor다.
- 어떤 term은 독립 sensory object 후보가 될 수 있다.
- 어떤 term은 너무 넓어서 아직 통합하면 안 된다.

따라서 v1.1은 review-before-merge layer로 설계했다. 후보를 모으고, 기존 object와 연결하고, axes와 cue 후보를 정리한 뒤, 검토를 거쳐 일부만 main ontology에 병합한다.

## 데이터 구조

### `data/domain_vocabulary_seed.csv`

향수, 위스키, 와인, 커피, cross-domain vocabulary를 모은 seed table이다.

주요 필드:

- `domain`: vocabulary가 주로 쓰이는 domain
- `vocabulary_type`: note, accord, tasting_descriptor, family, texture_descriptor, atmosphere_descriptor
- `term`: 영어 vocabulary
- `korean_label`: 한국어 label
- `sensory_family`: 감각 family
- `mapped_existing_objects`: 이미 존재하는 Sensory Atlas object
- `candidate_object_id`: 후보 object id
- `core_axes`: 후보 축 정보
- `suggested_phrase_cues`: 향후 phrase cue 후보
- `negative_cues`: 혼동 방지 cue
- `integration_status`: 통합 상태
- `notes`: annotation note

### `data/sensory_object_candidates.jsonl`

main ontology에 아직 병합하지 않은 candidate sensory object 모음이다.

각 candidate는 다음 정보를 가진다.

- `candidate_object_id`
- `label`
- `korean_label`
- `source_domains`
- `family`
- `definition`
- `core_axes`
- `example_expressions`
- `suggested_phrase_cues`
- `negative_cues`
- `related_existing_objects`
- `integration_recommendation`

### `data/domain_mapping.json`

domain vocabulary를 Sensory Atlas 개념으로 연결하는 mapping layer다.

이 파일은 domain별 family와 cross-domain mapping을 포함한다. 예를 들어 `smoky`는 기존 object인 `fireplace_ash`, `charred_oak`, `tobacco_leaf`와 연결되고, 후보 object인 `peat_smoke`, `incense_smoke`와도 연결된다.

## Note / Accord / Tasting Vocabulary를 Sensory Atlas식으로 바꾸는 방식

v1.1은 domain term을 그대로 object로 만들지 않고, 그 term이 환기하는 감각 구조를 분리한다.

```text
bergamot → bergamot_brightness
musk → white_musk_clean_skin / skin_musk_warmth
peat smoke → peat_smoke
powdery → powder_cloud / cosmetic_powder
aquatic → aquatic_clean_water / sea_breeze
tannin → wine_tannin_grip / oak_tannin_dryness
```

이 변환은 다음 질문을 기준으로 한다.

- 이 단어는 특정 재료명인가, 감각 장면인가?
- 기존 sensory object로 충분히 설명되는가?
- 새로운 object로 분리할 만큼 독립적인 감각 원형이 있는가?
- 어떤 axes가 핵심인가?
- 어떤 phrase cue가 object를 활성화할 수 있는가?
- 어떤 negative cue가 오탐을 줄일 수 있는가?

## 기존 Sensory Object와 Candidate Object의 차이

| 구분 | 의미 | 예시 |
| --- | --- | --- |
| existing object | parser가 이미 사용하는 main ontology object | `citrus_peel`, `wet_stone`, `black_tea` |
| candidate object | 검토 후 ontology에 병합할 수 있는 후보 | `bergamot_brightness`, `peat_smoke`, `wine_tannin_grip` |
| axis descriptor | object가 아니라 texture, density, motion 같은 축에 영향을 주는 표현 | `sharp`, `soft`, `body`, `finish` |
| do_not_integrate_yet | 유용하지만 너무 넓거나 모호해 보류할 표현 | 넓은 family term, domain-specific ambiguity |

## 저작권 / 데이터 사용 원칙

- 리뷰 문장이나 proprietary text를 복사하지 않는다.
- 공개적으로 널리 쓰이는 vocabulary concept만 참고한다.
- 한국어 example expression은 원문 없이 새로 작성한다.
- 이 레이어는 scraped dataset이 아니라 curated vocabulary layer다.
- 특정 제품 리뷰, 브랜드 문구, 유료 데이터베이스의 문장을 그대로 가져오지 않는다.

## 다음 단계

- candidate object를 수동 검토한다.
- 일부 candidate를 `data/sensory_objects.jsonl`에 병합한다.
- 병합된 candidate에 대해 `phrase_cues.json`을 추가한다.
- fragrance / whisky mapping을 보여주는 domain-specific demo mode를 만든다.
- Streamlit에 domain vocabulary browser를 추가한다.
- 이후 embedding fallback 또는 LLM-assisted parser를 같은 schema 뒤에 연결한다.
