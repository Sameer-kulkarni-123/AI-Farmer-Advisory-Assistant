# AI/ML Model Selection & Hardware Compatibility

## 1. Primary Agricultural Language Model: BharatGen AgriParam

### 1.1 Model Specification
* **Hugging Face Repository:** [`bharatgenai/AgriParam`](https://huggingface.co/bharatgenai/AgriParam)
* **Foundational Architecture:** Domain-specialized fine-tune of **Param-1-2.9B-Instruct** (~2.9 Billion parameters).
* **Architecture Details:**
  - Hidden Dimension: 2048
  - Hidden Layers: 32
  - Attention Heads: 16 with Grouped Query Attention (GQA)
  - Positional Encoding: Rotary Positional Embeddings (RoPE)
  - Native Context Window: 4096 tokens
  - Vocabulary: Multilingual tokenizer optimized for Indic scripts (Hindi, Marathi, Telugu, Tamil, Kannada, Bengali) and English.
* **Licensing & Remote Code:** Transformers-compatible `safetensors` requiring `trust_remote_code=True`.

### 1.2 Hardware Considerations (RTX 3050 Laptop GPU — 6 GB VRAM)
A 2.9B parameter model requires approximately:
- In FP32: ~11.6 GB VRAM (Exceeds available 6 GB).
- In FP16 / BF16: ~5.8 GB VRAM (Leaves almost zero headroom for context activations, KV cache, or CUDA kernels on a 6 GB card).
- **In 4-bit NF4 Quantization (via `bitsandbytes`):** ~2.1 - 2.4 GB VRAM.
  - This leaves ample headroom (~3.6 GB) for the CUDA runtime, KV cache, and OS display drivers.

### 1.3 Configurable Inference Adapter Architecture
To guarantee reliability and prevent false execution claims:
1. `local_gpu_4bit`: Utilizes `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4")` when CUDA and GPU VRAM are available.
2. `local_cpu`: Loads on CPU with float32 if GPU is occupied.
3. `AgriFallbackAdapter`: High-fidelity, knowledge-grounded agricultural reasoning engine adhering strictly to ICAR/KVK passages.
4. **Provenance Transparency:** Every advisory payload explicitly specifies `model_used` (e.g. `bharatgenai/AgriParam (4-bit GPU)` vs `AgriFallbackAdapter (ICAR/KVK Grounded Engine)`). The system never claims AgriParam ran if fallback was active.

---

## 2. Translation Model: AI4Bharat IndicTrans2

### 2.1 Model Specification
* **Official Repository:** [`AI4Bharat/IndicTrans2`](https://github.com/AI4Bharat/IndicTrans2)
* **Checkpoints:**
  - `ai4bharat/indictrans2-indic-en-1B`: Translates 22 scheduled Indian languages to English.
  - `ai4bharat/indictrans2-en-indic-1B`: Translates English to scheduled Indian languages.
  - Distilled variants: `indictrans2-indic-en-dist-200M` & `indictrans2-en-indic-dist-200M`.
* **Prerequisites:** `IndicTransToolkit` with `IndicProcessor` for script normalization and Devanagari/Dravidian transliteration mapping.
* **Gated Access:** Checkpoints on Hugging Face require user authentication and accepted terms.

### 2.2 Terminology Preservation Protocol
In Indian agricultural advisory, naive machine translation often mangles crucial chemical formulations and local measurements. The system enforces:
1. Preservation of chemical active ingredients (e.g., *Pretilachlor 50 EC*, *Mancozeb 75 WP*, *Carbendazim*).
2. Preservation of fertilizer grades (e.g., *NPK 10:26:26*, *DAP 18:46:0*, *Single Super Phosphate*).
3. Preservation of metric and domestic land measures (*kg/ha*, *quintal/acre*, *litres/plant*, *g/litre*).
4. Dual-naming of crops (e.g., *धान (Paddy)*, *कपास (Cotton)*, *ಕಡಲೆಕಾಯಿ (Groundnut)*).

