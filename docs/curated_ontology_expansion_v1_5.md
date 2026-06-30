# Curated Ontology Expansion Batch 1 v1.5

## 목적

v1.5는 Sensory Atlas의 첫 번째 실제 main ontology expansion입니다. v1.4 candidate review workflow와 v1.4.1 curated shortlist를 거쳐, 후보 중 일부만 `data/core/sensory_objects.jsonl`에 승격했습니다.

이 작업은 candidate를 자동 병합하는 단계가 아닙니다. 은유적 감각 언어를 안정적으로 구조화할 수 있는 reusable sensory archetype만 선별해 main ontology에 추가합니다.

## 왜 일부만 승격했는가

ontology 품질은 object 개수보다 중요합니다. 준비된 후보를 모두 넣으면 Sensory Atlas가 감각 언어 parser가 아니라 generic note dictionary처럼 보일 위험이 있습니다.

이번 batch에서는 12개 shortlist 중 8개만 승격했습니다. 나머지는 note-like risk, descriptor-like risk, 기존 object와의 구분 문제, cross-domain example 부족 때문에 보류했습니다.

## 승격 기준

- sensory archetype strength
- cross-domain reuse
- distinctiveness from existing objects
- 충분한 example expression
- phrase cue와 negative cue availability
- axis evidence explainability
- low note dictionary risk

## 승격된 object

### green_leaf_crush

- Korean label: 으깬 초록 잎
- Sensory role: 손으로 잎을 으깼을 때의 아삭하고 풋풋한 초록 수분감
- Why promoted: green note가 아니라 잎의 파열감, 수분감, 섬유질을 가진 reusable sensory archetype
- Related objects: green_stem, wet_moss, after_rain_garden
- Confusion risk: green_stem, wet_moss

### wet_soil

- Korean label: 비 맞은 흙
- Sensory role: 비가 스며든 흙의 낮고 축축한 대지감
- Why promoted: forest_floor나 wet_stone과 다르게 흙 자체의 낮은 습도와 밀도를 표현
- Related objects: forest_floor, wet_moss, after_rain_garden, wet_stone
- Confusion risk: forest_floor, rain_on_asphalt

### astringent_dryness

- Korean label: 수렴성 드라이함
- Sensory role: 혀와 입안을 조이는 떫고 건조한 피니시
- Why promoted: 향/맛/질감 전반에서 반복되는 texture archetype
- Related objects: black_tea, dry_herb, charred_oak
- Confusion risk: dry_herb, black_tea

### amber_glow

- Korean label: 앰버의 금빛 잔향
- Sensory role: 따뜻한 수지와 금빛 잔향이 결합된 부드러운 밀도
- Why promoted: 단순 amber note가 아니라 warm resinous glow archetype으로 재사용 가능
- Related objects: honeycomb, vanilla_cream, pine_resin
- Confusion risk: honeycomb, vanilla_cream

### dark_resin

- Korean label: 어두운 수지감
- Sensory role: 어둡고 낮게 깔리는 수지성 단맛과 흙빛 깊이
- Why promoted: pine_resin보다 어둡고 tobacco_leaf보다 끈적한 atmosphere-first resin object
- Related objects: tobacco_leaf, forest_floor, charred_oak, pine_resin
- Confusion risk: tobacco_leaf, charred_oak

### lactonic_milk_softness

- Korean label: 우유빛 둥근 부드러움
- Sensory role: 우유처럼 하얗고 둥근 부드러운 질감
- Why promoted: vanilla_cream과 warm_cotton 사이의 lactonic softness archetype
- Related objects: vanilla_cream, warm_cotton, cashmere
- Confusion risk: vanilla_cream, warm_cotton

### tea_like_clarity

- Korean label: 차처럼 맑고 건조한 투명감
- Sensory role: 찻물처럼 맑고 건조하며 약하게 쌉싸름한 투명감
- Why promoted: beverage note를 넘어 dry clarity / clean bitterness를 설명하는 archetype
- Related objects: black_tea, dry_herb, fresh_linen
- Confusion risk: black_tea, dry_herb

### golden_density

- Korean label: 금빛의 달콤한 밀도
- Sensory role: 금빛으로 두껍게 남는 따뜻한 단맛과 무게감
- Why promoted: honeycomb, burnt_sugar, vanilla_cream과 구분되는 density-first sweet glow
- Related objects: honeycomb, burnt_sugar, vanilla_cream
- Confusion risk: honeycomb, burnt_sugar

## 보류된 object

- `fig_leaf_green`: 무화과/과실 note처럼 보일 수 있어 green_stem과의 구분 검토 필요
- `stone_fruit_glow`: stone fruit note family로 읽힐 위험이 있어 future batch로 보류
- `iodine_coast`: coastal/medicinal context에 치우쳐 더 많은 cross-domain example 필요
- `syrupy_body`: sensory object보다 density/texture descriptor에 가까울 수 있어 보류

## 데이터 변경

- `data/core/sensory_objects.jsonl`: 8개 curated object 추가
- `data/core/phrase_cues.json`: 승격 object별 positive/negative cue 추가
- `data/workflow/candidate_review_status.jsonl`: 승격 object는 `merged`, 보류 object는 `defer_to_future_batch`로 갱신
- `data/regression/ontology_expansion_v1_5_cases.jsonl`: v1.5 regression/dev case 추가

## 평가 결과

- default: Top-1 1.00 / Top-3 1.00
- blind: Top-1 1.00 / Top-3 1.00
- holdout: Top-1 0.78 / Top-3 0.88 / low-confidence 6

평가 데이터셋과 holdout은 수정하지 않았습니다.

## 한계

- parser는 여전히 rule-based입니다.
- 새 object는 기존 object와 경쟁할 수 있습니다.
- 일부 object는 더 많은 negative cue가 필요할 수 있습니다.
- v1.5 cases는 dev/regression data이며 unbiased holdout이 아닙니다.

## 다음 단계

- v1.6에서 필요 시 promoted object parser integration 점검
- 사용자 feedback case 수집
- 두 번째 ontology expansion batch 검토
- ontology가 안정된 뒤 embedding fallback 또는 LLM-assisted parser 실험
