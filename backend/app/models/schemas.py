"""
Pydantic Request and Response Schemas for API validation.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class CitationItem(BaseModel):
    document_id: str
    title: str
    source: str
    source_url: Optional[str] = None
    crop: Optional[str] = None
    category: Optional[str] = None
    similarity_score: Optional[float] = None
    excerpt: Optional[str] = None

class StructuredAdvisory(BaseModel):
    crop: Optional[str] = None
    topic: Optional[str] = None
    recommendation: str = Field(..., description="Core agricultural recommendation")
    why_recommended: str = Field(..., description="Evidence-backed reasoning")
    practical_steps: List[str] = Field(default_factory=list, description="Step-by-step actionable advice")
    important_precautions: List[str] = Field(default_factory=list, description="Warnings, soil, or chemical safety guidelines")
    regional_considerations: Optional[str] = Field(None, description="Agro-climatic and regional nuances")
    sources: List[CitationItem] = Field(default_factory=list, description="Authoritative reference sources")
    confidence_level: str = Field("Strong", description="'Strong', 'Limited', or 'Insufficient'")
    disclaimer: str = Field(
        "Advisory based on verified ICAR/KVK guidance. Consult your local Krishi Vigyan Kendra (KVK) for farm-specific confirmation.",
        description="Standard safety disclaimer"
    )

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Farmer's agricultural query")
    conversation_id: Optional[str] = Field(None, description="Optional existing conversation UUID")
    language: Optional[str] = Field("en", description="Target language code (e.g., 'en', 'hi', 'kn', 'ta', 'te', 'bn', 'mr')")
    crop: Optional[str] = Field(None, description="Crop context (e.g., 'Rice', 'Wheat', 'Cotton')")
    region: Optional[str] = Field(None, description="State or agro-climatic region (e.g., 'Karnataka', 'Punjab')")
    soil_type: Optional[str] = Field(None, description="Soil type (e.g., 'Black Soil', 'Red Loam')")
    growth_stage: Optional[str] = Field(None, description="Crop growth stage (e.g., 'Vegetative', 'Flowering')")

class ChatResponse(BaseModel):
    conversation_id: str
    message_id: str
    language: str
    user_query: str
    translated_query: Optional[str] = None
    advisory: StructuredAdvisory
    model_used: str
    latency_seconds: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AdvisoryRequest(BaseModel):
    crop: str = Field(..., description="Crop name (e.g., 'Rice', 'Wheat', 'Maize', 'Cotton', 'Tomato')")
    category: Optional[str] = Field("cultivation", description="Category: 'cultivation', 'irrigation', 'fertilizer', 'pest_management'")
    state: Optional[str] = Field("All-India", description="State or region")
    district: Optional[str] = Field(None, description="District")
    soil_type: Optional[str] = Field("All", description="Soil type")
    growth_stage: Optional[str] = Field("All", description="Growth stage")
    language: Optional[str] = Field("en", description="Preferred output language")

class AdvisoryResponse(BaseModel):
    crop: str
    state: Optional[str]
    soil_type: Optional[str]
    growth_stage: Optional[str]
    advisory: StructuredAdvisory
    model_used: str
    latency_seconds: float

class LanguageItem(BaseModel):
    code: str
    name: str
    native: str
    indictrans_code: str
    status: str = "Active"

class SourceItem(BaseModel):
    document_id: str
    title: str
    source: str
    source_url: Optional[str] = None
    crop: str
    category: str
    region: str
    language: str
    verified: bool
    chunk_count: int = 1
    content_preview: Optional[str] = None

class MessageDetail(BaseModel):
    id: str
    role: str
    content: str
    language: str
    recommendation: Optional[str] = None
    why_recommended: Optional[str] = None
    practical_steps: Optional[List[str]] = None
    precautions: Optional[List[str]] = None
    regional_notes: Optional[str] = None
    evidence_level: Optional[str] = None
    model_used: Optional[str] = None
    created_at: datetime
    citations: List[CitationItem] = []

class ConversationSummary(BaseModel):
    id: str
    title: str
    language: str
    crop: Optional[str] = None
    region: Optional[str] = None
    message_count: int = 0
    created_at: datetime
    updated_at: datetime

class ConversationDetail(BaseModel):
    id: str
    title: str
    language: str
    crop: Optional[str] = None
    region: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    messages: List[MessageDetail] = []

class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    database: str
    vector_store: str
    agriparam_engine: str
    indictrans_engine: str
    supported_languages: List[str]

