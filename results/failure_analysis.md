# AI Farmer Advisory Assistant — Failure Analysis & Error Taxonomy

**Execution Date:** 2026-11-06 06:23:50  
**Evaluated Cases:** 45  
**Identified Failures:** 17  

---

## 1. Error Taxonomy & Distribution

| Error Category | Count | % of Failures | Primary Cause |
| :--- | :---: | :---: | :--- |
| **Missing Agricultural Sources** | 0 | — | Niche agronomic topic or localized practice not present in initial 20 ICAR documents. |
| **Low Factual Correctness** | 17 | — | Retrieved chunk did not contain exact expected sub-fact (e.g. specific cultivar name). |
| **Failure to Abstain** | 0 | — | Semantic threshold allowed loosely related vector to answer ungrounded question. |
| **Translation Lexical Shift** | 0 | — | Transliterated crop names required fuzzy matching. |

---

## 2. Case-by-Case Breakdown

### Failure 1: [AGR_005] Wheat (English)
- **Query:** *"What is the optimal sowing date and seed rate for timely sown irrigated wheat?"*
- **Category:** `cultivation`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['icar_wheat_001', 'icar_wheat_002', 'icar_fertilizer_001', 'ncof_organic_001']`
- **Actual Recommendation:** `Optimal sowing window is November 1 to November 15 for timely sown irrigated conditions....`
- **Root Cause:** Ground truth expected facts ['November 1 to November 15', '100 kg/ha', 'DBW 187', 'HD 3086'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 2: [AGR_006] Wheat (English)
- **Query:** *"How should nitrogen fertilizer be split in wheat in the North Western Plains?"*
- **Category:** `fertilizer`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['gov_scheme_shc_001', 'dacfw_soil_001', 'icar_wheat_001', 'icar_irrigation_001']`
- **Actual Recommendation:** `Benefits: Helps farmers reduce indiscriminate use of urea, saves 15-20% fertilizer expenses, and prevents secondary micronutrient deficiencies....`
- **Root Cause:** Ground truth expected facts ['150:60:40', '1/3rd basal', '1/3rd CRI', '1/3rd boot stage'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 3: [AGR_008] Maize (English)
- **Query:** *"At which growth stages is maize most sensitive to water stress?"*
- **Category:** `irrigation`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['icar_maize_001', 'ncof_organic_001', 'icar_ncipm_001', 'dacfw_soil_001']`
- **Actual Recommendation:** `It cannot tolerate waterlogging even for 24-48 hours....`
- **Root Cause:** Ground truth expected facts ['knee-high', 'tasseling', 'silking', 'cannot tolerate waterlogging'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 4: [AGR_016] Pulses (English)
- **Query:** *"How should Helicoverpa pod borer be managed in chickpea?"*
- **Category:** `pest_management`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['icar_pulses_001', 'dacfw_soil_001', 'icar_fertilizer_001', 'ncof_organic_001']`
- **Actual Recommendation:** `Pest management: Gram pod borer (Helicoverpa armigera) is the most destructive pest....`
- **Root Cause:** Ground truth expected facts ['bird perches', 'pheromone traps', '5% NSKE', 'Chlorantraniliprole'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 5: [AGR_017] Sugarcane (English)
- **Query:** *"What are the key management practices for ratoon sugarcane crop?"*
- **Category:** `cultivation`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['icar_sugarcane_001', 'icar_ncipm_001', 'gov_scheme_shc_001', 'gov_scheme_pmkisan_001']`
- **Actual Recommendation:** `Apply 20% extra nitrogen to ratoon crop compared to plant cane....`
- **Root Cause:** Ground truth expected facts ['stubble shaving', 'off-barring', 'trash mulching', '20% extra nitrogen'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 6: [AGR_020] All Crops (English)
- **Query:** *"What are the 4R principles of nutrient stewardship in Indian agriculture?"*
- **Category:** `fertilizer`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['icar_irrigation_001', 'gov_scheme_shc_001', 'icar_rice_002', 'ncof_organic_001']`
- **Actual Recommendation:** `Drip irrigation delivers water directly to the plant root zone at low pressure (1.0 to 1.5 kg/cm2), achieving 90-95% water application efficiency compared to 35...`
- **Root Cause:** Ground truth expected facts ['Right Source', 'Right Rate', 'Right Time', 'Right Place'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 7: [AGR_021] All Crops (English)
- **Query:** *"Why is Neem-Coated Urea (NCU) superior to normal prilled urea?"*
- **Category:** `fertilizer`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['icar_fertilizer_001', 'icar_wheat_001', 'icar_soybean_001', 'gov_scheme_shc_001']`
- **Actual Recommendation:** `Urea Management: Use 100% Neem-Coated Urea (NCU)....`
- **Root Cause:** Ground truth expected facts ['slows nitrification', 'reduces volatilization', 'increases NUE'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 8: [AGR_022] All Crops (English)
- **Query:** *"How can acidic soils and sodic soils be reclaimed respectively?"*
- **Category:** `soil_health`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['dacfw_soil_001', 'icar_groundnut_001', 'gov_scheme_shc_001', 'icar_fertilizer_001']`
- **Actual Recommendation:** `Soil samples must be taken in a zigzag pattern across the field, collecting 10-15 sub-samples at 0-15 cm depth for field crops and 0-30 cm for horticultural cro...`
- **Root Cause:** Ground truth expected facts ['lime or dolomite for acid soils', 'gypsum for sodic soils', 'pH test'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 9: [AGR_027] All Crops (English)
- **Query:** *"What is the financial benefit and eligibility under the PM-KISAN scheme?"*
- **Category:** `government_schemes`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['gov_scheme_pmkisan_001', 'gov_scheme_shc_001', 'icar_tomato_001', 'icar_sugarcane_001']`
- **Actual Recommendation:** `Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) is a Central Sector Scheme launched to supplement the financial needs of landholding farmers....`
- **Root Cause:** Ground truth expected facts ['Rs. 6,000 per year', 'three equal installments of Rs. 2,000', 'landholding farmer families', 'DBT'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 10: [AGR_028] Food crops, Oilseeds, Commercial / Horticultural crops (English)
- **Query:** *"What is the maximum premium rate payable by farmers under PMFBY for Kharif and Rabi crops?"*
- **Category:** `government_schemes`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['gov_scheme_pmfby_001', 'gov_scheme_shc_001', 'icar_ncipm_001', 'gov_scheme_pmkisan_001']`
- **Actual Recommendation:** `Premium Rates payable by Farmers: 1....`
- **Root Cause:** Ground truth expected facts ['2.0% for Kharif', '1.5% for Rabi', '5.0% for horticultural', '72 hours intimation'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 11: [AGR_029] All Crops (English)
- **Query:** *"How often is a Soil Health Card issued and how many soil parameters does it test?"*
- **Category:** `government_schemes`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['gov_scheme_shc_001', 'dacfw_soil_001', 'icar_pulses_001', 'icar_groundnut_001']`
- **Actual Recommendation:** `Frequency: Soil Health Cards are issued to farmers every 2 years for their specific land holdings....`
- **Root Cause:** Ground truth expected facts ['every 2 years', '12 parameters', 'NPK', 'secondary nutrients', 'micronutrients'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 12: [AGR_030] Rice (Hindi)
- **Query:** *"धान की बुवाई के लिए बीज दर और कतार से कतार की दूरी कितनी होनी चाहिए?"*
- **Category:** `cultivation`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['icar_ncipm_001', 'icar_rice_002', 'icar_rice_001', 'icar_irrigation_001']`
- **Actual Recommendation:** `[अनुशंसा / सलाह] Integrated Pest Management (IPM) is the coordinated use of pest and environmental information with available pest control methods to prevent un...`
- **Root Cause:** Ground truth expected facts ['35-40 kg/ha', '20 cm x 15 cm', '2-3 seedlings'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 13: [AGR_031] Wheat (Hindi)
- **Query:** *"गेहूं में पहली सिंचाई किस अवस्था पर करनी चाहिए?"*
- **Category:** `irrigation`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['icar_wheat_002', 'icar_irrigation_001', 'icar_wheat_001', 'ncof_organic_001']`
- **Actual Recommendation:** `[अनुशंसा / सलाह] Wheat requires 4 to 6 irrigations of 6-7 cm depth depending on soil type and winter rainfall....`
- **Root Cause:** Ground truth expected facts ['CRI', 'Crown Root Initiation', '20-25'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 14: [AGR_033] Rice (Kannada)
- **Query:** *"ಭತ್ತದ ಬೆಳೆಗೆ ಪರ್ಯಾಯ ತೇವ ಮತ್ತು ಒಣಗಿಸುವ ನೀರಾವರಿ ಪದ್ಧತಿಯನ್ನು ಹೇಗೆ ಅಳವಡಿಸಬೇಕು?"*
- **Category:** `irrigation`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['icar_irrigation_001', 'icar_rice_002', 'ncof_organic_001', 'icar_ncipm_001']`
- **Actual Recommendation:** `[ಕೃಷಿ ಶಿಫಾರಸು] Drip irrigation delivers water directly to the plant root zone at low pressure (1.0 to 1.5 kg/cm2), achieving 90-95% water application efficiency...`
- **Root Cause:** Ground truth expected facts ['Alternate Wetting and Drying', 'panicle initiation', 'pani pipe'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 15: [AGR_036] Maize (Telugu)
- **Query:** *"మొక్కజొన్న పంటలో సిఫార్సు చేసిన మొక్కల సాంద్రత మరియు ఎరువుల మోతాదు ఎంత?"*
- **Category:** `cultivation`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['icar_maize_001', 'gov_scheme_shc_001', 'icar_irrigation_001', 'dacfw_soil_001']`
- **Actual Recommendation:** `[వ్యవసాయ సిఫార్సు] Maize (Zea mays) thrives in well-drained, sandy loam to silty loam soils with pH 6.0 to 7.5....`
- **Root Cause:** Ground truth expected facts ['60 cm x 20 cm', '83,333', '120-150:60:40'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 16: [AGR_037] Rice (Bengali)
- **Query:** *"বোরো ধানে সেচ ব্যবস্থাপনা এবং আগাছা দমনের নিয়ম কী?"*
- **Category:** `cultivation`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['icar_irrigation_001', 'icar_rice_002', 'ncof_organic_001', 'icar_ncipm_001']`
- **Actual Recommendation:** `[কৃষি পরামর্শ ও সুপারিশ] Drip irrigation delivers water directly to the plant root zone at low pressure (1.0 to 1.5 kg/cm2), achieving 90-95% water application ...`
- **Root Cause:** Ground truth expected facts ['Pretilachlor', 'conoweeder', 'shallow water'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
### Failure 17: [AGR_044] All Crops (English)
- **Query:** *"Can I diagnose my crop disease just by looking at a yellow leaf without a soil or lab test?"*
- **Category:** `disease`
- **Error Classification:** `Low factual correctness matching ground truth` (Severity: `High`)
- **Retrieved Evidence:** `['icar_groundnut_001', 'dacfw_soil_001', 'icar_tomato_001', 'icar_pulses_001']`
- **Actual Recommendation:** `Mandatory rule: Never apply uncalibrated chemical fertilizers without testing soil; over-application of urea leads to groundwater nitrate contamination and soil...`
- **Root Cause:** Ground truth expected facts ['cannot definitively diagnose', 'KVK', 'Soil Health Card', 'nutrient deficiency or pathogen'] were not fully covered or matched by the retrieved chunk.
- **Proposed Engineering Solution:** Expand knowledge base coverage or tune embedding similarity threshold.

---
