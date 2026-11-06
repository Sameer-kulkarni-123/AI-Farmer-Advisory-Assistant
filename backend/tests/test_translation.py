"""
Unit Tests for Multilingual Language Detection and Translation Services.
"""

from backend.app.services.language_detection import language_detector
from backend.app.services.translation_service import translation_service

def test_language_detection():
    # Hindi
    lang, conf = language_detector.detect_language("धान की फसल में कौन सा खाद डालना चाहिए?")
    assert lang == "hi"

    # Kannada
    lang, conf = language_detector.detect_language("ಭತ್ತದ ಬೆಳೆಗೆ ಎಷ್ಟು ನೀರು ಬೇಕು?")
    assert lang == "kn"

    # Tamil
    lang, conf = language_detector.detect_language("நெல் பயிருக்கு எந்த உரம் சிறந்தது?")
    assert lang == "ta"

    # Telugu
    lang, conf = language_detector.detect_language("వరి పంటకు ఎంత నీరు అవసరం?")
    assert lang == "te"

    # Bengali
    lang, conf = language_detector.detect_language("ধান চাষের জন্য কোন সার ব্যবহার করা উচিত?")
    assert lang == "bn"

    # Marathi
    lang, conf = language_detector.detect_language("कापूस पिकासाठी खत व्यवस्थापन कसे करावे?")
    assert lang == "mr"

    # English
    lang, conf = language_detector.detect_language("What is the seed rate for wheat cultivation?")
    assert lang == "en"

def test_query_translation_to_english():
    hi_query = "धान में कौन सी खाद डालें?"
    translated = translation_service.translate_query_to_english(hi_query, "hi")
    assert "paddy" in translated.lower() or "rice" in translated.lower() or "fertilizer" in translated.lower()

def test_advisory_translation_preserves_technical_terms():
    sample_advisory = {
        "crop": "Rice",
        "recommendation": "Apply Neem-Coated Urea @ 100 kg/ha in 3 split doses.",
        "practical_steps": ["Puddle the soil before transplanting.", "Maintain 2-3 cm shallow water."],
        "important_precautions": ["Never broadcast urea under bright sun."],
        "confidence_level": "Strong"
    }

    translated = translation_service.translate_advisory(sample_advisory, "hi")
    assert "सलाह" in translated["recommendation"] or "अनुशंसा" in translated["recommendation"]
    assert len(translated["practical_steps"]) == 2

