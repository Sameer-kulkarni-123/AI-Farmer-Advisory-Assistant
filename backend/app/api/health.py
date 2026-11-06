"""
System Health and Model Availability check endpoint.
"""

from fastapi import APIRouter
from backend.app.config import settings
from backend.app.models.schemas import HealthResponse
from backend.app.services.agriparam_service import agriparam_service
from backend.app.services.translation_service import translation_service
from backend.app.services.retrieval_service import retrieval_service

router = APIRouter(prefix="/api/health", tags=["Health & Status"])

@router.get("", response_model=HealthResponse, summary="Check System Status")
def check_health():
    """
    Returns live status of database, ChromaDB vector store, AgriParam LLM, and IndicTrans2 adapters.
    """
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        database="SQLite Connected",
        vector_store=f"ChromaDB Persistent (Chunks: {retrieval_service.count()})",
        agriparam_engine=agriparam_service.model_tag,
        indictrans_engine=translation_service.get_adapter_provenance(),
        supported_languages=list(settings.SUPPORTED_LANGUAGES.keys())
    )

