# Data Inventory

Current as of ontology v1.5. Authoritative source: `data/data_manifest.json`.

## data/core — Parser Runtime

Files read directly by the parser on every inference call. Changes here affect production behavior immediately.

| File | Format | Records | Purpose |
| --- | --- | ---: | --- |
| `sensory_objects.jsonl` | JSONL | 58 | Primary ontology — sensory objects with object_role and core_axes |
| `phrase_cues.json` | JSON | 58 | Phrase-level cue boosts per object |
| `cue_hierarchy.json` | JSON | 8 groups | Contextual cue groups for keyword/context conflict resolution |

**Constraint:** Every object in `sensory_objects.jsonl` must have a corresponding entry in `phrase_cues.json`.

## data/evaluation — Parser Evaluation

Read by `python -m sensory_atlas.cli evaluate` and the Streamlit Evaluation Dashboard. Do not modify holdout set to chase performance.

| File | Records | Purpose |
| --- | ---: | --- |
| `test_sentences_20.jsonl` | 20 | default — ontology sanity check |
| `blind_test_sentences_30.jsonl` | 30 | blind — phrase-level generalization |
| `holdout_test_sentences_50.jsonl` | 50 | holdout — stricter metaphor generalization |

**Current results:** default 1.00 / blind 1.00 / holdout Top-1 0.78 Top-3 0.88

## data/vocabulary — Reference Vocabulary

Not read by parser at inference time. Used for ontology design, phrase cue expansion, and future embedding work.

| File | Purpose |
| --- | --- |
| `sensory_axis_descriptors.json` | Extended axis vocabulary (17 axes). See `axis_mapping.json` for mapping to 10 parser canonical axes. |
| `axis_mapping.json` | Mapping layer: extended axis → parser canonical axis with usage notes |
| `sensory_modifier_groups.json` | Modifier group taxonomy for vocabulary annotation |
| `sensory_expression_patterns.jsonl` | Expression pattern library for cue design and ontology expansion |
| `general_sensory_vocabulary.csv` | General sensory vocabulary seed |
| `domain_vocabulary_seed.csv` | Domain-specific vocabulary (fragrance / taste / texture) |
| `domain_mapping.json` | Cross-domain sensory mapping for future recommendation layer |

## data/workflow — Candidate Review

Managed by `python -m sensory_atlas.cli review-candidates` and `select-curated-candidates`.

| File | Purpose |
| --- | --- |
| `sensory_object_candidates.jsonl` | Candidate pool — not yet in ontology |
| `candidate_review_status.jsonl` | Review status per candidate |
| `curated_candidate_shortlist_v1_5.jsonl` | v1.5 batch shortlist approved for promotion review |

**Workflow:** candidate pool → review-candidates → shortlist → manual promotion to `data/core/sensory_objects.jsonl`

## data/regression — Failure Tracking

Used for regression analysis across parser versions.

| File | Purpose |
| --- | --- |
| `dev_failure_cases.jsonl` | Curated holdout failures for regression tracking |
| `ontology_expansion_v1_5_cases.jsonl` | Cases that motivated v1.5 ontology expansion |

## Ontology Coverage

| Family | Objects | object_role distribution |
| --- | ---: | --- |
| Food_Texture | 11 | food_anchor ×8, compound_anchor ×3 |
| Organic | 9 | material_anchor ×7, scene_anchor ×2 |
| Textile | 7 | material_anchor ×7 |
| Mineral | 6 | material_anchor ×6 |
| Space_Scene | 6 | scene_anchor ×6 |
| Wood | 3 | material_anchor ×3 |
| Time_Season | 3 | temporal_anchor ×3 |
| Water_Air | 3 | scene_anchor ×2, temporal_anchor ×1 |
| Leather | 2 | material_anchor ×2 |
| Metal | 2 | material_anchor ×2 |
| Resin | 2 | material_anchor ×1, compound_anchor ×1 |
| Visual_Rendering | 2 | rendering_anchor ×2 |
| Smoke_Ash | 1 | scene_anchor ×1 |
| Texture | 1 | compound_anchor ×1 |

**Total:** 58 objects across 14 families
