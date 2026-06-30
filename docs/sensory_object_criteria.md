# Sensory Object Criteria

## Definition

A **sensory object** is a reusable sensory archetype that a user can reach for when describing a sensation.

It does not need to be a physical material. What it must be is a stable anchor — something that carries a consistent, recognizable sensory signature that most people can mentally grasp when named or evoked.

> "11월 말 새벽 공기처럼 차갑고 투명한 느낌"

Here, `winter_dawn` is the anchor. The user is not describing dawn as a fact; they are using it as a sensory reference point.

## Criteria

A candidate qualifies as a sensory object if it meets all three conditions:

**1. Anchor-ability**
A user who encounters this object as a reference can immediately form a shared sensory image. Abstract qualities alone do not qualify — the object must evoke something specific enough to anchor a description.

- `cashmere` ✓ — users share a recognizable warmth, softness, and weight
- `soft and warm` ✗ — too generic to anchor; describes a quality, not an object

**2. Axis consistency**
The object maps reliably to a stable pattern across at least 3–4 sensory axes. Objects with highly variable axis profiles across contexts are not stable anchors.

- `marble` ✓ — consistently Cold temperature, Smooth texture, Gloss light, Mineral organic_mineral
- `nice smell` ✗ — no stable axis profile

**3. Distinctiveness**
The object is not fully covered by an existing object's definition and example expressions. If two objects would always be matched by the same expressions, one of them is redundant.

- `wet_moss` and `forest_floor` ✓ — distinct profiles despite being co-located (moss = material anchor, forest floor = scene anchor)
- A second "soft cotton" object alongside `warm_cotton` ✗ — redundant

## Object Roles

`object_role` describes how the object functions within the ontology. Every sensory object has exactly one role.

| object_role | Description | Examples |
| --- | --- | --- |
| `material_anchor` | A specific material or substance. Carries tactile, olfactory, or surface qualities. | cashmere, marble, cedarwood, dark_chocolate |
| `scene_anchor` | A place, environment, or spatial setting. Carries atmospheric and contextual qualities. | old_library, rain_on_asphalt, forest_floor |
| `temporal_anchor` | A time of day, season, or atmospheric condition. Carries light, temperature, and time qualities. | winter_dawn, late_night_air, cold_fog |
| `food_anchor` | A food or beverage. Carries taste, texture, and olfactory qualities in the edible domain. | butter_toast, dark_chocolate, black_tea |
| `rendering_anchor` | A visual rendering quality. Carries light, clarity, and rendering qualities. | film_grain, four_k_clarity |
| `compound_anchor` | A complex sensory experience that does not reduce to a single material or scene, but still functions as a recognizable anchor. | amber_glow, astringent_dryness, tea_like_clarity |

## Family

`family` describes the sensory domain or material class the object belongs to. It is used for browsing, filtering, and coverage analysis — not for parser scoring.

Current families: Textile, Leather, Mineral, Metal, Organic, Wood, Resin, Texture, Time_Season, Water_Air, Space_Scene, Food_Texture, Smoke_Ash, Visual_Rendering

Family names should be noun-based, capitalized, and represent a material class or scene domain — not an axis value.

**Avoid:** using axis value labels as family names (e.g., `Warm`, `Soft`, `Dense` are axis values, not families).

## What Does NOT Qualify

| Type | Why |
| --- | --- |
| Pure axis descriptor | `astringent` alone is a texture axis value, not an anchor. `astringent_dryness` qualifies as a compound_anchor because it describes a recognizable sensation type. |
| Product category | `whisky`, `perfume`, `candle` are product domains, not sensory objects. They may be linked via `associated_products`. |
| Generic modifier | `warm and soft`, `clean and fresh` are modifier combinations. They describe axes, not objects. |
| Duplicate coverage | An object whose definition and examples are fully covered by an existing object's `related_objects` and expressions. |

## Review Checklist for New Candidates

- [ ] Can a user use this as an anchor in a natural sensory sentence?
- [ ] Does it have a stable axis profile (3+ axes with consistent values)?
- [ ] Is it distinct from all existing objects with overlap score < 0.6?
- [ ] Does its `family` fit the existing taxonomy or justify a new family entry?
- [ ] Does it have at least 8 example expressions?
- [ ] Has it been assigned an `object_role`?
