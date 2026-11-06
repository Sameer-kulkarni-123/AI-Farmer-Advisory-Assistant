"""
Custom Domain Exceptions for AI Farmer Advisory.
"""

from fastapi import HTTPException, status

class AgriculturalAdvisoryException(Exception):
    """Base exception for agricultural advisory errors."""
    def __init__(self, message: str, code: str = "ADVISORY_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class InsufficientEvidenceException(AgriculturalAdvisoryException):
    """Raised when retrieved agricultural sources cannot verify the advisory."""
    def __init__(self, message: str = "Insufficient official evidence found to safely answer this query."):
        super().__init__(message, code="INSUFFICIENT_EVIDENCE")

class UnsupportedLanguageException(AgriculturalAdvisoryException):
    """Raised when the requested language is outside the supported IndicTrans2 set."""
    def __init__(self, lang_code: str):
        super().__init__(f"Language '{lang_code}' is currently not supported.", code="UNSUPPORTED_LANGUAGE")

class ModelInferenceException(AgriculturalAdvisoryException):
    """Raised when AgriParam or IndicTrans2 inference fails."""
    def __init__(self, model_name: str, reason: str):
        super().__init__(f"Inference error in model '{model_name}': {reason}", code="MODEL_INFERENCE_ERROR")

class MissingContextException(AgriculturalAdvisoryException):
    """Raised when crucial context (crop, soil, stage) is missing for safety-critical advice."""
    def __init__(self, missing_fields: list):
        fields_str = ", ".join(missing_fields)
        super().__init__(f"Crucial agricultural context missing: {fields_str}", code="MISSING_CONTEXT")

