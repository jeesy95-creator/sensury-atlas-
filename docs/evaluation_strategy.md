# Evaluation Strategy

Sensory Atlas is not evaluated with a single accuracy number.

The project uses staged evaluation to separate sanity checks from generalization pressure.

## Dataset Stages

### default

Purpose: ontology sanity check. The default set contains expressions close to the seed vocabulary.

### blind

Purpose: phrase-level generalization. The blind set avoids direct object names but stays within the known design space.

### holdout

Purpose: stricter metaphor generalization. The holdout set avoids direct object names and tries not to reuse phrase cues.

## Current Results

| Dataset | Purpose | Total | Top-1 | Top-3 | Low Confidence |
| --- | --- | ---: | ---: | ---: | ---: |
| default | Ontology sanity check | 20 | 1.00 | 1.00 | 0 |
| blind | Phrase-level generalization | 30 | 1.00 | 1.00 | 1 |
| holdout | Stricter metaphor generalization | 50 | 0.64 | 0.78 | 12 |

## How To Interpret Holdout

Holdout performance should not be maximized by simply adding exact cues from the holdout set. The value of holdout is diagnostic:

- Where does the parser score nothing?
- Where does an atmosphere object over-match?
- Where does rendering conflict with material?
- Which expressions need user confirmation?

## Failure Types

- `phrase_cue_missing`
- `abstract_metaphor_too_broad`
- `rendering_vs_material_confusion`
- `food_vs_textile_confusion`
- `mineral_vs_visual_confusion`
- `atmosphere_overmatch`
- `time_season_underweighted`
- `low_confidence`

## Next Improvements

- Add axis-level evidence
- Track confidence per axis
- Generate clarification questions for low-confidence cases
- Add candidate sensory object discovery
- Compare rule-based output with LLM-assisted output later
