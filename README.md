# Sensory Atlas

Sensory Atlas is an MVP for translating metaphorical sensory language into structured sensory profiles.

It is not a flavor-note recommender. The core unit is a **sensory object**: examples include Cashmere, Cut Diamond, Wet Moss, Winter Dawn, Old Library, Film Grain, and 4K Clarity. These objects connect user language to a sensory ontology and, later, to recommendation systems.

## Problem

People often describe taste, scent, texture, and atmosphere indirectly:

> 11월 말 새벽 공기처럼 차갑고 선명한 느낌

Sensory Atlas turns that kind of expression into axes such as temperature, texture, light, motion, time, atmosphere, density, rendering, and organic/mineral character.

## MVP Scope

- Load and validate `data/sensory_objects.jsonl`
- Load 20 test sentences from `data/test_sentences_20.jsonl`
- Parse each sentence with a deterministic rule-based fallback parser
- Save parser output to `outputs/parser_results.jsonl`
- Provide a local CLI with no external API key
- Include pytest coverage for loaders, schema, and parser output

## Project Structure

```text
sensory-atlas/
├── data/
│   ├── sensory_objects.jsonl
│   └── test_sentences_20.jsonl
├── prompts/
│   └── sensory_parser_prompt_v0_1.md
├── outputs/
│   └── parser_results.jsonl
├── src/
│   └── sensory_atlas/
│       ├── __init__.py
│       ├── schema.py
│       ├── loaders.py
│       ├── parser.py
│       ├── matcher.py
│       └── cli.py
├── tests/
│   ├── test_loaders.py
│   ├── test_schema.py
│   └── test_parser.py
├── README.md
├── pyproject.toml
└── .gitignore
```

## Install

```bash
cd /Users/jisoyun/Desktop/sensory-atlas
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Validate Data

```bash
python -m sensory_atlas.cli validate-data
```

## Parser Dry Run

```bash
python -m sensory_atlas.cli dry-run
```

This writes:

```text
outputs/parser_results.jsonl
```

## Evaluate Parser

```bash
python -m sensory_atlas.cli evaluate
python -m sensory_atlas.cli evaluate --dataset blind
python -m sensory_atlas.cli evaluate --dataset holdout
```

This compares parser `detected_objects` with test-set `target_objects`.

```text
outputs/eval_report.md
outputs/eval_report_blind.md
outputs/eval_report_holdout.md
```

## Evaluation Strategy

Sensory Atlas uses staged evaluation sets.

- `default`: ontology sanity check. Sentences are close to the seed vocabulary.
- `blind`: phrase-level generalization test. Direct object names are mostly avoided, but phrase cues are still within the known design space.
- `holdout`: stricter generalization test. Sentences avoid direct object names and try not to reuse phrase cues.

The goal is not to maximize holdout performance by overfitting phrase cues.
The holdout set is used to reveal parser limitations and guide future ontology expansion.

## Example Output

```json
{
  "input_text": "11월 말 새벽 공기처럼 차갑고 투명한 느낌",
  "detected_objects": [
    {
      "object_id": "winter_dawn",
      "score": 0.82
    }
  ],
  "anchor_object": {
    "object_id": "winter_dawn",
    "score": 0.82
  },
  "axes": {
    "temperature": "Cold",
    "texture": ["Clean", "Sharp"],
    "light": ["Transparent", "Crystal Reflection"],
    "motion": ["Rise", "Cut"],
    "time": ["Winter", "Dawn"],
    "rendering": "Precision-first"
  },
  "interpretation_summary": "이 표현은 겨울 새벽 계열의 sensory object와 연결됩니다. 핵심은 Cold 온도감, Clean, Sharp 질감, Transparent 빛으로 해석됩니다.",
  "confidence": 0.78,
  "parser_version": "rule_based_v0.1"
}
```

## Tests

```bash
pytest
```

## Next Steps

- Add calibrated weights per axis and per sensory object family
- Add a candidate-object workflow for expressions that do not match the ontology
- Add an LLM parser behind the same `ParserOutput` contract
- Add evaluation metrics against `expected_axes_minimal`
- Add recommendation readiness scoring once product data exists
