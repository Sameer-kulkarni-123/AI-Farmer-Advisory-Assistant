"""
Agricultural advisory input validation and chemical safety checks.
"""

import re
from typing import Tuple, List

# Central Insecticides Board & Registration Committee (CIBRC) banned or restricted chemicals
BANNED_PESTICIDES = [
    "endosulfan", "monocrotophos", "phorate", "paraquat", "chlordane", "aldrin",
    "dieldrin", "heptachlor", "methyl parathion", "methomyl", "phosphamidon"
]

def check_banned_chemicals(query: str) -> Tuple[bool, List[str]]:
    """
    Check if the query or recommendation mentions banned/hazardous agrochemicals.
    Returns (has_banned, list_of_detected_chemicals).
    """
    q_lower = query.lower()
    detected = []
    for chemical in BANNED_PESTICIDES:
        if re.search(r'\b' + re.escape(chemical) + r'\b', q_lower):
            detected.append(chemical)
    return (len(detected) > 0, detected)

def sanitize_farmer_query(query: str) -> str:
    """Strip dangerous characters and trim excessive input length."""
    if not query:
        return ""
    # Strip markup / HTML
    cleaned = re.sub(r'<[^>]*>', '', query)
    # Limit max length to avoid prompt injection or overflow
    cleaned = cleaned[:1000].strip()
    return cleaned

