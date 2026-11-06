"""
Chat API Endpoint: processes agricultural questions with RAG grounding.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.models.database import get_db
from backend.app.models.schemas import ChatRequest, ChatResponse
from backend.app.services.rag_service import rag_service
from backend.app.core.logging import logger

router = APIRouter(prefix="/api/chat", tags=["Chat Advisory"])

@router.post("", response_model=ChatResponse, summary="Submit Agricultural Query")
def post_chat_query(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Submit an agricultural question in any supported Indian language or English.
    Returns an evidence-grounded structured advisory with citations and confidence level.
    """
    try:
        result = rag_service.process_query(
            query=request.message,
            db=db,
            conversation_id=request.conversation_id,
            language=request.language,
            crop=request.crop,
            region=request.region,
            soil_type=request.soil_type,
            growth_stage=request.growth_stage
        )
        return result
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate agricultural advisory: {str(e)}"
        )

