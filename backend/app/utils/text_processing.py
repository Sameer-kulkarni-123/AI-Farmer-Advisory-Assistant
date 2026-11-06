"""
Text processing, chunking, and agricultural entity recognition utilities.
"""

import re
from typing import List, Dict, Any, Tuple

# Pre-compiled Indian agricultural keywords
CROPS = {
    "rice": ["rice", "paddy", "dhan", "chawal", "arisi", "vari", "nellu", "bhat"],
    "wheat": ["wheat", "gehun", "godhumai", "godhuma", "gahu", "gom"],
    "maize": ["maize", "corn", "makka", "makki", "cholam", "mokka jonnalu"],
    "cotton": ["cotton", "kapas", "paruthi", "prathi", "kapaas"],
    "tomato": ["tomato", "tamatar", "thakkali", "tamata"],
    "potato": ["potato", "aloo", "batata", "urulaikizhangu", "bangaladumpa", "alu"],
    "groundnut": ["groundnut", "peanut", "moongphali", "kadalai", "verusanaga", "shengdana", "chinabadam"],
    "soybean": ["soybean", "soya", "soyabean"],
    "sugarcane": ["sugarcane", "ganna", "karumbu", "cheruku", "ush"],
    "pulses": ["pulse", "pulses", "dal", "chickpea", "bengal gram", "chana", "pigeonpea", "arhar", "tur", "red gram"]
}

TOPIC_KEYWORDS = {
    "fertilizer": ["fertilizer", "fertilizers", "fertilize", "urea", "dap", "npk", "potash", "mop", "ssp", "manure", "nitrogen", "phosphorus", "potassium", "zinc", "nutrient", "nutrients", "khad"],
    "irrigation": ["irrigation", "irrigate", "irrigating", "water", "watering", "drainage", "drip", "sprinkler", "moisture", "flood", "pani", "sinchai", "water tube", "awd"],
    "pest_management": ["pest", "pests", "insect", "insects", "worm", "bollworm", "caterpillar", "borer", "aphid", "aphids", "whitefly", "thrips", "bug", "ipm", "pesticide", "pesticides", "spray", "keeda"],
    "disease": ["disease", "diseases", "blight", "rot", "wilt", "rust", "mildew", "spot", "virus", "fungus", "fungicide", "rog", "beemari"],
    "soil_health": ["soil", "soils", "mitti", "land preparation", "plowing", "clay", "loam", "sandy", "saline", "alkaline", "ph", "carbon", "health card"],
    "organic_farming": ["organic", "jeevamrit", "beejamrit", "compost", "natural farming", "neemastra", "brahmastra", "biofertilizer", "jaivik"],
    "government_schemes": ["scheme", "schemes", "subsidy", "subsidies", "pmkisan", "pm-kisan", "pmfby", "crop insurance", "soil health card", "kisan credit card", "kcc", "yojana"]
}

def clean_text(text: str) -> str:
    """Normalize whitespace and remove unprintable characters."""
    if not text:
        return ""
    text = re.sub(r'[\r\n]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 450, chunk_overlap: int = 80) -> List[str]:
    """
    Split text into overlapping semantic chunks based on sentence boundaries.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return []

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', cleaned)
    chunks = []
    current_chunk = []
    current_len = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        words = sentence.split()
        sentence_len = len(words)

        if current_len + sentence_len > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            # Keep overlap sentences from end
            overlap_words = 0
            overlap_sentences = []
            for s in reversed(current_chunk):
                s_words = len(s.split())
                if overlap_words + s_words <= chunk_overlap:
                    overlap_sentences.insert(0, s)
                    overlap_words += s_words
                else:
                    break
            current_chunk = overlap_sentences
            current_len = sum(len(s.split()) for s in current_chunk)

        current_chunk.append(sentence)
        current_len += sentence_len

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def detect_crop(query: str) -> str:
    """Identify if the query specifies an Indian crop."""
    q_lower = query.lower()
    for crop_name, aliases in CROPS.items():
        for alias in aliases:
            pattern = r'\b' + re.escape(alias) + r'\b'
            if re.search(pattern, q_lower):
                return crop_name.capitalize()
    return "All"

def detect_category(query: str) -> str:
    """Identify the main agricultural topic of the query."""
    q_lower = query.lower()
    for category, keywords in TOPIC_KEYWORDS.items():
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, q_lower):
                return category
    return "cultivation"
