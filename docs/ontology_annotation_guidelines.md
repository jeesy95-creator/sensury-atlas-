# Sensory Atlas Ontology Annotation Guidelines

## 1. 목적

이 문서는 Sensory Atlas의 sensory object 표현을 일관되게 확장하기 위한 기준이다. 목표는 사용자의 은유적 감각 언어를 단순 tasting note가 아니라 구조화된 감각 객체와 감각 축으로 번역할 수 있도록 데이터 밀도를 높이는 것이다.

## 2. Sensory Object 작성 원칙

- 하나의 object는 하나의 감각적 원형을 나타낸다.
- object는 향료명이나 재료명이 아니라 사용자의 감각 언어 단위다.
- material, temperature, texture, light, motion, time, atmosphere, density, rendering, organic_mineral 축을 함께 고려한다.
- object 이름을 직접 말하지 않은 표현에서도 같은 감각 원형이 떠오르는지 확인한다.
- 비슷한 object와 구분되는 핵심 단서를 definition, example_expressions, phrase_cues에 나누어 기록한다.

## 3. example_expressions 작성 규칙

example_expressions는 parser가 object의 언어적 주변부를 배울 수 있게 하는 표현 모음이다. 한 object당 최소 8개 이상을 권장한다.

- 직접 표현: object 이름이나 가까운 명칭을 포함한다.
- 은유 표현: object 이름 없이 장면, 질감, 온도, 분위기로 우회한다.
- 분위기 표현: 공간, 시간, 빛, 움직임을 함께 적는다.
- 구분 표현: 비슷한 object와 헷갈리지 않도록 반대 개념을 포함한다.
- 반복 금지: 같은 문장을 조사만 바꾸어 늘리지 않는다.

예시:

- 직접 표현: `젖은 이끼 같은 향`
- 은유 표현: `비 온 뒤 숲 바닥에 남은 초록빛 습기`
- 질감/온도 표현: `차갑고 축축하지만 부드럽게 깔리는 느낌`
- 구분 표현: `달콤하기보다는 축축하고 초록빛에 가까운 향`

## 4. phrase_cues 작성 규칙

phrase_cues는 object를 강하게 활성화하는 phrase-level 단서다.

- 직접 명칭뿐 아니라 우회 표현을 포함한다.
- 단일 단어보다 2-5어절의 구체적 phrase를 우선한다.
- 너무 범용적인 단어는 단독 cue로 쓰지 않는다. 예를 들어 `차가운`, `부드러운`, `어두운`만 단독 cue로 쓰면 오탐이 늘어난다.
- object family를 구분해야 하는 경우 negative_cues를 적극적으로 사용한다.
- holdout 문장을 그대로 cue로 복사하지 않는다.
- phrase cue는 성능 점수를 억지로 올리는 수단이 아니라 ontology coverage를 넓히는 annotation이다.

## 5. 비슷한 Object 구분 기준

### sea_breeze vs mountain_stream

| Object | 핵심 단서 | 피해야 할 혼동 |
| --- | --- | --- |
| `sea_breeze` | 넓게 퍼지는 해안 공기, 소금기, 바다, 바람 | 계곡, 바위틈, 좁은 물길 |
| `mountain_stream` | 좁고 차갑게 흐르는 물길, 계곡, 바위, 미네랄 | 소금기, 해안, 수평으로 퍼지는 공기 |

### rain_on_asphalt vs after_rain_garden

| Object | 핵심 단서 | 피해야 할 혼동 |
| --- | --- | --- |
| `rain_on_asphalt` | 도시, 도로, 먼지, 포장도로, 빗물 | 잎, 정원, 흙, 식물성 습기 |
| `after_rain_garden` | 정원, 흙, 식물, 잎, 초록빛 습기 | 아스팔트, 보도블록, 도시 바닥 |

### leather vs suede

| Object | 핵심 단서 | 피해야 할 혼동 |
| --- | --- | --- |
| `leather` | 묵직함, 드라이함, 동물성, 오래된 가죽 | 보송한 털감, 가루 같은 표면 |
| `suede` | 보송함, 매트함, 짧은 털감, 부드러운 표면 | 매끈하고 묵직한 오래된 가죽 |

### film_grain vs four_k_clarity

| Object | 핵심 단서 | 피해야 할 혼동 |
| --- | --- | --- |
| `film_grain` | 낮은 해상도처럼 보이지만 분위기, 잔상, 노이즈, 감성적 렌더링 | 정밀한 초점, 고해상도, 차가운 디테일 |
| `four_k_clarity` | 선명도, 고해상도, 입자까지 보임, 차갑고 정밀함 | 흐릿함, 노스텔지어, 분위기 중심 렌더링 |

### slate vs granite vs wet_stone

| Object | 핵심 단서 | 피해야 할 혼동 |
| --- | --- | --- |
| `slate` | 납작하고 어두운 돌, 차분함, 매트함 | 큰 입자감, 젖은 표면 |
| `granite` | 입자가 보이는 단단한 돌, 거칠고 견고함 | 얇고 평평한 돌판, 물기 어린 돌 |
| `wet_stone` | 물기 어린 차가운 돌, 젖은 표면, 축축한 미네랄 | 건조한 석판, 거친 화강암 입자 |

## 6. 데이터 확장 시 주의점

- holdout 문장을 그대로 cue로 복사하지 않는다.
- 성능 점수를 올리기 위한 과적합을 피한다.
- 새로운 표현은 object의 core_axes와 충돌하지 않아야 한다.
- 비슷한 object가 함께 활성화될 수 있더라도 anchor object가 무엇인지 설명 가능해야 한다.
- 표현을 추가하면 ontology coverage test와 regression test를 함께 확인한다.
