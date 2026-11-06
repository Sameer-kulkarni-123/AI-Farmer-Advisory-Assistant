"""
CLI Ingestion Script: Populates ChromaDB and SQLite with ICAR/KVK documents.
Supports --rebuild flag.
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from backend.app.models.database import init_db
from backend.app.services.document_ingestion import ingestion_service

def main():
    parser = argparse.ArgumentParser(description="Ingest agricultural documents into Vector DB and SQLite.")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the vector store from scratch.")
    args = parser.parse_args()

    print("==========================================================")
    print("AI FARMER ADVISORY - AGRICULTURAL KNOWLEDGE INGESTION")
    print("==========================================================")
    print(f"Rebuild Flag: {args.rebuild}")

    init_db()
    result = ingestion_service.ingest_all_documents(rebuild=args.rebuild)

    print("\nIngestion Summary:")
    print(f"- Status: {result['status']}")
    print(f"- Documents Processed: {result['documents_ingested']}")
    print(f"- Overlapping Chunks Indexed: {result['total_chunks_indexed']}")
    print(f"- Total Vector Collection Size: {result['collection_count']}")
    print("==========================================================")

if __name__ == "__main__":
    main()

