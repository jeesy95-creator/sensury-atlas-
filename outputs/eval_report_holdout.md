# Sensory Atlas Evaluation Report

- Dataset: holdout
- Total test sentences: 50
- Top-1 hit rate: 0.78
- Top-3 hit rate: 0.88
- Low confidence cases: 6

| Test ID | Top-1 | Top-3 | Low confidence | Targets | Detected top 3 |
| --- | --- | --- | --- | --- | --- |
| holdout_001 | True | True | False | cashmere, warm_cotton, wool_blanket | cashmere, wool_blanket, warm_cotton |
| holdout_002 | True | True | False | warm_cotton, fresh_linen, cashmere | fresh_linen, warm_cotton, cashmere |
| holdout_003 | True | True | False | fresh_linen, clean_room, warm_cotton | fresh_linen, dry_herb, black_tea |
| holdout_004 | True | True | True | organza, silk, fresh_linen | organza, silk, fresh_linen |
| holdout_005 | True | True | True | velvet, dark_chocolate | dark_chocolate, velvet, burnt_sugar |
| holdout_006 | True | True | False | wool_blanket, cashmere, warm_cotton | cashmere, warm_cotton, fresh_linen |
| holdout_007 | False | True | False | silk, organza, velvet | fresh_linen, warm_cotton, silk |
| holdout_008 | True | True | False | winter_dawn, cut_diamond, crystal | winter_dawn, crystal, cut_diamond |
| holdout_009 | True | True | False | cut_diamond, crystal, cold_metal | cut_diamond, crystal, winter_dawn |
| holdout_010 | True | True | False | cold_metal, silver_spoon, crystal | cold_metal, crystal, silver_spoon |
| holdout_011 | True | True | False | wet_stone, slate, granite | wet_stone, wet_moss, mountain_stream |
| holdout_012 | False | True | False | slate, cold_metal, cut_diamond | old_wood, cedarwood, slate |
| holdout_013 | True | True | False | silver_spoon, cold_metal | silver_spoon, cold_metal, crystal |
| holdout_014 | True | True | False | marble, cold_metal, crystal | crystal, marble, winter_dawn |
| holdout_015 | True | True | False | wet_moss, forest_floor, after_rain_garden | wet_moss, forest_floor, cold_fog |
| holdout_016 | True | True | False | forest_floor, wet_moss, old_wood | old_wood, old_library, bark |
| holdout_017 | True | True | False | green_stem, wet_moss, citrus_peel | green_stem, after_rain_garden, wet_moss |
| holdout_018 | True | True | False | dry_herb, black_tea, cedarwood | dry_herb, green_stem, forest_floor |
| holdout_019 | False | True | False | pine_resin, cedarwood, forest_floor | old_wood, burnt_sugar, pine_resin |
| holdout_020 | False | False | True | bark, cedarwood, dry_herb | slate, green_stem, tobacco_leaf |
| holdout_021 | True | True | True | after_rain_garden, green_stem, wet_moss | after_rain_garden, wet_moss, green_stem |
| holdout_022 | True | True | False | winter_dawn, cold_fog, mountain_stream | winter_dawn, mountain_stream, crystal |
| holdout_023 | True | True | False | mountain_stream, wet_stone, crystal | mountain_stream, wet_moss, crystal |
| holdout_024 | True | True | True | sea_breeze, fresh_linen, mountain_stream | sea_breeze, clean_room, organza |
| holdout_025 | False | False | False | cold_fog, late_night_air, winter_dawn | four_k_clarity, mountain_stream, cut_diamond |
| holdout_026 | True | True | False | summer_noon, citrus_peel, fresh_linen | summer_noon, citrus_peel |
| holdout_027 | False | False | False | late_night_air, film_grain, cold_fog | dark_chocolate, tobacco_leaf, velvet |
| holdout_028 | False | True | False | mountain_stream, crystal, winter_dawn | organza, crystal, fresh_linen |
| holdout_029 | True | True | False | roasted_almond, butter_toast, burnt_sugar | butter_toast, roasted_almond, vanilla_cream |
| holdout_030 | True | True | False | butter_toast, vanilla_cream, roasted_almond | butter_toast, vanilla_cream, roasted_almond |
| holdout_031 | True | True | False | vanilla_cream, honeycomb, butter_toast | vanilla_cream, honeycomb, butter_toast |
| holdout_032 | True | True | False | honeycomb, burnt_sugar, vanilla_cream | burnt_sugar, cashmere, dark_chocolate |
| holdout_033 | True | True | False | burnt_sugar, dark_chocolate, charred_oak | burnt_sugar, charred_oak, vanilla_cream |
| holdout_034 | False | False | False | dark_chocolate, velvet, burnt_sugar | silver_spoon, cold_metal, crystal |
| holdout_035 | True | True | False | roasted_almond, butter_toast, dry_herb | roasted_almond, butter_toast, dark_chocolate |
| holdout_036 | True | True | False | leather, suede, old_wood | old_wood, old_library, butter_toast |
| holdout_037 | True | True | False | charred_oak, fireplace_ash, old_wood | old_wood, old_library, cedarwood |
| holdout_038 | True | True | True | fireplace_ash, charred_oak, slate | fireplace_ash |
| holdout_039 | True | True | False | old_wood, cedarwood, old_library | old_wood, black_tea, old_library |
| holdout_040 | False | True | False | cedarwood, old_wood, dry_herb | warm_cotton, fresh_linen, cedarwood |
| holdout_041 | False | False | False | tobacco_leaf, dry_herb, leather | black_tea, warm_cotton, butter_toast |
| holdout_042 | True | True | False | barrel_cellar, old_wood, leather | old_wood, old_library, leather |
| holdout_043 | True | True | False | film_grain, old_library, late_night_air | film_grain, old_library, late_night_air |
| holdout_044 | True | True | False | four_k_clarity, cut_diamond, crystal | four_k_clarity, crystal, mountain_stream |
| holdout_045 | True | True | False | old_library, old_wood, film_grain | old_library, old_wood, film_grain |
| holdout_046 | True | True | False | clean_room, fresh_linen, warm_cotton | warm_cotton, cold_fog, fresh_linen |
| holdout_047 | True | True | False | rainy_street, rain_on_asphalt, wet_stone | wet_stone, rainy_street, rain_on_asphalt |
| holdout_048 | False | False | False | rain_on_asphalt, rainy_street, wet_stone | cold_fog, cold_metal, mountain_stream |
| holdout_049 | True | True | False | clean_room, fresh_linen, warm_cotton | clean_room, fresh_linen, citrus_peel |
| holdout_050 | True | True | False | film_grain, late_night_air, old_library | film_grain, old_library, warm_cotton |

## Cue Group Analysis

| Cue Group | Count |
| --- | --- |
| film_like_rendering | 2 |
| food_roasted_warmth | 2 |
| cold_metal_tension | 1 |
| four_k_clarity | 1 |
| marble_hall_polish | 1 |
| mountain_water_flow | 1 |
| textile_body_warmth | 1 |
| wet_earth_green | 1 |

## Failure Analysis

### Top-1 failures

| Test ID | Input | Targets | Detected top 3 | Activated cue groups | Error Type | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| holdout_007 | 매끈한 얇은 천이 물처럼 흘러내리는데 빛은 낮고 차분해 | silk, organza, velvet | fresh_linen, warm_cotton, silk |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_012 | 어두운 얇은 면이 층층이 벗겨지는 듯 건조하고 차게 끊겨 | slate, cold_metal, cut_diamond | old_wood, cedarwood, slate |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_019 | 끈적한 나무 수액이 햇볕에 데워진 듯 숲 냄새가 진하게 붙어 | pine_resin, cedarwood, forest_floor | old_wood, burnt_sugar, pine_resin |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_020 | 거친 줄기 표면을 긁었을 때처럼 마르고 어두운 식물성 결 | bark, cedarwood, dry_herb | slate, green_stem, tobacco_leaf |  | low_confidence | Top-1 score is below the low-confidence threshold. |
| holdout_025 | 낮게 떠 있는 회백색 숨결이 윤곽을 지우며 서늘하게 번져 | cold_fog, late_night_air, winter_dawn | four_k_clarity, mountain_stream, cut_diamond |  | time_season_underweighted | Time or season cue did not survive into top 3. |
| holdout_027 | 자정이 지난 방의 공기처럼 어둡고 얇게 머무르는 잔향 | late_night_air, film_grain, cold_fog | dark_chocolate, tobacco_leaf, velvet |  | rendering_vs_material_confusion | Rendering target was not represented in detected top 3. |
| holdout_028 | 찬물로 헹군 유리잔 속 빈 공간처럼 투명하고 가볍게 올라와 | mountain_stream, crystal, winter_dawn | organza, crystal, fresh_linen |  | time_season_underweighted | Time or season cue did not survive into top 3. |
| holdout_034 | 어두운 갈색 덩어리가 입안에서 두껍고 매끄럽게 녹는 느낌 | dark_chocolate, velvet, burnt_sugar | silver_spoon, cold_metal, crystal |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_040 | 차분한 목재 조각에서 깨끗하고 건조한 향이 가늘게 이어져 | cedarwood, old_wood, dry_herb | warm_cotton, fresh_linen, cedarwood |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_041 | 말린 잎을 담아둔 서랍처럼 따뜻하고 어둡게 식물성이 남아 | tobacco_leaf, dry_herb, leather | black_tea, warm_cotton, butter_toast |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_048 | 비가 막 지난 골목의 검은 바닥에서 차가운 증기가 올라와 | rain_on_asphalt, rainy_street, wet_stone | cold_fog, cold_metal, mountain_stream |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |

### Top-3 failures

| Test ID | Input | Targets | Detected top 3 | Activated cue groups | Error Type | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| holdout_020 | 거친 줄기 표면을 긁었을 때처럼 마르고 어두운 식물성 결 | bark, cedarwood, dry_herb | slate, green_stem, tobacco_leaf |  | low_confidence | Top-1 score is below the low-confidence threshold. |
| holdout_025 | 낮게 떠 있는 회백색 숨결이 윤곽을 지우며 서늘하게 번져 | cold_fog, late_night_air, winter_dawn | four_k_clarity, mountain_stream, cut_diamond |  | time_season_underweighted | Time or season cue did not survive into top 3. |
| holdout_027 | 자정이 지난 방의 공기처럼 어둡고 얇게 머무르는 잔향 | late_night_air, film_grain, cold_fog | dark_chocolate, tobacco_leaf, velvet |  | rendering_vs_material_confusion | Rendering target was not represented in detected top 3. |
| holdout_034 | 어두운 갈색 덩어리가 입안에서 두껍고 매끄럽게 녹는 느낌 | dark_chocolate, velvet, burnt_sugar | silver_spoon, cold_metal, crystal |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_041 | 말린 잎을 담아둔 서랍처럼 따뜻하고 어둡게 식물성이 남아 | tobacco_leaf, dry_herb, leather | black_tea, warm_cotton, butter_toast |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_048 | 비가 막 지난 골목의 검은 바닥에서 차가운 증기가 올라와 | rain_on_asphalt, rainy_street, wet_stone | cold_fog, cold_metal, mountain_stream |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |

### Low confidence cases

Low confidence case count: 6

| Test ID | Input | Top-1 | Score | Notes |
| --- | --- | --- | --- | --- |
| holdout_004 | 공기를 머금은 얇은 막이 스치듯 지나가며 서늘한 투명함만 남아 | organza | 0.17 | Top-1 score is below the low-confidence threshold. |
| holdout_005 | 검은 극장 좌석을 손으로 쓸었을 때처럼 깊고 조용한 부드러움 | dark_chocolate | 0.18 | Top-1 score is below the low-confidence threshold. |
| holdout_020 | 거친 줄기 표면을 긁었을 때처럼 마르고 어두운 식물성 결 | slate | 0.19 | Top-1 score is below the low-confidence threshold. |
| holdout_021 | 비가 멈춘 화단 가장자리에서 흙과 잎의 물기가 같이 올라와 | after_rain_garden | 0.19 | Top-1 score is below the low-confidence threshold. |
| holdout_024 | 소금기 어린 열린 공기가 얼굴 옆을 스치며 가볍게 식혀 | sea_breeze | 0.20 | Top-1 score is below the low-confidence threshold. |
| holdout_038 | 꺼진 불자리의 창백한 먼지가 손끝에서 부서지는 듯해 | fireplace_ash | 0.16 | Top-1 score is below the low-confidence threshold. |

### Common Failure Patterns

- phrase cue missing
- abstract metaphor too broad
- rendering cue confused with material cue
- textile comfort confused with food comfort
- mineral cue confused with visual clarity
- atmosphere cue over-matched
- time/season cue too weak
