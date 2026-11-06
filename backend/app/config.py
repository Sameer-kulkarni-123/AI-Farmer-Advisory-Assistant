"""
Application Configuration for AI Farmer Advisory Assistant.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "AI Farmer Advisory Assistant"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # API Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{BASE_DIR / 'farmer_assistant.db'}"
    )

    # Vector Database & Paths
    VECTOR_DB_DIR: str = str(BASE_DIR / "vector_store" / "chroma_db")
    DOCUMENTS_DIR: str = str(BASE_DIR / "knowledge_base" / "documents")
    METADATA_DIR: str = str(BASE_DIR / "knowledge_base" / "metadata")
    PROCESSED_DIR: str = str(BASE_DIR / "knowledge_base" / "processed")
    DATASET_DIR: str = str(BASE_DIR / "dataset")
    RESULTS_DIR: str = str(BASE_DIR / "results")

    # Embeddings
    EMBEDDING_MODEL_NAME: str = os.getenv(
        "EMBEDDING_MODEL_NAME", 
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    EMBEDDING_DIMENSION: int = 384
    CHUNK_SIZE: int = 450
    CHUNK_OVERLAP: int = 80
    RETRIEVAL_TOP_K: int = 4
    SIMILARITY_THRESHOLD: float = 0.10

    # BharatGen AgriParam LLM Settings
    AGRIPARAM_MODEL_ID: str = os.getenv("AGRIPARAM_MODEL_ID", "bharatgenai/AgriParam")
    # Inference mode: "local_gpu_4bit", "local_cpu", "hosted_api", or "fallback"
    INFERENCE_MODE: str = os.getenv("INFERENCE_MODE", "fallback")
    LOAD_IN_4BIT: bool = os.getenv("LOAD_IN_4BIT", "true").lower() == "true"
    MAX_NEW_TOKENS: int = 650
    TEMPERATURE: float = 0.2

    # AI4Bharat IndicTrans2 Settings
    INDICTRANS2_INDIC_EN: str = os.getenv("INDICTRANS2_INDIC_EN", "ai4bharat/indictrans2-indic-en-1B")
    INDICTRANS2_EN_INDIC: str = os.getenv("INDICTRANS2_EN_INDIC", "ai4bharat/indictrans2-en-indic-1B")
    # Translation mode: "indictrans2_local", "hosted_api", or "agricultural_translator"
    TRANSLATION_MODE: str = os.getenv("TRANSLATION_MODE", "agricultural_translator")

    # Supported Indian Languages
    SUPPORTED_LANGUAGES: dict = {
        "en": {"name": "English", "native": "English", "code": "en", "indictrans_code": "eng_Latn"},
        "hi": {"name": "Hindi", "native": "हिन्दी", "code": "hi", "indictrans_code": "hin_Deva"},
        "kn": {"name": "Kannada", "native": "ಕನ್ನಡ", "code": "kn", "indictrans_code": "kan_Knda"},
        "ta": {"name": "Tamil", "native": "தமிழ்", "code": "ta", "indictrans_code": "tam_Taml"},
        "te": {"name": "Telugu", "native": "తెలుగు", "code": "te", "indictrans_code": "tel_Telu"},
        "bn": {"name": "Bengali", "native": "বাংলা", "code": "bn", "indictrans_code": "ben_Beng"},
        "mr": {"name": "Marathi", "native": "मराठी", "code": "mr", "indictrans_code": "mar_Deva"}
    }

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
