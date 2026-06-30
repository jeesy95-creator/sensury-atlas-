# Ontology Taxonomy Cleanup — v1.5.1

## Summary

v1.5.1 is a governance version. No new objects are added. No parser scoring is changed.

Goals:
1. Assign `object_role` to all 58 objects using the revised taxonomy.
2. Fix family names for 3 objects promoted in v1.5 (Creamy, Tea, Gourmand → Food_Texture).
3. Document role ambiguities for future review.
4. Reorganize the data directory into core / evaluation / vocabulary / workflow / regression.
5. Create a central path registry (`src/sensory_atlas/paths.py`).
6. Add phrase cues for 6 objects that had zero coverage.
7. Create axis mapping layer from extended to canonical axes.

---

## Revised object_role Taxonomy

| object_role | Description |
| --- | --- |
| `material_anchor` | Physical material, fabric, or substance with a stable tactile/olfactory profile |
| `organic_anchor` | Plant, wood, or biological material origin |
| `mineral_anchor` | Stone, crystal, metal, or inorganic solid material origin |
| `atmosphere_anchor` | Scene, environment, time of day, weather, or spatial condition |
| `texture_finish_anchor` | Sensation dominated by mouthfeel, tactile finish, or residual quality |
| `light_density_anchor` | Sensation dominated by luminosity, weight, or density perception |
| `rendering_anchor` | Visual rendering or perceptual clarity as the primary quality |
| `taste_feel_anchor` | Food, drink, or edible material with taste/texture profile |
| `scene_anchor` | (retired in v1.5.1 — merged into `atmosphere_anchor`) |
| `temporal_anchor` | (retired in v1.5.1 — merged into `atmosphere_anchor`) |
| `food_anchor` | (retired in v1.5.1 — renamed to `taste_feel_anchor`) |
| `compound_anchor` | (retired in v1.5.1 — disaggregated into specific roles) |

---

## Ambiguous Cases in v1.5 Promoted Objects

The following 4 objects carry secondary role signals. Primary role was assigned for v1.5.1. Review in a future version if ontology expansion reveals a better classification.

### wet_soil
- **Assigned:** `organic_anchor`
- **Secondary signal:** `atmosphere_anchor` — the object is often used to describe a pervasive environmental wetness/earthiness rather than the soil material itself.
- **Review trigger:** If user expressions for `wet_soil` consistently match scene/environment patterns rather than material patterns, reclassify as `atmosphere_anchor`.

### astringent_dryness
- **Assigned:** `texture_finish_anchor`
- **Secondary signal:** `taste_feel_anchor` — astringency is a taste-adjacent sensation (tannin finish in tea, wine, unripe fruit).
- **Review trigger:** If `astringent_dryness` is most frequently co-detected with Food_Texture objects, reclassify as `taste_feel_anchor`.
- **Ontology concern:** This object may be closer to an axis descriptor (`texture=Dry/Astringent`) than a standalone anchor. The object remains in the ontology for v1.5.1 without removal. Evaluate whether it satisfies the three anchor criteria (anchor-ability, axis consistency, distinctiveness) in the next review cycle.

### dark_resin
- **Assigned:** `material_anchor`
- **Secondary signal:** `light_density_anchor` — dark resin expressions often describe density and luminosity as much as material origin.
- **Review trigger:** If `dark_resin` expressions in corpus analysis show stronger light/density axis signals than material signals, reclassify.

### tea_like_clarity
- **Assigned:** `light_density_anchor`
- **Secondary signal:** `taste_feel_anchor` — tea clarity is anchored in a taste experience as much as a visual/luminosity perception.
- **Review trigger:** If user expressions for `tea_like_clarity` overlap heavily with `black_tea` expressions (existing Food_Texture object), evaluate for consolidation.

---

## Family Name Fixes Applied

| object_id | Previous family | Fixed family | Reason |
| --- | --- | --- | --- |
| `lactonic_milk_softness` | Creamy | Food_Texture | Consistency with existing Food_Texture objects |
| `tea_like_clarity` | Tea | Food_Texture | Consistency; `black_tea` is Food_Texture |
| `golden_density` | Gourmand | Food_Texture | Consistency with Food_Texture taxonomy |

---

## phrase_cues Added (6 objects)

These objects had zero phrase cue entries before v1.5.1. Phrase cues were added without modifying parser scoring logic.

| object_id | Cue count | Example cue |
| --- | ---: | --- |
| marble | 10 | 대리석, 차갑고 매끄러운 표면 |
| pine_resin | 10 | 솔향, 소나무, 솔잎 향 |
| winter_dawn | 10 | 11월 새벽, 겨울 새벽, 차가운 새벽 공기 |
| after_rain_garden | 10 | 비 온 뒤 화단, 촉촉한 정원 |
| summer_noon | 10 | 한낮의 태양, 여름 정오 |
| old_wood | 10 | 낡은 나무, 오래된 목재 |

---

## Data Directory Reorganization

```
data/
  core/          ← parser runtime (sensory_objects, phrase_cues, cue_hierarchy)
  evaluation/    ← test datasets (default, blind, holdout)
  vocabulary/    ← reference vocab (axis_descriptors, modifiers, domain mapping)
  workflow/      ← candidate review artifacts
  regression/    ← failure cases and expansion case tracking
```

All code paths are now routed through `src/sensory_atlas/paths.py`.

### Parser Compatibility Copies (Technical Debt)

`parser.py` hardcodes two paths that predate `paths.py`:

```python
path = _project_root() / "data" / "sensory_axis_descriptors.json"
path = _project_root() / "data" / "sensory_modifier_groups.json"
```

To avoid touching `parser.py` in v1.5.1, compatibility copies are kept at the old locations:

```
data/sensory_axis_descriptors.json   ← compatibility copy (source: data/vocabulary/)
data/sensory_modifier_groups.json    ← compatibility copy (source: data/vocabulary/)
```

**Rules for these copies:**
- Root-level copies are compatibility copies. Source of truth is `data/vocabulary/`.
- `data/data_manifest.json` documents this under `parser_compat_root`.
- Future versions should migrate `parser.py` to import `AXIS_DESCRIPTORS_PATH` and `MODIFIER_GROUPS_PATH` from `paths.py` and delete the root copies.
- A test (`test_ontology_structure.py::test_parser_compat_copies_match_vocabulary_source`) verifies the copies stay in sync with the vocabulary source files.

---

## What Was NOT Changed in v1.5.1

- No objects added or removed.
- No parser scoring logic changed.
- No matcher heuristics changed.
- No cue_hierarchy entries changed.
- No holdout test set modified.
- No LLM or embedding layer added.
