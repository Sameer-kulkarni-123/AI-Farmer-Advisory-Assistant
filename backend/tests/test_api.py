"""
Direct API Endpoint Integration Tests (invoking route handlers with Session).
"""

import pytest
from backend.app.models.database import SessionLocal, init_db
from backend.app.models.schemas import ChatRequest, AdvisoryRequest
from backend.app.api.health import check_health
from backend.app.api.languages import get_supported_languages
from backend.app.api.sources import get_sources
from backend.app.api.chat import post_chat_query
from backend.app.api.advisory import post_crop_advisory

@pytest.fixture(scope="module")
def db_session():
    init_db()
    db = SessionLocal()
    yield db
    db.close()

def test_health_endpoint():
    res = check_health()
    assert res.status == "healthy"
    assert "Agri" in res.agriparam_engine
    assert "en" in res.supported_languages

def test_languages_endpoint():
    res = get_supported_languages()
    assert len(res) >= 7
    codes = [item.code for item in res]
    assert "en" in codes
    assert "hi" in codes
    assert "kn" in codes
    assert "ta" in codes
    assert "te" in codes

def test_sources_endpoint(db_session):
    res = get_sources(crop=None, category=None, verified_only=True, db=db_session)
    assert len(res) >= 1
    first = res[0]
    assert first.document_id is not None
    assert first.source_url is not None

def test_chat_endpoint_paddy_query(db_session):
    req = ChatRequest(
        message="Which fertilizer should I use for growing paddy?",
        language="en",
        crop="Rice"
    )
    res = post_chat_query(req, db=db_session)
    assert res["conversation_id"] is not None
    assert "advisory" in res
    assert res["advisory"]["confidence_level"] in ["Strong", "Limited", "Insufficient"]
    assert len(res["advisory"]["practical_steps"]) > 0

def test_chat_banned_chemical_precaution(db_session):
    req = ChatRequest(
        message="Can I spray Endosulfan or Monocrotophos on tomato crop for insects?",
        language="en",
        crop="Tomato"
    )
    res = post_chat_query(req, db=db_session)
    precautions = " ".join(res["advisory"]["important_precautions"])
    assert "banned" in precautions.lower() or "alert" in precautions.lower()

def test_structured_advisory_endpoint(db_session):
    req = AdvisoryRequest(
        crop="Wheat",
        category="cultivation",
        state="Punjab",
        soil_type="Alluvial Loam",
        growth_stage="Crown Root Initiation",
        language="en"
    )
    res = post_crop_advisory(req, db=db_session)
    assert res["crop"] == "Wheat"
    assert "recommendation" in res["advisory"]
