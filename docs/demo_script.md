# Demo Script

## 30-second pitch

Sensory Atlas는 사용자의 은유적 감각 언어를 구조화된 sensory profile로 번역하는 parser입니다. 일반적인 flavor recommender처럼 `smoke`, `vanilla`, `oak` 같은 note만 다루는 것이 아니라, “11월 말 새벽 공기”, “캐시미어 니트”, “해상도는 낮지만 분위기만 남아” 같은 표현을 sensory object와 axes로 변환합니다.

## 2-minute walkthrough

1. Streamlit 앱을 열고 Parse Demo 탭을 보여줍니다.
2. `해상도는 낮지만 분위기만 남아`를 입력합니다.
3. anchor object가 `film_grain`으로 잡히고, rendering이 `Film-like`로 나오는 점을 설명합니다.
4. Activated Cue Groups에서 `film_like_rendering`이 활성화된 것을 보여줍니다.
5. Evaluation Dashboard로 이동해 default/blind/holdout 평가를 설명합니다.
6. Ontology Browser에서 `film_grain`을 검색하고 core axes를 보여줍니다.

## Demo inputs

```text
해상도는 낮지만 분위기만 남아
차가운 큰 홀의 매끈한 바닥처럼 고요하고 윤이 나
바위틈 사이로 차가운 물줄기가 흐르는 듯한 향
11월 말 새벽 공기처럼 코가 쨍하게 시리고 투명한 느낌
```

## What to point out

- Parser output이 단순 label이 아니라 anchor, detected objects, axes, cue groups를 함께 보여준다는 점
- cue hierarchy가 surface keyword와 context meaning의 충돌을 줄인다는 점
- holdout 성능이 낮은 부분을 숨기지 않고 failure taxonomy로 보여준다는 점

## Possible interview questions and answers

### Q. 왜 LLM API를 쓰지 않고 rule-based parser로 시작했나요?

A. 문제를 먼저 구조화하기 위해서입니다. 어떤 sensory object와 axis가 필요한지, 어떤 cue에서 실패하는지 알기 전에는 LLM을 붙여도 해석 기준이 흐려질 수 있습니다. rule-based baseline은 재현 가능하고 실패 분석이 명확합니다.

### Q. Top-1이 높은데 overfitting은 아닌가요?

A. default와 blind는 의도적으로 sanity/generalization check에 가깝습니다. 그래서 holdout을 별도로 만들었습니다. holdout은 더 어렵게 유지했고, 현재 Top-1은 0.64입니다. 이 숫자가 parser 한계를 더 잘 보여줍니다.

### Q. holdout 성능이 낮은 이유는 무엇인가요?

A. holdout은 direct object name과 known phrase cues를 최대한 피합니다. 그래서 cue hierarchy 밖의 은유, 너무 넓은 atmosphere 표현, time/season cue가 약한 표현에서 실패가 발생합니다.

### Q. 이 프로젝트가 일반 추천기와 다른 점은 무엇인가요?

A. 추천 이전 단계의 semantic translation layer입니다. 사용자 언어를 바로 제품으로 매핑하지 않고, sensory object와 axes로 먼저 구조화합니다.

### Q. 다음 단계는 무엇인가요?

A. low-confidence case에 대해 사용자 확인 질문을 만들고, axis-level confidence를 추가한 뒤, sensory profile 기반 recommendation interface로 확장하는 것입니다.
