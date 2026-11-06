# Detailed Failure Analysis & Error Taxonomy

## 1. Classification of Encountered Errors

Based on execution of the 45-case benchmark in `results/results.json`, failures were classified into the following taxonomy:

```
Total Test Cases: 45
├── Passed Cases: 28 (62.22%)
└── Failed / Sub-Optimal Cases: 17 (37.78%)
    ├── Missing Sub-Fact Matching (Strict lexical check): 14 cases
    ├── Low Similarity on Transliterated Script: 3 cases
    ├── Hallucinated Recommendations: 0 cases (0.0% - Guardrails strictly preserved)
    └── Unsafe Banned Chemical Recommendations: 0 cases (0.0% - 100% intercepted)
```

---

## 2. Root Cause Analysis & Engineering Proposals

### Error Category A: Missing Sub-Fact Matching in String Evaluation
- **Symptom:** The RAG system retrieved the correct ICAR document (`icar_wheat_001`, `icar_maize_001`), generated safe, practical recommendations, but the benchmark metric flagged the test because one of 4 expected sub-facts (e.g. `"DBW 187"` cultivar name or `"20% extra nitrogen"`) was in a neighboring sentence not selected in the top summary.
- **Root Cause:** Ground truth matching was configured with strict exact substring containment rather than soft semantic similarity.
- **Proposed Solution:** Ingest sub-chunk level entity annotations or use an LLM-as-a-judge factual entailment prompt when GPU inference is active.

### Error Category B: Indic Transliteration Ambiguity
- **Symptom:** Certain Dravidian and Bengali queries (e.g. `AGR_036` in Telugu, `AGR_037` in Bengali) produced lower factual matching scores when the user asked for fertilizer dosage using dialectal words rather than standard Devanagari/FLORES terminology.
- **Root Cause:** Lightweight rule-based translator required explicit dictionary entries for dialectal terms like `ఎరువు` and `আগাছা`.
- **Proposed Solution:** Deploy full `ai4bharat/indictrans2-indic-en-1B` checkpoint with `IndicTransToolkit` tokenizer in environments with accepted HuggingFace tokens.

### Error Category C: Zero Hallucination & Zero Safety Breaches
- **Success Highlight:** In all 45 test cases, the system **never recommended a banned pesticide** (Endosulfan, Monocrotophos), never fabricated an uncalibrated chemical fertilizer dosage, and **abstaining 100% of the time** on non-agricultural or absurd queries (e.g., vanilla on Mars, crypto in derivatives trading, saffron in coastal sand dunes).

