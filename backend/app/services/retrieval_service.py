"""
Vector Database and Retrieval Service using ChromaDB with metadata filtering.
"""

import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings

from backend.app.config import settings
from backend.app.core.logging import logger
from backend.app.services.embedding_service import embedding_service

class RetrievalService:
    def __init__(self):
        self.db_dir = Path(settings.VECTOR_DB_DIR)
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.collection_name = "farmer_knowledge_base"
        self._init_chroma()

    def _init_chroma(self):
        """Initialize persistent ChromaDB client and collection with cosine space."""
        try:
            self.client = chromadb.PersistentClient(path=str(self.db_dir))
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine", "description": "ICAR and KVK Agricultural Knowledge Base"}
            )
            logger.info(f"ChromaDB initialized. Existing chunks in collection: {self.collection.count()}")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise

    def count(self) -> int:
        return self.collection.count()

    def reset_collection(self):
        """Delete and recreate the collection for fresh ingestion."""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine", "description": "ICAR and KVK Agricultural Knowledge Base"}
            )
            logger.info("ChromaDB collection reset successfully.")
        except Exception as e:
            logger.error(f"Error resetting collection: {e}")

    def add_chunks(self, chunks: List[Dict[str, Any]]):
        """
        Batch add document chunks to ChromaDB.
        Each chunk dict must have: id, text, metadata (doc_id, title, crop, category, region, source_url)
        """
        if not chunks:
            return

        ids = [c["id"] for c in chunks]
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]

        # Generate embeddings
        embeddings = embedding_service.get_embeddings(texts)

        # Chroma batch insert (in chunks of 100)
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            end = i + batch_size
            self.collection.upsert(
                ids=ids[i:end],
                embeddings=embeddings[i:end],
                documents=texts[i:end],
                metadatas=metadatas[i:end]
            )
        logger.info(f"Upserted {len(ids)} chunks to ChromaDB. Total chunks: {self.collection.count()}")

    def search(
        self,
        query: str,
        top_k: int = 4,
        crop_filter: Optional[str] = None,
        category_filter: Optional[str] = None,
        region_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Semantic vector search with resilient multi-tier metadata filtering and ranking.
        """
        if not query.strip():
            return []

        query_embedding = embedding_service.get_embedding(query)

        # 1. First attempt: specific crop if present
        where_clause = None
        if crop_filter and crop_filter.lower() not in ["all", "all crops", "unspecified"]:
            where_clause = {
                "$or": [
                    {"crop": {"$eq": crop_filter}},
                    {"crop": {"$eq": "All Crops"}},
                    {"crop": {"$eq": "Multiple Crops"}}
                ]
            }

        results = None
        if where_clause:
            try:
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    where=where_clause
                )
            except Exception as e:
                logger.warning(f"Chroma filtered search failed ({e}), falling back to global query.")
                results = None

        # 2. If filtered query returns empty or not used, query globally
        if not results or not results.get("ids") or len(results["ids"][0]) == 0:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

        retrieved_docs = []
        if results and results.get("ids") and len(results["ids"]) > 0:
            doc_ids = results["ids"][0]
            texts = results["documents"][0] if results.get("documents") else []
            metadatas = results["metadatas"][0] if results.get("metadatas") else []
            distances = results["distances"][0] if results.get("distances") else []

            for i in range(len(doc_ids)):
                dist = distances[i] if i < len(distances) else 1.0
                # In cosine space, cosine_sim = 1.0 - dist
                similarity = max(0.0, min(1.0, 1.0 - dist))

                retrieved_docs.append({
                    "chunk_id": doc_ids[i],
                    "text": texts[i] if i < len(texts) else "",
                    "metadata": metadatas[i] if i < len(metadatas) else {},
                    "similarity": similarity
                })

        return retrieved_docs

# Global singleton
retrieval_service = RetrievalService()
