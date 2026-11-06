"""
Knowledge Sources API: lists and details official Indian agricultural reference documents.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.app.models.database import get_db
from backend.app.models.source import SourceDocument
from backend.app.models.schemas import SourceItem

router = APIRouter(prefix="/api/sources", tags=["Knowledge Sources"])

@router.get("", response_model=List[SourceItem], summary="List Agricultural Knowledge Sources")
def get_sources(
    crop: Optional[str] = Query(None, description="Filter by crop"),
    category: Optional[str] = Query(None, description="Filter by category"),
    verified_only: bool = Query(True, description="Filter verified ICAR/KVK documents"),
    db: Session = Depends(get_db)
):
    query = db.query(SourceDocument)
    if crop:
        query = query.filter(SourceDocument.crop.ilike(f"%{crop}%"))
    if category:
        query = query.filter(SourceDocument.category == category)
    if verified_only:
        query = query.filter(SourceDocument.verified == True)

    docs = query.order_by(SourceDocument.crop).all()
    result = []
    for d in docs:
        result.append(SourceItem(
            document_id=d.document_id,
            title=d.title,
            source=d.source,
            source_url=d.source_url,
            crop=d.crop,
            category=d.category,
            region=d.region,
            language=d.language,
            verified=d.verified,
            chunk_count=d.chunk_count,
            content_preview=d.content[:240] + "..." if d.content else None
        ))
    return result

@router.get("/{source_id}", response_model=SourceItem, summary="Get Document Details")
def get_source_by_id(source_id: str, db: Session = Depends(get_db)):
    doc = db.query(SourceDocument).filter(SourceDocument.document_id == source_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source document '{source_id}' not found in knowledge base."
        )
    return SourceItem(
        document_id=doc.document_id,
        title=doc.title,
        source=doc.source,
        source_url=doc.source_url,
        crop=doc.crop,
        category=doc.category,
        region=doc.region,
        language=doc.language,
        verified=doc.verified,
        chunk_count=doc.chunk_count,
        content_preview=doc.content
    )

