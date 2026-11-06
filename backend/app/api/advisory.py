"""
Structured Crop Advisory API endpoint.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.models.database import get_db
from backend.app.models.schemas import AdvisoryRequest, AdvisoryResponse
from backend.app.services.advisory_service import advisory_service

router = APIRouter(prefix="/api/advisory", tags=["Crop Advisory"])

@router.post("", response_model=AdvisoryResponse, summary="Get Structured Crop Guidance")
def post_crop_advisory(req: AdvisoryRequest, db: Session = Depends(get_db)):
    """
    Retrieve structured guidance filtered by crop, state, soil type, and growth stage.
    """
    try:
        return advisory_service.get_crop_advisory(
            crop=req.crop,
            category=req.category or "cultivation",
            state=req.state or "All-India",
            district=req.district or "",
            soil_type=req.soil_type or "All",
            growth_stage=req.growth_stage or "All",
            language=req.language or "en",
            db=db
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate structured crop advisory: {str(e)}"
        )

