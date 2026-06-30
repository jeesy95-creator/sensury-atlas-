# Semantic Fallback Evaluation Report

- Dataset: holdout
- Total test sentences: 50
- Rule Top-1 hit rate: 0.78
- Rule Top-3 hit rate: 0.88
- Fallback assist Top-1 hit rate: 0.61
- Fallback assist Top-3 hit rate: 0.88
- Fallback used count: 33
- Fallback helped count: 5
- Fallback hurt count: 3
- Low confidence count: 5

| Test ID | Fallback Used | Reason | Targets | Rule Top 3 | Semantic Top 3 | Helped | Hurt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| holdout_001 | True | confidence_below_threshold | cashmere, warm_cotton, wool_blanket | cashmere, wool_blanket, warm_cotton | winter_dawn, incense_smoke, vanilla_cream | False | True |
| holdout_002 | True | ambiguous_with_clarification_questions | warm_cotton, fresh_linen, cashmere | fresh_linen, warm_cotton, cashmere | lactonic_milk_softness, velvet, rain_on_asphalt | False | True |
| holdout_003 | True | confidence_below_threshold | fresh_linen, clean_room, warm_cotton | fresh_linen, dry_herb, warm_cotton | fresh_linen, dry_herb, burnt_sugar | False | False |
| holdout_004 | True | low_confidence | organza, silk, fresh_linen | organza, silk, fresh_linen | organza, tea_like_clarity, winter_dawn | False | False |
| holdout_005 | True | low_confidence | velvet, dark_chocolate | dark_chocolate, velvet, burnt_sugar | velvet, lactonic_milk_softness, black_fruit_density | False | False |
| holdout_006 | True | confidence_below_threshold | wool_blanket, cashmere, warm_cotton | cashmere, warm_cotton, fresh_linen | winter_dawn, wool_blanket, cashmere | False | False |
| holdout_007 | False |  | silk, organza, velvet | fresh_linen, warm_cotton, silk |  | False | False |
| holdout_008 | True | confidence_below_threshold | winter_dawn, cut_diamond, crystal | winter_dawn, crystal, cut_diamond | cut_diamond, winter_dawn, burnt_sugar | False | False |
| holdout_009 | True | confidence_below_threshold | cut_diamond, crystal, cold_metal | cut_diamond, crystal, winter_dawn | crystal, clean_finish, aquatic_clean_water | False | False |
| holdout_010 | True | confidence_below_threshold | cold_metal, silver_spoon, crystal | cold_metal, crystal, silver_spoon | mineral_spark, granite, cold_metal | False | False |
| holdout_011 | True | confidence_below_threshold | wet_stone, slate, granite | wet_stone, wet_moss, mountain_stream | wet_stone, granite, fireplace_ash | False | False |
| holdout_012 | True | confidence_below_threshold | slate, cold_metal, cut_diamond | old_wood, cedarwood, slate | slate, tobacco_leaf, cedarwood | False | False |
| holdout_013 | False |  | silver_spoon, cold_metal | silver_spoon, cold_metal, crystal |  | False | False |
| holdout_014 | False |  | marble, cold_metal, crystal | crystal, marble, winter_dawn |  | False | False |
| holdout_015 | False |  | wet_moss, forest_floor, after_rain_garden | wet_moss, forest_floor, cold_fog |  | False | False |
| holdout_016 | True | confidence_below_threshold | forest_floor, wet_moss, old_wood | old_wood, old_library, bark | wet_moss, forest_floor, wet_soil | False | False |
| holdout_017 | True | confidence_below_threshold | green_stem, wet_moss, citrus_peel | green_stem, after_rain_garden, wet_moss | green_stem, green_leaf_crush, cut_diamond | False | False |
| holdout_018 | True | confidence_below_threshold | dry_herb, black_tea, cedarwood | dry_herb, green_stem, forest_floor | green_leaf_crush, dark_chocolate, dry_herb | False | False |
| holdout_019 | False |  | pine_resin, cedarwood, forest_floor | old_wood, burnt_sugar, pine_resin |  | False | False |
| holdout_020 | True | low_confidence | bark, cedarwood, dry_herb | slate, green_stem, forest_floor | green_stem, bark, tobacco_leaf | True | False |
| holdout_021 | False |  | after_rain_garden, green_stem, wet_moss | after_rain_garden, wet_moss, green_stem |  | False | False |
| holdout_022 | True | confidence_below_threshold | winter_dawn, cold_fog, mountain_stream | winter_dawn, mountain_stream, crystal | ozonic_air, late_night_air, winter_dawn | False | False |
| holdout_023 | True | confidence_below_threshold | mountain_stream, wet_stone, crystal | mountain_stream, wet_moss, crystal | mountain_stream, wet_stone, tea_like_clarity | False | False |
| holdout_024 | True | low_confidence | sea_breeze, fresh_linen, mountain_stream | sea_breeze, clean_room, organza | sea_breeze, organza, clean_room | False | False |
| holdout_025 | True | confidence_below_threshold | cold_fog, late_night_air, winter_dawn | four_k_clarity, mountain_stream, cut_diamond | cold_fog, silk, late_night_air | True | False |
| holdout_026 | True | confidence_below_threshold | summer_noon, citrus_peel, fresh_linen | summer_noon, citrus_peel, pine_resin | summer_noon, slate, black_tea | False | False |
| holdout_027 | True | confidence_below_threshold | late_night_air, film_grain, cold_fog | tobacco_leaf, dark_chocolate, velvet | velvet, organza, dark_chocolate | False | False |
| holdout_028 | True | confidence_below_threshold | mountain_stream, crystal, winter_dawn | organza, crystal, fresh_linen | organza, crystal, cold_glass | False | False |
| holdout_029 | True | ambiguous_with_clarification_questions | roasted_almond, butter_toast, burnt_sugar | butter_toast, roasted_almond, vanilla_cream | roasted_almond, butter_toast, burnt_sugar | False | False |
| holdout_030 | False |  | butter_toast, vanilla_cream, roasted_almond | butter_toast, vanilla_cream, roasted_almond |  | False | False |
| holdout_031 | False |  | vanilla_cream, honeycomb, butter_toast | vanilla_cream, honeycomb, butter_toast |  | False | False |
| holdout_032 | False |  | honeycomb, burnt_sugar, vanilla_cream | burnt_sugar, cashmere, dark_chocolate |  | False | False |
| holdout_033 | True | confidence_below_threshold | burnt_sugar, dark_chocolate, charred_oak | burnt_sugar, charred_oak, vanilla_cream | burnt_sugar, dry_spice, cut_diamond | False | False |
| holdout_034 | True | confidence_below_threshold | dark_chocolate, velvet, burnt_sugar | silver_spoon, cold_metal, crystal | silk, dark_chocolate, velvet | True | False |
| holdout_035 | False |  | roasted_almond, butter_toast, dry_herb | roasted_almond, butter_toast, dark_chocolate |  | False | False |
| holdout_036 | True | confidence_below_threshold | leather, suede, old_wood | old_wood, old_library, butter_toast | amber_glow, dry_spice, dark_resin | False | True |
| holdout_037 | False |  | charred_oak, fireplace_ash, old_wood | old_wood, old_library, cedarwood |  | False | False |
| holdout_038 | True | low_confidence | fireplace_ash, charred_oak, slate | fireplace_ash | dry_herb, fireplace_ash, roasted_almond | False | False |
| holdout_039 | False |  | old_wood, cedarwood, old_library | old_wood, black_tea, old_library |  | False | False |
| holdout_040 | True | confidence_below_threshold | cedarwood, old_wood, dry_herb | fresh_linen, warm_cotton, cedarwood | cedarwood, warm_cotton, tea_like_clarity | False | False |
| holdout_041 | True | confidence_below_threshold | tobacco_leaf, dry_herb, leather | black_tea, warm_cotton, butter_toast | tobacco_leaf, black_tea, warm_cotton | True | False |
| holdout_042 | False |  | barrel_cellar, old_wood, leather | old_wood, old_library, tobacco_leaf |  | False | False |
| holdout_043 | False |  | film_grain, old_library, late_night_air | film_grain, old_library, late_night_air |  | False | False |
| holdout_044 | False |  | four_k_clarity, cut_diamond, crystal | four_k_clarity, crystal, mountain_stream |  | False | False |
| holdout_045 | True | confidence_below_threshold | old_library, old_wood, film_grain | old_library, old_wood, film_grain | old_library, clean_room, old_wood | False | False |
| holdout_046 | True | confidence_below_threshold | clean_room, fresh_linen, warm_cotton | warm_cotton, cold_fog, fresh_linen | clean_room, warm_cotton, fresh_linen | False | False |
| holdout_047 | False |  | rainy_street, rain_on_asphalt, wet_stone | wet_stone, rainy_street, rain_on_asphalt |  | False | False |
| holdout_048 | True | confidence_below_threshold | rain_on_asphalt, rainy_street, wet_stone | cold_fog, cold_metal, mountain_stream | black_fruit_density, wet_soil, rain_on_asphalt | True | False |
| holdout_049 | True | confidence_below_threshold | clean_room, fresh_linen, warm_cotton | clean_room, fresh_linen, citrus_peel | clean_room, summer_noon, cedarwood | False | False |
| holdout_050 | False |  | film_grain, late_night_air, old_library | film_grain, old_library, warm_cotton |  | False | False |
