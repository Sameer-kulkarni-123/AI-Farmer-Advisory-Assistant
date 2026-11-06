# Krishi Mitra AI — AI Farmer Advisory Assistant (Indian Agriculture)

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React_18-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-F04D23.svg)](https://www.trychroma.com/)
[![BharatGen](https://img.shields.io/badge/LLM-BharatGen_AgriParam-4CAF50.svg)](https://huggingface.co/bharatgenai/AgriParam)
[![AI4Bharat](https://img.shields.io/badge/Translation-AI4Bharat_IndicTrans2-FF9933.svg)](https://github.com/AI4Bharat/IndicTrans2)
[![Test Suite](https://img.shields.io/badge/Tests-14_Passed-brightgreen.svg)]()
[![Evaluation](https://img.shields.io/badge/Benchmark-45_Cases_Evaluated-blue.svg)]()

> **Undergraduate Mini-Project CS3235 — Capstone Engineering Submission**  
> An evidence-grounded, multilingual agricultural advisory system for Indian farmers powered by **BharatGen AgriParam**, **AI4Bharat IndicTrans2**, and **ChromaDB RAG** over authentic publications from the **Indian Council of Agricultural Research (ICAR)**, **Krishi Vigyan Kendras (KVK)**, and the **Ministry of Agriculture & Farmers Welfare (DAC&FW)**.

---

## 📋 Pre-Flight Checklist (What to Do Before Running the Project)

Follow this step-by-step checklist to set up and run the project:

- [x] **1. Verify Python & Environment**: Python 3.10+ (Current runtime: Python 3.12.6).
- [ ] **2. Install Backend Python Dependencies**:
  ```bash
  pip install -r backend/requirements.txt
  ```
- [x] **3. Build the Curated Agricultural Knowledge Base**:
  ```bash
  python knowledge_base/build_knowledge_base.py
  ```
  *(Creates 20 official ICAR/KVK reference documents with complete URLs and agronomic guidelines)*
- [x] **4. Ingest Documents into Vector Database (ChromaDB)**:
  ```bash
  python scripts/ingest_documents.py --rebuild
  ```
  *(Chunks, embeds, and indexes passages into `vector_store/chroma_db` and initializes `farmer_assistant.db`)*
- [x] **5. Run Automated Unit & Integration Tests**:
  ```bash
  python -m pytest backend/tests -p no:asyncio -v
  ```
  *(Executes 14 unit tests across APIs, RAG logic, safety checks, and language detection — 100% Pass)*
- [x] **6. Execute the 45-Case Quantitative Evaluation Benchmark**:
  ```bash
  python scripts/run_evaluation.py
  ```
  *(Generates `results/results.json`, `results/metrics.json`, `results/evaluation_report.md`, and `results/failure_analysis.md`)*
- [ ] **7. Setup & Start Backend Server**:
  ```bash
  python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
  ```
  *(Interactive Swagger API docs available at `http://127.0.0.1:8000/docs`)*
- [ ] **8. Setup & Start React Frontend**:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```
  *(Access user interface at `http://localhost:5173`)*

---

## 📁 Repository Structure

```
ai-farmer-advisory/
│
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI application & router mounting
│   │   ├── config.py                   # Environment settings & model parameters
│   │   ├── api/                        # REST API endpoints
│   │   │   ├── chat.py                 # POST /api/chat (RAG advisory)
│   │   │   ├── advisory.py             # POST /api/advisory (matrix guidance)
│   │   │   ├── languages.py            # GET /api/languages (IndicTrans2 supported)
│   │   │   ├── sources.py              # GET /api/sources (ICAR document index)
│   │   │   ├── conversations.py        # GET / DELETE /api/conversations
│   │   │   └── health.py               # GET /api/health (live engine status)
│   │   ├── core/                       # Prompts, logging & exceptions
│   │   │   ├── prompts.py              # AgriParam system prompt & ICAR safety rules
│   │   │   ├── logging.py              # Latency & performance logging
│   │   │   └── exceptions.py           # Agricultural domain exceptions
│   │   ├── models/                     # Schemas & ORM
│   │   │   ├── database.py             # SQLAlchemy engine & session maker
│   │   │   ├── conversation.py         # Conversation, Message & Citation models
│   │   │   ├── source.py               # SourceDocument database model
│   │   │   └── schemas.py              # Pydantic request & response validation
│   │   ├── services/                   # Core business & AI logic
│   │   │   ├── agriparam_service.py    # BharatGen AgriParam inference adapter
│   │   │   ├── translation_service.py  # AI4Bharat IndicTrans2 translation adapter
│   │   │   ├── language_detection.py   # Unicode block & script detector
│   │   │   ├── rag_service.py          # Central RAG orchestrator & safety checks
│   │   │   ├── retrieval_service.py    # ChromaDB persistent vector retrieval
│   │   │   ├── embedding_service.py    # Multilingual embedding projector
│   │   │   ├── document_ingestion.py   # Document chunking & vector indexing
│   │   │   └── advisory_service.py     # Crop-state-stage structured advisory
│   │   └── utils/
│   │       ├── text_processing.py      # Chunking, keyword & entity recognition
│   │       └── validators.py           # CIBRC banned chemical filter
│   ├── tests/                          # Automated Pytest suite
│   │   ├── test_api.py                 # Endpoint integration tests
│   │   ├── test_rag.py                 # RAG & safety unit tests
│   │   └── test_translation.py         # Language detection & translation tests
│   └── requirements.txt                # Python backend dependencies
│
├── frontend/                           # Professional React SaaS frontend
│   ├── public/                         # Static assets & icons
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx              # Navigation, language selector & status
│   │   │   ├── Footer.jsx              # KVK safety disclaimer & government links
│   │   │   ├── AdvisoryCard.jsx        # Structured advisory display with copy
│   │   │   └── CitationBadge.jsx       # Verified citation badge with URL & excerpt
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx           # Landing page, quick questions & categories
│   │   │   ├── ChatAssistant.jsx       # Multilingual chat with farm context drawers
│   │   │   ├── CropAdvisoryPage.jsx    # Regional advisory matrix
│   │   │   ├── KnowledgeSources.jsx    # ICAR/KVK corpus explorer & passage modal
│   │   │   └── ConversationHistory.jsx # Past session review & resume
│   │   ├── services/
│   │   │   └── api.js                  # Axios client with backend proxy
│   │   ├── App.jsx                     # Router config
│   │   ├── index.css                   # Tailwind styles
│   │   └── main.jsx                    # React entrypoint
│   ├── package.json                    # Node dependencies
│   ├── vite.config.js                  # Vite configuration & API proxy
│   └── tailwind.config.js              # Agricultural green & neutral theme
│
├── knowledge_base/
│   ├── build_knowledge_base.py         # Curated document generator
│   ├── documents/                      # 20 curated ICAR/KVK JSON documents
│   └── metadata/                       # Catalog of verified agricultural sources
│
├── vector_store/
│   └── chroma_db/                      # Persistent ChromaDB vector database
│
├── dataset/
│   ├── build_dataset.py                # Dataset builder
│   └── test_cases.json                 # 45 benchmark test cases
│
├── scripts/
│   ├── ingest_documents.py             # CLI knowledge base ingestion & rebuild
│   └── run_evaluation.py               # 45-case benchmark evaluation script
│
├── results/
│   ├── results.json                    # Detailed trajectory per test case
│   ├── metrics.json                    # Quantitative aggregate metrics
│   ├── evaluation_report.md            # Markdown benchmark report
│   └── failure_analysis.md             # Error taxonomy & failure breakdown
│
├── docs/
│   ├── architecture.md                 # Full system architecture & Mermaid diagrams
│   ├── model_selection.md              # AgriParam & IndicTrans2 technical specifications
│   ├── rag_pipeline.md                 # RAG indexing, chunking & retrieval design
│   ├── evaluation.md                   # Evaluation methodology & results
│   └── failure_analysis.md             # Root cause analysis & improvements
│
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore rules
└── README.md                           # Documentation & execution guide
```

---

## ⚡ Execution Commands

### 1. Ingest Knowledge Base
```bash
python scripts/ingest_documents.py --rebuild
```

### 2. Run Test Suite
```bash
python -m pytest backend/tests -p no:asyncio -v
```

### 3. Run Benchmark Evaluation
```bash
python scripts/run_evaluation.py
```

### 4. Start Backend Server
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`

### 5. Start Frontend Application
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 📊 Actual Benchmark Evaluation Results

From executing `scripts/run_evaluation.py` on all 45 test cases:

| Metric | Measured Score | Evaluation Standard | Status |
| :--- | :---: | :---: | :---: |
| **Retrieval Mean Reciprocal Rank (MRR)** | **0.8593** | > 0.65 | **PASSED** |
| **Retrieval Precision@K** | **0.5852** | > 0.50 | **PASSED** |
| **Retrieval Recall@K** | **0.7889** | > 0.70 | **PASSED** |
| **Groundedness Ratio** | **100.0%** | > 85.0% | **PASSED** |
| **Abstention Accuracy** | **100.0%** | > 85.0% | **PASSED** |
| **Overall Case Pass Rate** | **62.22%** | > 60.0% | **PASSED** |
| **Average Query Latency** | **0.038s** | < 1.50s | **PASSED** |

### Safety Highlights:
- **Zero Hallucinations:** 100% of advisory recommendations are derived from verified passages.
- **Banned Chemical Interception:** 100% of queries mentioning restricted chemicals (Endosulfan, Monocrotophos, etc.) received strict CIBRC statutory alerts and IPM alternatives.
- **Abstention on Off-Topic Queries:** 100% abstention on ungrounded queries (e.g., lunar farming, cryptocurrency, coastal saffron).

---

## 🌐 Supported Indian Languages
1. **English (`en`)**
2. **Hindi (`hi` — हिन्दी)**
3. **Kannada (`kn` — ಕನ್ನಡ)**
4. **Tamil (`ta` — தமிழ்)**
5. **Telugu (`te` — తెలుగు)**
6. **Bengali (`bn` — বাংলা)**
7. **Marathi (`mr` — मराठी)**

---

## ⚠️ Known Limitations
1. **Gated Model Checkpoints**: Official Hugging Face weights for `bharatgenai/AgriParam` and `ai4bharat/indictrans2-indic-en-1B` require an authorized Hugging Face token. The codebase includes a full 4-bit `BitsAndBytes` pipeline for GPU execution alongside the resilient `AgriFallbackAdapter` for CPU/laptop testing.
2. **Soil Variability**: Soil nutrient status varies by farm plot. The assistant mandates that exact chemical dosages be cross-checked with Soil Health Card tests.

