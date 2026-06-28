# v1.0 Data Coverage Report

## Summary

v1.0 expands Sensory Atlas ontology coverage without changing parser, matcher, or cue hierarchy logic. The goal was to give the existing rule-based parser richer sensory language around each sensory object.

## What Changed

- Expanded `example_expressions` for all 50 sensory objects.
- Added or enriched phrase cues for 20 priority weak/missing objects.
- Added `data/dev_failure_cases.jsonl` with 20 new development cases for future parser iteration.
- Added ontology annotation guidelines in Korean.
- Added ontology coverage tests.

## Coverage Metrics

| Metric | Before | After |
| --- | ---: | ---: |
| Sensory objects | 50 | 50 |
| Objects with updated examples | 0 | 50 |
| Minimum examples per object | 3 | 9 |
| Average examples per object | 3.1 | 9.1 |
| Maximum examples per object | 8 | 14 |
| Phrase cue entries | 30 | 44 |
| Priority objects present in phrase cues | 6 / 20 | 20 / 20 |
| Priority objects with at least 8 positive cues | 0 / 20 | 20 / 20 |

## Priority Phrase Cue Objects Covered

- `bark`
- `sea_breeze`
- `rain_on_asphalt`
- `rainy_street`
- `leather`
- `suede`
- `black_tea`
- `tobacco_leaf`
- `cedarwood`
- `green_stem`
- `dry_herb`
- `slate`
- `silver_spoon`
- `fresh_linen`
- `clean_room`
- `late_night_air`
- `barrel_cellar`
- `charred_oak`
- `forest_floor`
- `wet_stone`

## Evaluation Results

| Dataset | Total | Top-1 | Top-3 | Low Confidence |
| --- | ---: | ---: | ---: | ---: |
| default | 20 | 1.00 | 1.00 | 0 |
| blind | 30 | 1.00 | 1.00 | 0 |
| holdout | 50 | 0.78 | 0.88 | 6 |

## Holdout Notes

The holdout set was not modified. The improvement appears to come from broader phrase-level coverage and richer example expressions, especially for scene/material objects that previously had sparse language around them.

Compared with the previous documented v0.9 baseline:

| Dataset | Previous Top-1 | v1.0 Top-1 | Previous Top-3 | v1.0 Top-3 | Previous Low Confidence | v1.0 Low Confidence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| default | 1.00 | 1.00 | 1.00 | 1.00 | 0 | 0 |
| blind | 1.00 | 1.00 | 1.00 | 1.00 | 1 | 0 |
| holdout | 0.64 | 0.78 | 0.78 | 0.88 | 12 | 6 |

## Validation

```text
pytest
31 passed

python -m sensory_atlas.cli validate-data
Validated 50 sensory objects
```

## Remaining Limitations

- Phrase cues are still hand-authored and may encode annotator bias.
- Negative cues are documented in data but not yet used directly by the matcher.
- Dev failure cases are not an accuracy gate yet; they are intentionally reserved for future iteration.
- Some object boundaries remain subtle, especially between rainy urban scenes and wet mineral scenes.

## Next Step

Use `data/dev_failure_cases.jsonl` as a development set for v1.1. The next parser iteration can consume negative cues and cue family context more explicitly without touching the locked holdout set.
