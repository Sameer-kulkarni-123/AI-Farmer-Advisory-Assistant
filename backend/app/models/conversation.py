"""
SQLAlchemy models for Conversations, Messages, and Citations.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Float, Boolean, JSON
from sqlalchemy.orm import relationship
from backend.app.models.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, default="New Farming Advisory")
    language = Column(String(10), default="en")
    crop = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")

class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False) # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    language = Column(String(10), default="en")
    translated_content = Column(Text, nullable=True)
    
    # Structured response components (for assistant responses)
    recommendation = Column(Text, nullable=True)
    why_recommended = Column(Text, nullable=True)
    practical_steps = Column(JSON, nullable=True) # list of strings
    precautions = Column(JSON, nullable=True) # list of strings
    regional_notes = Column(Text, nullable=True)
    evidence_level = Column(String(30), default="Strong")
    model_used = Column(String(100), default="AgriParam")
    latency_seconds = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    conversation = relationship("Conversation", back_populates="messages")
    citations = relationship("CitationRecord", back_populates="message", cascade="all, delete-orphan")

class CitationRecord(Base):
    __tablename__ = "citations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    message_id = Column(String(36), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    document_id = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    source = Column(String(255), nullable=False)
    source_url = Column(String(500), nullable=True)
    crop = Column(String(100), nullable=True)
    category = Column(String(100), nullable=True)
    similarity_score = Column(Float, nullable=True)

    message = relationship("Message", back_populates="citations")

