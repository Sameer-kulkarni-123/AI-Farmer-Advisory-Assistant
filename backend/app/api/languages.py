"""
Languages API endpoint: lists actually configured and supported languages.
"""

from typing import List
from fastapi import APIRouter
from backend.app.config import settings
from backend.app.models.schemas import LanguageItem

router = APIRouter(prefix="/api/languages", tags=["Languages"])

@router.get("", response_model=List[LanguageItem], summary="List Supported Indian Languages")
def get_supported_languages():
    """
    Returns the exact set of languages supported by the translation and advisory pipeline.
    """
    result = []
    for code, info in settings.SUPPORTED_LANGUAGES.items():
        result.append(LanguageItem(
            code=code,
            name=info["name"],
            native=info["native"],
            indictrans_code=info["indictrans_code"],
            status="Active"
        ))
    return result

