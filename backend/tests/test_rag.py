"""
Unit Tests for RAG pipeline components, embedding projection, and safety guardrails.
"""

from backend.app.services.retrieval_service import retrieval_service
from backend.app.utils.validators import check_banned_chemicals, sanitize_farmer_query
from backend.app.utils.text_processing import detect_crop, detect_category, chunk_text
from backend.app.services.agriparam_service import agriparam_service

def test_crop_detection():
    assert detect_crop("What is the seed rate for paddy?") == "Rice"
    assert detect_crop("How to manage pink bollworm in cotton?") == "Cotton"
    assert detect_crop("When to apply gypsum to groundnut?") == "Groundnut"
    assert detect_crop("Wheat rust prevention tips") == "Wheat"
    assert detect_crop("Tell me about farming in rainy season") == "All"

def test_category_detection():
    assert detect_category("how frequently to irrigate tomato") == "irrigation"
    assert detect_category("urea and dap dosage per acre") == "fertilizer"
    assert detect_category("control aphids and bollworm") == "pest_management"
    assert detect_category("pmkisan installment date") == "government_schemes"

def test_banned_chemical_check():
    has_banned, detected = check_banned_chemicals("Can I spray Endosulfan for pest?")
    assert has_banned is True
    assert "endosulfan" in detected

    has_banned_safe, _ = check_banned_chemicals("Can I use Neem oil or Trichoderma?")
    assert has_banned_safe is False

def test_chunking_preserves_sentences():
    text = (
        "Rice requires clayey soil. Seed rate is 35 kg per hectare. "
        "Transplant at 25 days. Maintain shallow water during vegetative phase. "
        "Drain water 15 days before harvesting."
    )
    chunks = chunk_text(text, chunk_size=20, chunk_overlap=5)
    assert len(chunks) >= 1
    assert "Rice" in chunks[0]

def test_abstention_on_irrelevant_query():
    # When query has no matching documents and similarity is below threshold
    res = agriparam_service.generate_advisory(
        query="Quantum cryptography algorithms in astrophysics",
        retrieved_chunks=[]
    )
    assert res["confidence_level"] == "Insufficient"
    assert "unavailable in the verified" in res["recommendation"]

