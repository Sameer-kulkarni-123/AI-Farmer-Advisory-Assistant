"""
Dedicated Advisory Service for structured Crop-State-Soil-Stage queries.
"""

import time
from typing import Dict, Any
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.services.rag_service import rag_service

class AdvisoryService:
    def get_crop_advisory(
        self,
        crop: str,
        category: str,
        state: str,
        district: str,
        soil_type: str,
        growth_stage: str,
        language: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        Generate structured crop advisory filtered by crop, soil, and growth stage.
        """
        start = time.perf_counter()

        query_intent = (
            f"Provide official ICAR recommended {category} advisory for {crop} "
            f"in {state} ({district or 'General District'}) with {soil_type} soil at {growth_stage} growth stage."
        )

        rag_response = rag_service.process_query(
            query=query_intent,
            db=db,
            conversation_id=None,
            language=language,
            crop=crop,
            region=state,
            soil_type=soil_type,
            growth_stage=growth_stage
        )

        latency = time.perf_counter() - start

        return {
            "crop": crop,
            "state": state,
            "soil_type": soil_type,
            "growth_stage": growth_stage,
            "advisory": rag_response["advisory"],
            "model_used": rag_response["model_used"],
            "latency_seconds": round(latency, 3)
        }

advisory_service = AdvisoryService()

