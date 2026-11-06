"""
Document Ingestion Pipeline: loads ICAR/KVK documents, chunks, embeds, and indexes them.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List

from backend.app.config import settings
from backend.app.core.logging import logger
from backend.app.utils.text_processing import chunk_text
from backend.app.services.retrieval_service import retrieval_service
from backend.app.models.database import SessionLocal
from backend.app.models.source import SourceDocument

class DocumentIngestionService:
    def __init__(self):
        self.docs_dir = Path(settings.DOCUMENTS_DIR)

    def ingest_all_documents(self, rebuild: bool = False) -> Dict[str, Any]:
        """
        Ingest all JSON documents from knowledge_base/documents/ into ChromaDB and SQLite.
        """
        if not self.docs_dir.exists():
            raise FileNotFoundError(f"Documents directory {self.docs_dir} not found.")

        if rebuild:
            logger.info("Rebuilding knowledge base: resetting vector collection...")
            retrieval_service.reset_collection()

        doc_files = list(self.docs_dir.glob("*.json"))
        logger.info(f"Found {len(doc_files)} knowledge base documents to ingest.")

        db = SessionLocal()
        all_chunks = []
        ingested_docs = 0

        try:
            for file_path in doc_files:
                with open(file_path, "r", encoding="utf-8") as f:
                    doc = json.load(f)

                doc_id = doc.get("document_id")
                title = doc.get("title")
                source = doc.get("source")
                source_url = doc.get("source_url", "")
                crop = doc.get("crop", "All Crops")
                category = doc.get("category", "cultivation")
                region = doc.get("region", "India")
                language = doc.get("language", "English")
                verified = doc.get("verified", True)
                content = doc.get("content", "")

                # Chunk document
                chunks = chunk_text(content, chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP)

                # Store chunks metadata for ChromaDB
                for idx, c_text in enumerate(chunks):
                    chunk_id = f"{doc_id}_chunk_{idx}"
                    all_chunks.append({
                        "id": chunk_id,
                        "text": c_text,
                        "metadata": {
                            "document_id": doc_id,
                            "title": title,
                            "source": source,
                            "source_url": source_url,
                            "crop": crop,
                            "category": category,
                            "region": region,
                            "language": language,
                            "chunk_index": idx
                        }
                    })

                # Upsert into SQLite source_documents
                existing_doc = db.query(SourceDocument).filter(SourceDocument.document_id == doc_id).first()
                if existing_doc:
                    existing_doc.title = title
                    existing_doc.source = source
                    existing_doc.source_url = source_url
                    existing_doc.crop = crop
                    existing_doc.category = category
                    existing_doc.region = region
                    existing_doc.language = language
                    existing_doc.verified = verified
                    existing_doc.chunk_count = len(chunks)
                    existing_doc.content = content
                else:
                    new_doc = SourceDocument(
                        document_id=doc_id,
                        title=title,
                        source=source,
                        source_url=source_url,
                        crop=crop,
                        category=category,
                        region=region,
                        language=language,
                        verified=verified,
                        chunk_count=len(chunks),
                        content=content
                    )
                    db.add(new_doc)
                ingested_docs += 1

            db.commit()

            # Add chunks to Vector Database
            retrieval_service.add_chunks(all_chunks)

            result = {
                "status": "success",
                "documents_ingested": ingested_docs,
                "total_chunks_indexed": len(all_chunks),
                "collection_count": retrieval_service.count()
            }
            logger.info(f"Ingestion complete: {result}")
            return result

        except Exception as e:
            db.rollback()
            logger.error(f"Failed during document ingestion: {e}")
            raise
        finally:
            db.close()

ingestion_service = DocumentIngestionService()

