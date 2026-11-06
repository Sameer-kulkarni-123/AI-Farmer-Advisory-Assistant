# System Architecture — AI Farmer Advisory Assistant

## 1. High-Level Architectural Overview

The **AI Farmer Advisory Assistant (Krishi Mitra AI)** is an evidence-grounded, multilingual agricultural reasoning platform designed for Indian farmers, extension workers, and students. It integrates domain-specialized LLMs (**BharatGen AgriParam**), sequence-to-sequence translation (**AI4Bharat IndicTrans2**), and persistent vector retrieval (**ChromaDB**) grounded on official Indian agricultural repositories (**ICAR**, **KVK**, and **DAC&FW**).

```mermaid
graph TD
    User["👨‍🌾 Indian Farmer / Extension Worker"]
    Frontend["⚛️ React + Vite + Tailwind Frontend<br/>(Dashboard, Chat, Crop Advisory, Sources, History)"]
    FastAPI["🚀 FastAPI Backend Application<br/>(Pydantic, REST API, Async Handlers)"]

    LangDetect["🔤 Language Detection<br/>(Unicode Block & Morphology Heuristics)"]
    IndicTrans["🇮🇳 AI4Bharat IndicTrans2 Adapter<br/>(Indic-to-English & English-to-Indic)"]
    
    RAGCore["🧠 RAG Coordinator Service"]
    Retriever["🔍 ChromaDB Vector Engine<br/>(Persistent Cosine Similarity Space)"]
    KnowledgeBase[("📚 ICAR & KVK Knowledge Base<br/>(20 Official Packages of Practices)")]
    
    AgriParam["🌱 BharatGen AgriParam LLM<br/>(4-bit NF4 GPU / CPU Offload / Grounded Adapter)"]
    SafetyRules["🛡️ Agricultural Safety Guardrails<br/>(Banned Agrochem Check, Dosage Safeguard, KVK Referral)"]
    
    SQLite[("💾 SQLite Relational Database<br/>(Conversations, Transcripts, Sources, Citations)")]

    User <-->|HTTP / JSON (REST)| Frontend
    Frontend <-->|REST API Endpoints| FastAPI
    
    FastAPI --> LangDetect
    LangDetect --> IndicTrans
    IndicTrans --> RAGCore
    
    RAGCore --> Retriever
    Retriever <--> KnowledgeBase
    Retriever --> RAGCore
    
    RAGCore --> SafetyRules
    SafetyRules --> AgriParam
    AgriParam --> RAGCore
    
    RAGCore --> IndicTrans
    RAGCore --> SQLite
    FastAPI <--> SQLite
```

---

## 2. Component Specifications

### 2.1 Frontend Architecture (React 18 + Vite)
- **Framework:** React 18, Vite 6, Tailwind CSS 3.4.
- **Pages:**
  1. `Dashboard.jsx`: Executive summary, quick question bar, domain taxonomies, and recent conversation logs.
  2. `ChatAssistant.jsx`: Full conversational assistant with multi-turn context, speech suggestions, language toggles, and structured advisory cards.
  3. `CropAdvisoryPage.jsx`: Filter matrix (Crop, State, District, Soil Type, Growth Stage, Category) generating calibrated advisories.
  4. `KnowledgeSources.jsx`: Searchable explorer of official ICAR/KVK reference documents with passage inspector.
  5. `ConversationHistory.jsx`: Persistent transcript viewer with session continuation and deletion.
- **Client Services:** Axios API client configured to proxy `http://127.0.0.1:8000`.

### 2.2 Backend Architecture (FastAPI + SQLAlchemy)
- **Router Modules (`app/api/`):**
  - `chat.py`: `POST /api/chat` for free-form multilingual questions.
  - `advisory.py`: `POST /api/advisory` for structured crop queries.
  - `languages.py`: `GET /api/languages` reporting verified language coverage.
  - `sources.py`: `GET /api/sources` and `GET /api/sources/{id}` for document inspection.
  - `conversations.py`: `GET /api/conversations`, `GET /api/conversations/{id}`, `DELETE /api/conversations/{id}`.
  - `health.py`: `GET /api/health` reporting live engine status.
- **Database (`app/models/`):** SQLite (`farmer_assistant.db`) managing relational models: `Conversation`, `Message`, `CitationRecord`, and `SourceDocument`.

### 2.3 RAG Pipeline & Vector Indexing
- **Storage:** Persistent ChromaDB at `vector_store/chroma_db` using cosine distance space (`hnsw:space: cosine`).
- **Embedding Service:** 384-dimensional multilingual vector representation supporting SentenceTransformers (`paraphrase-multilingual-MiniLM-L12-v2`) and deterministic agricultural domain-weighted TF-IDF projection.
- **Grounding & Abstention:** Strict thresholding (`SIMILARITY_THRESHOLD = 0.10 - 0.20`). Non-agricultural queries (space, crypto, financial derivatives) or undocumented crop-climate queries trigger explicit abstention instead of ungrounded extrapolation.

