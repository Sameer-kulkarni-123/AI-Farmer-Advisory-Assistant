"""
Retrieval-Augmented Generation (RAG) Service for Indian Agriculture.
Coordinates query processing, translation, vector retrieval, AgriParam generation, and persistence.
"""

import time
import uuid
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.core.logging import logger, log_execution_time
from backend.app.utils.validators import check_banned_chemicals, sanitize_farmer_query
from backend.app.utils.text_processing import detect_crop, detect_category
from backend.app.services.language_detection import language_detector
from backend.app.services.translation_service import translation_service
from backend.app.services.retrieval_service import retrieval_service
from backend.app.services.agriparam_service import agriparam_service
from backend.app.models.conversation import Conversation, Message, CitationRecord

class RAGService:
    @log_execution_time("RAG_Advisory_Pipeline")
    def process_query(
        self,
        query: str,
        db: Session,
        conversation_id: Optional[str] = None,
        language: Optional[str] = None,
        crop: Optional[str] = None,
        region: Optional[str] = None,
        soil_type: Optional[str] = None,
        growth_stage: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute full RAG pipeline for farmer query.
        """
        start_time = time.perf_counter()

        # 1. Sanitize user query
        clean_query = sanitize_farmer_query(query)

        # 2. Safety filter: Check for banned agrochemicals
        has_banned, banned_list = check_banned_chemicals(clean_query)
        if has_banned:
            banned_names = ", ".join([b.capitalize() for b in banned_list])
            warning_msg = (
                f"NOTICE: {banned_names} is banned or strictly restricted under the Insecticides Act 1968 / CIBRC "
                f"regulations due to high human and environmental toxicity. The assistant will not provide recommendations for banned chemicals."
            )
            logger.warning(f"Banned chemical query detected: {banned_list}")
            # Inject safety context or abstain immediately

        # 3. Language detection & translation
        detected_lang, conf = language_detector.detect_language(clean_query)
        target_lang = language if language and language in settings.SUPPORTED_LANGUAGES else detected_lang

        translated_query = clean_query
        if target_lang != "en":
            translated_query = translation_service.translate_query_to_english(clean_query, target_lang)

        # 4. Context entity detection
        detected_crop_val = crop if crop and crop.lower() != "all" else detect_crop(translated_query)
        detected_cat_val = detect_category(translated_query)

        # 5. Semantic Vector Retrieval
        logger.info(f"Retrieving evidence for crop='{detected_crop_val}', category='{detected_cat_val}'...")
        retrieved_chunks = retrieval_service.search(
            query=translated_query,
            top_k=settings.RETRIEVAL_TOP_K,
            crop_filter=detected_crop_val if detected_crop_val != "All" else None,
            category_filter=detected_cat_val if detected_cat_val != "cultivation" else None,
            region_filter=region
        )

        logger.info(f"Retrieved {len(retrieved_chunks)} relevant chunks from ChromaDB.")

        # 6. AgriParam Generation / Grounded Engine
        advisory_result = agriparam_service.generate_advisory(
            query=translated_query,
            retrieved_chunks=retrieved_chunks,
            crop=detected_crop_val,
            region=region,
            soil_type=soil_type,
            growth_stage=growth_stage
        )

        # If banned chemical was in question, append precaution
        if has_banned:
            advisory_result["important_precautions"].insert(
                0,
                f"ALERT: The mentioned chemical ({', '.join(banned_list)}) is banned in India by CIBRC. Use authorized bio-pesticides or recommended IPM alternatives instead."
            )
            advisory_result["confidence_level"] = "Limited"

        # 7. Response translation to farmer's selected language
        if target_lang != "en":
            advisory_result = translation_service.translate_advisory(advisory_result, target_lang)

        latency = time.perf_counter() - start_time

        # 8. Database Persistence (Conversations & Messages)
        conv_id = conversation_id
        if not conv_id:
            # Create new conversation
            new_conv = Conversation(
                id=str(uuid.uuid4()),
                title=clean_query[:60] + ("..." if len(clean_query) > 60 else ""),
                language=target_lang,
                crop=detected_crop_val if detected_crop_val != "All" else None,
                region=region
            )
            db.add(new_conv)
            db.commit()
            conv_id = new_conv.id
        else:
            existing_conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
            if existing_conv:
                existing_conv.language = target_lang

        # Save user message
        user_msg = Message(
            id=str(uuid.uuid4()),
            conversation_id=conv_id,
            role="user",
            content=clean_query,
            language=target_lang,
            translated_content=translated_query if target_lang != "en" else None
        )
        db.add(user_msg)

        # Save assistant message
        asst_msg_id = str(uuid.uuid4())
        asst_msg = Message(
            id=asst_msg_id,
            conversation_id=conv_id,
            role="assistant",
            content=advisory_result.get("recommendation", ""),
            language=target_lang,
            recommendation=advisory_result.get("recommendation"),
            why_recommended=advisory_result.get("why_recommended"),
            practical_steps=advisory_result.get("practical_steps", []),
            precautions=advisory_result.get("important_precautions", []),
            regional_notes=advisory_result.get("regional_considerations"),
            evidence_level=advisory_result.get("confidence_level", "Strong"),
            model_used=advisory_result.get("model_used", "AgriParam"),
            latency_seconds=round(latency, 3)
        )
        db.add(asst_msg)

        # Save citations
        for src in advisory_result.get("sources", []):
            cit = CitationRecord(
                id=str(uuid.uuid4()),
                message_id=asst_msg_id,
                document_id=src.get("document_id", "unknown"),
                title=src.get("title", ""),
                source=src.get("source", ""),
                source_url=src.get("source_url"),
                crop=src.get("crop"),
                category=src.get("category"),
                similarity_score=src.get("similarity_score")
            )
            db.add(cit)

        db.commit()

        return {
            "conversation_id": conv_id,
            "message_id": asst_msg_id,
            "language": target_lang,
            "user_query": clean_query,
            "translated_query": translated_query if target_lang != "en" else None,
            "advisory": advisory_result,
            "model_used": advisory_result.get("model_used", "AgriParam"),
            "latency_seconds": round(latency, 3)
        }

rag_service = RAGService()

