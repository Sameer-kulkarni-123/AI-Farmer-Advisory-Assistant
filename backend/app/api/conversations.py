"""
Conversations API: manage previous chat sessions and retrieve full history.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.models.database import get_db
from backend.app.models.conversation import Conversation, Message
from backend.app.models.schemas import ConversationSummary, ConversationDetail, MessageDetail, CitationItem

router = APIRouter(prefix="/api/conversations", tags=["Conversations History"])

@router.get("", response_model=List[ConversationSummary], summary="List Past Sessions")
def list_conversations(db: Session = Depends(get_db)):
    convs = db.query(Conversation).order_by(Conversation.updated_at.desc()).all()
    results = []
    for c in convs:
        count = db.query(Message).filter(Message.conversation_id == c.id).count()
        results.append(ConversationSummary(
            id=c.id,
            title=c.title,
            language=c.language,
            crop=c.crop,
            region=c.region,
            message_count=count,
            created_at=c.created_at,
            updated_at=c.updated_at
        ))
    return results

@router.get("/{conversation_id}", response_model=ConversationDetail, summary="Get Session Transcript")
def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()
    msg_details = []
    for m in messages:
        citations = []
        if m.role == "assistant":
            for c in m.citations:
                citations.append(CitationItem(
                    document_id=c.document_id,
                    title=c.title,
                    source=c.source,
                    source_url=c.source_url,
                    crop=c.crop,
                    category=c.category,
                    similarity_score=c.similarity_score
                ))

        msg_details.append(MessageDetail(
            id=m.id,
            role=m.role,
            content=m.content,
            language=m.language,
            recommendation=m.recommendation,
            why_recommended=m.why_recommended,
            practical_steps=m.practical_steps or [],
            precautions=m.precautions or [],
            regional_notes=m.regional_notes,
            evidence_level=m.evidence_level,
            model_used=m.model_used,
            created_at=m.created_at,
            citations=citations
        ))

    return ConversationDetail(
        id=conv.id,
        title=conv.title,
        language=conv.language,
        crop=conv.crop,
        region=conv.region,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        messages=msg_details
    )

@router.delete("/{conversation_id}", summary="Delete Conversation")
def delete_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    db.delete(conv)
    db.commit()
    return {"status": "success", "message": f"Conversation '{conversation_id}' deleted."}

