"""
Language Detection Service for Indian Languages and English.
Uses Unicode character block analysis and linguistic keyword heuristics.
"""

import re
from typing import Tuple

class LanguageDetectionService:
    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect whether the text is English, Hindi, Kannada, Tamil, Telugu, Bengali, or Marathi.
        Returns (language_code, confidence).
        """
        if not text or not text.strip():
            return "en", 1.0

        clean = text.strip()
        total_chars = len(clean)

        # Count characters by Unicode block
        devanagari_count = 0
        tamil_count = 0
        telugu_count = 0
        kannada_count = 0
        bengali_count = 0
        latin_count = 0

        for ch in clean:
            cp = ord(ch)
            if 0x0900 <= cp <= 0x097F:
                devanagari_count += 1
            elif 0x0B80 <= cp <= 0x0BFF:
                tamil_count += 1
            elif 0x0C00 <= cp <= 0x0C7F:
                telugu_count += 1
            elif 0x0C80 <= cp <= 0x0CFF:
                kannada_count += 1
            elif 0x0980 <= cp <= 0x09FF:
                bengali_count += 1
            elif (0x0041 <= cp <= 0x005A) or (0x0061 <= cp <= 0x007A):
                latin_count += 1

        # Check dominant script
        counts = {
            "devanagari": devanagari_count,
            "ta": tamil_count,
            "te": telugu_count,
            "kn": kannada_count,
            "bn": bengali_count,
            "en": latin_count
        }

        dominant_script, max_c = max(counts.items(), key=lambda item: item[1])

        if max_c == 0:
            return "en", 0.5

        confidence = min(1.0, max_c / (total_chars * 0.7 + 1))

        if dominant_script == "devanagari":
            # Disambiguate Marathi vs Hindi using key function words
            marathi_markers = ["आहे", "नाही", "करावे", "पिकासाठी", "खत", "कसे", "पाणी", "लागवड", "काय"]
            hindi_markers = ["है", "नहीं", "करें", "फसल", "खाद", "कैसे", "पानी", "बुवाई", "क्या", "चाहिए"]

            m_score = sum(1 for m in marathi_markers if m in clean)
            h_score = sum(1 for h in hindi_markers if h in clean)

            if m_score > h_score:
                return "mr", confidence
            return "hi", confidence

        return dominant_script, confidence

language_detector = LanguageDetectionService()

