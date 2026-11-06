"""
SQLAlchemy model for Agricultural Knowledge Sources.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer
from backend.app.models.database import Base

class SourceDocument(Base):
    __tablename__ = "source_documents"

    document_id = Column(String(100), primary_key=True)
    title = Column(String(255), nullable=False)
    source = Column(String(255), nullable=False)
    source_url = Column(String(500), nullable=True)
    crop = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    region = Column(String(200), default="India")
    language = Column(String(20), default="English")
    verified = Column(Boolean, default=True)
    chunk_count = Column(Integer, default=1)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

