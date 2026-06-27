# Sensory Atlas Evaluation Report

- Dataset: holdout
- Total test sentences: 50
- Top-1 hit rate: 0.64
- Top-3 hit rate: 0.78
- Low confidence cases: 12

| Test ID | Top-1 | Top-3 | Low confidence | Targets | Detected top 3 |
| --- | --- | --- | --- | --- | --- |
| holdout_001 | True | True | False | cashmere, warm_cotton, wool_blanket | cashmere, wool_blanket, warm_cotton |
| holdout_002 | True | True | False | warm_cotton, fresh_linen, cashmere | fresh_linen, warm_cotton, cashmere |
| holdout_003 | False | True | False | fresh_linen, clean_room, warm_cotton | dry_herb, black_tea, fresh_linen |
| holdout_004 | True | True | True | organza, silk, fresh_linen | organza |
| holdout_005 | False | False | True | velvet, dark_chocolate | marble |
| holdout_006 | True | True | False | wool_blanket, cashmere, warm_cotton | cashmere, fresh_linen, warm_cotton |
| holdout_007 | False | True | False | silk, organza, velvet | fresh_linen, warm_cotton, silk |
| holdout_008 | True | True | False | winter_dawn, cut_diamond, crystal | crystal, winter_dawn, mountain_stream |
| holdout_009 | True | True | True | cut_diamond, crystal, cold_metal | cut_diamond |
| holdout_010 | True | True | True | cold_metal, silver_spoon, crystal | cold_metal |
| holdout_011 | False | False | True | wet_stone, slate, granite | velvet, cold_fog, green_stem |
| holdout_012 | False | False | False | slate, cold_metal, cut_diamond | cedarwood, old_wood, fireplace_ash |
| holdout_013 | True | True | False | silver_spoon, cold_metal | silver_spoon, cold_metal, crystal |
| holdout_014 | True | True | False | marble, cold_metal, crystal | crystal, marble, winter_dawn |
| holdout_015 | True | True | False | wet_moss, forest_floor, after_rain_garden | wet_moss, cold_fog, forest_floor |
| holdout_016 | True | True | False | forest_floor, wet_moss, old_wood | old_wood, bark, old_library |
| holdout_017 | True | True | False | green_stem, wet_moss, citrus_peel | green_stem, after_rain_garden, wet_moss |
| holdout_018 | False | True | False | dry_herb, black_tea, cedarwood | green_stem, dry_herb, old_library |
| holdout_019 | False | True | False | pine_resin, cedarwood, forest_floor | old_wood, burnt_sugar, pine_resin |
| holdout_020 | False | False | True | bark, cedarwood, dry_herb | slate |
| holdout_021 | True | True | True | after_rain_garden, green_stem, wet_moss | after_rain_garden, green_stem, wet_moss |
| holdout_022 | True | True | True | winter_dawn, cold_fog, mountain_stream | mountain_stream |
| holdout_023 | True | True | False | mountain_stream, wet_stone, crystal | mountain_stream, wet_moss, wet_stone |
| holdout_024 | False | False | True | sea_breeze, fresh_linen, mountain_stream | summer_noon |
| holdout_025 | False | False | False | cold_fog, late_night_air, winter_dawn | four_k_clarity, mountain_stream, cut_diamond |
| holdout_026 | True | True | True | summer_noon, citrus_peel, fresh_linen | citrus_peel, summer_noon |
| holdout_027 | False | False | False | late_night_air, film_grain, cold_fog | dark_chocolate, tobacco_leaf, velvet |
| holdout_028 | False | True | False | mountain_stream, crystal, winter_dawn | organza, crystal, fresh_linen |
| holdout_029 | True | True | False | roasted_almond, butter_toast, burnt_sugar | butter_toast, roasted_almond, vanilla_cream |
| holdout_030 | True | True | False | butter_toast, vanilla_cream, roasted_almond | butter_toast, roasted_almond, vanilla_cream |
| holdout_031 | True | True | False | vanilla_cream, honeycomb, butter_toast | vanilla_cream, honeycomb, butter_toast |
| holdout_032 | True | True | False | honeycomb, burnt_sugar, vanilla_cream | burnt_sugar, cashmere, fresh_linen |
| holdout_033 | True | True | False | burnt_sugar, dark_chocolate, charred_oak | burnt_sugar, charred_oak |
| holdout_034 | False | False | False | dark_chocolate, velvet, burnt_sugar | silver_spoon, crystal, cold_metal |
| holdout_035 | True | True | False | roasted_almond, butter_toast, dry_herb | roasted_almond, butter_toast, burnt_sugar |
| holdout_036 | False | True | False | leather, suede, old_wood | butter_toast, old_library, old_wood |
| holdout_037 | True | True | False | charred_oak, fireplace_ash, old_wood | old_wood, old_library, black_tea |
| holdout_038 | True | True | True | fireplace_ash, charred_oak, slate | fireplace_ash |
| holdout_039 | False | True | False | old_wood, cedarwood, old_library | black_tea, old_wood, old_library |
| holdout_040 | False | False | False | cedarwood, old_wood, dry_herb | fresh_linen, warm_cotton, silk |
| holdout_041 | False | False | False | tobacco_leaf, dry_herb, leather | black_tea, warm_cotton, butter_toast |
| holdout_042 | True | True | False | barrel_cellar, old_wood, leather | old_wood, old_library, barrel_cellar |
| holdout_043 | True | True | False | film_grain, old_library, late_night_air | film_grain, old_library, late_night_air |
| holdout_044 | True | True | False | four_k_clarity, cut_diamond, crystal | four_k_clarity, cut_diamond, crystal |
| holdout_045 | True | True | False | old_library, old_wood, film_grain | old_library, clean_room |
| holdout_046 | True | True | False | clean_room, fresh_linen, warm_cotton | warm_cotton, cold_fog, fresh_linen |
| holdout_047 | True | True | False | rainy_street, rain_on_asphalt, wet_stone | wet_stone, rain_on_asphalt, wet_moss |
| holdout_048 | False | False | True | rain_on_asphalt, rainy_street, wet_stone | cold_fog, cold_metal, slate |
| holdout_049 | True | True | False | clean_room, fresh_linen, warm_cotton | fresh_linen, clean_room, citrus_peel |
| holdout_050 | True | True | False | film_grain, late_night_air, old_library | film_grain, old_library, late_night_air |

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
| holdout_003 | 햇살 아래 바싹 마른 침구 가장자리처럼 가볍고 하얗게 떠 | fresh_linen, clean_room, warm_cotton | dry_herb, black_tea, fresh_linen |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_005 | 검은 극장 좌석을 손으로 쓸었을 때처럼 깊고 조용한 부드러움 | velvet, dark_chocolate | marble |  | low_confidence | Top-1 score is below the low-confidence threshold. |
| holdout_007 | 매끈한 얇은 천이 물처럼 흘러내리는데 빛은 낮고 차분해 | silk, organza, velvet | fresh_linen, warm_cotton, silk |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_011 | 비에 씻긴 회색 표면이 낮게 식어 있고 손에 약간의 물기가 묻어 | wet_stone, slate, granite | velvet, cold_fog, green_stem |  | low_confidence | Top-1 score is below the low-confidence threshold. |
| holdout_012 | 어두운 얇은 면이 층층이 벗겨지는 듯 건조하고 차게 끊겨 | slate, cold_metal, cut_diamond | cedarwood, old_wood, fireplace_ash |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_018 | 말라 비틀어진 잎을 손으로 부수면 나는 가볍고 쌉쌀한 초록 먼지 | dry_herb, black_tea, cedarwood | green_stem, dry_herb, old_library |  | atmosphere_overmatch | Atmospheric object dominated a material/object target. |
| holdout_019 | 끈적한 나무 수액이 햇볕에 데워진 듯 숲 냄새가 진하게 붙어 | pine_resin, cedarwood, forest_floor | old_wood, burnt_sugar, pine_resin |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_020 | 거친 줄기 표면을 긁었을 때처럼 마르고 어두운 식물성 결 | bark, cedarwood, dry_herb | slate |  | low_confidence | Top-1 score is below the low-confidence threshold. |
| holdout_024 | 소금기 어린 열린 공기가 얼굴 옆을 스치며 가볍게 식혀 | sea_breeze, fresh_linen, mountain_stream | summer_noon |  | low_confidence | Top-1 score is below the low-confidence threshold. |
| holdout_025 | 낮게 떠 있는 회백색 숨결이 윤곽을 지우며 서늘하게 번져 | cold_fog, late_night_air, winter_dawn | four_k_clarity, mountain_stream, cut_diamond |  | time_season_underweighted | Time or season cue did not survive into top 3. |
| holdout_027 | 자정이 지난 방의 공기처럼 어둡고 얇게 머무르는 잔향 | late_night_air, film_grain, cold_fog | dark_chocolate, tobacco_leaf, velvet |  | rendering_vs_material_confusion | Rendering target was not represented in detected top 3. |
| holdout_028 | 찬물로 헹군 유리잔 속 빈 공간처럼 투명하고 가볍게 올라와 | mountain_stream, crystal, winter_dawn | organza, crystal, fresh_linen |  | time_season_underweighted | Time or season cue did not survive into top 3. |
| holdout_034 | 어두운 갈색 덩어리가 입안에서 두껍고 매끄럽게 녹는 느낌 | dark_chocolate, velvet, burnt_sugar | silver_spoon, crystal, cold_metal |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_036 | 낡은 의자 팔걸이에 밴 따뜻하고 드라이한 어두운 잔향 | leather, suede, old_wood | butter_toast, old_library, old_wood |  | atmosphere_overmatch | Atmospheric object dominated a material/object target. |
| holdout_039 | 오래 닫혀 있던 나무 상자를 열었을 때의 마른 결이 조용히 남아 | old_wood, cedarwood, old_library | black_tea, old_wood, old_library |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_040 | 차분한 목재 조각에서 깨끗하고 건조한 향이 가늘게 이어져 | cedarwood, old_wood, dry_herb | fresh_linen, warm_cotton, silk |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_041 | 말린 잎을 담아둔 서랍처럼 따뜻하고 어둡게 식물성이 남아 | tobacco_leaf, dry_herb, leather | black_tea, warm_cotton, butter_toast |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_048 | 비가 막 지난 골목의 검은 바닥에서 차가운 증기가 올라와 | rain_on_asphalt, rainy_street, wet_stone | cold_fog, cold_metal, slate |  | low_confidence | Top-1 score is below the low-confidence threshold. |

### Top-3 failures

| Test ID | Input | Targets | Detected top 3 | Activated cue groups | Error Type | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| holdout_005 | 검은 극장 좌석을 손으로 쓸었을 때처럼 깊고 조용한 부드러움 | velvet, dark_chocolate | marble |  | low_confidence | Top-1 score is below the low-confidence threshold. |
| holdout_011 | 비에 씻긴 회색 표면이 낮게 식어 있고 손에 약간의 물기가 묻어 | wet_stone, slate, granite | velvet, cold_fog, green_stem |  | low_confidence | Top-1 score is below the low-confidence threshold. |
| holdout_012 | 어두운 얇은 면이 층층이 벗겨지는 듯 건조하고 차게 끊겨 | slate, cold_metal, cut_diamond | cedarwood, old_wood, fireplace_ash |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_020 | 거친 줄기 표면을 긁었을 때처럼 마르고 어두운 식물성 결 | bark, cedarwood, dry_herb | slate |  | low_confidence | Top-1 score is below the low-confidence threshold. |
| holdout_024 | 소금기 어린 열린 공기가 얼굴 옆을 스치며 가볍게 식혀 | sea_breeze, fresh_linen, mountain_stream | summer_noon |  | low_confidence | Top-1 score is below the low-confidence threshold. |
| holdout_025 | 낮게 떠 있는 회백색 숨결이 윤곽을 지우며 서늘하게 번져 | cold_fog, late_night_air, winter_dawn | four_k_clarity, mountain_stream, cut_diamond |  | time_season_underweighted | Time or season cue did not survive into top 3. |
| holdout_027 | 자정이 지난 방의 공기처럼 어둡고 얇게 머무르는 잔향 | late_night_air, film_grain, cold_fog | dark_chocolate, tobacco_leaf, velvet |  | rendering_vs_material_confusion | Rendering target was not represented in detected top 3. |
| holdout_034 | 어두운 갈색 덩어리가 입안에서 두껍고 매끄럽게 녹는 느낌 | dark_chocolate, velvet, burnt_sugar | silver_spoon, crystal, cold_metal |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_040 | 차분한 목재 조각에서 깨끗하고 건조한 향이 가늘게 이어져 | cedarwood, old_wood, dry_herb | fresh_linen, warm_cotton, silk |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_041 | 말린 잎을 담아둔 서랍처럼 따뜻하고 어둡게 식물성이 남아 | tobacco_leaf, dry_herb, leather | black_tea, warm_cotton, butter_toast |  | abstract_metaphor_too_broad | Metaphor is broad enough to map to multiple sensory families. |
| holdout_048 | 비가 막 지난 골목의 검은 바닥에서 차가운 증기가 올라와 | rain_on_asphalt, rainy_street, wet_stone | cold_fog, cold_metal, slate |  | low_confidence | Top-1 score is below the low-confidence threshold. |

### Low confidence cases

Low confidence case count: 12

| Test ID | Input | Top-1 | Score | Notes |
| --- | --- | --- | --- | --- |
| holdout_004 | 공기를 머금은 얇은 막이 스치듯 지나가며 서늘한 투명함만 남아 | organza | 0.12 | Top-1 score is below the low-confidence threshold. |
| holdout_005 | 검은 극장 좌석을 손으로 쓸었을 때처럼 깊고 조용한 부드러움 | marble | 0.09 | Top-1 score is below the low-confidence threshold. |
| holdout_009 | 빛이 얇은 절단면을 타고 튀는 듯 차고 깨끗하게 갈라져 | cut_diamond | 0.13 | Top-1 score is below the low-confidence threshold. |
| holdout_010 | 손끝에 닿은 창틀의 냉기처럼 단단하고 맑은 긴장감 | cold_metal | 0.11 | Top-1 score is below the low-confidence threshold. |
| holdout_011 | 비에 씻긴 회색 표면이 낮게 식어 있고 손에 약간의 물기가 묻어 | velvet | 0.13 | Top-1 score is below the low-confidence threshold. |
| holdout_020 | 거친 줄기 표면을 긁었을 때처럼 마르고 어두운 식물성 결 | slate | 0.13 | Top-1 score is below the low-confidence threshold. |
| holdout_021 | 비가 멈춘 화단 가장자리에서 흙과 잎의 물기가 같이 올라와 | after_rain_garden | 0.16 | Top-1 score is below the low-confidence threshold. |
| holdout_022 | 해가 뜨기 전 창문을 열었을 때 코끝이 맑게 비워지는 냉기 | mountain_stream | 0.09 | Top-1 score is below the low-confidence threshold. |
| holdout_024 | 소금기 어린 열린 공기가 얼굴 옆을 스치며 가볍게 식혀 | summer_noon | 0.13 | Top-1 score is below the low-confidence threshold. |
| holdout_026 | 정수리 위로 내려오는 한낮의 흰 열기처럼 밝고 건조하게 퍼져 | citrus_peel | 0.17 | Top-1 score is below the low-confidence threshold. |
| holdout_038 | 꺼진 불자리의 창백한 먼지가 손끝에서 부서지는 듯해 | fireplace_ash | 0.13 | Top-1 score is below the low-confidence threshold. |
| holdout_048 | 비가 막 지난 골목의 검은 바닥에서 차가운 증기가 올라와 | cold_fog | 0.17 | Top-1 score is below the low-confidence threshold. |

### Common Failure Patterns

- phrase cue missing
- abstract metaphor too broad
- rendering cue confused with material cue
- textile comfort confused with food comfort
- mineral cue confused with visual clarity
- atmosphere cue over-matched
- time/season cue too weak
