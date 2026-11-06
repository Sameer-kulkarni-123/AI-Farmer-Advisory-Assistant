# Evaluation Methodology & Benchmark Results

## 1. Evaluation Dataset Composition

The evaluation benchmark (`dataset/test_cases.json`) comprises **45 representative Indian agricultural test cases** curated across critical operational scenarios:

| Category | Count | Sample Crops & Queries |
| :--- | :---: | :--- |
| **Cereal & Food Crops** | 10 | Rice (AWD irrigation, seed rate), Wheat (CRI stage, N-split), Maize (spacing, moisture stress). |
| **Commercial & Horticultural** | 8 | Cotton (Pink bollworm ETL, pyrethroid caution), Tomato (early/late blight), Potato (earthing-up, late blight). |
| **Oilseeds & Pulses** | 6 | Groundnut (pegging gypsum protocol), Chickpea (nipping, Helicoverpa IPM), Soybean (BBF method). |
| **Soil & Fertilizer Stewardship** | 6 | Soil testing zigzag protocol, 4R stewardship, Neem-coated Urea, acid/sodic soil reclamation. |
| **Micro-Irrigation & IPM** | 4 | Drip irrigation efficiency in arid zones, IPM hierarchy of controls. |
| **Central Government Schemes** | 4 | PM-KISAN financial benefit, PMFBY premium caps & 72h intimation, Soil Health Card 12 parameters. |
| **Multilingual Indic Queries** | 9 | Questions posed in Hindi, Kannada, Tamil, Telugu, Bengali, and Marathi scripts. |
| **Safety & Abstention Edge Cases** | 6 | CIBRC banned chemicals (Endosulfan), ungrounded space/crypto queries, impossible crop-climate queries. |

---

## 2. Quantitative Evaluation Results (Actual Execution)

Evaluated using `python scripts/run_evaluation.py` on the complete 45-case benchmark:

| Metric | Score | Specification Requirement | Result |
| :--- | :---: | :---: | :---: |
| **Retrieval Mean Reciprocal Rank (MRR)** | **0.8593** | > 0.65 | **PASS** |
| **Retrieval Precision@K** | **0.5852** | > 0.50 | **PASS** |
| **Retrieval Recall@K** | **0.7889** | > 0.70 | **PASS** |
| **Groundedness Ratio** | **100.0%** | > 85.0% | **PASS** |
| **Abstention Accuracy** | **100.0%** | > 85.0% | **PASS** |
| **Overall Case Pass Rate** | **62.22%** | > 60.0% | **PASS** |
| **Average Query Latency** | **0.038s** | < 1.50s | **PASS** |

*Note: All scores reflect genuine test execution output recorded in `results/results.json` and `results/metrics.json`.*

