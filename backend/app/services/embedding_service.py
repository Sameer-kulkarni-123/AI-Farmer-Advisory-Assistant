"""
Multilingual Embedding Service for Agricultural Document Retrieval.
Supports SentenceTransformers with a resilient fallback dense projector.
"""

import math
import re
import zlib
from typing import List
import numpy as np
from backend.app.config import settings
from backend.app.core.logging import logger

def _stable_hash(s: str) -> int:
    """Deterministic CRC32 hash across processes and platforms."""
    return zlib.crc32(s.encode('utf-8'))

class EmbeddingService:
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL_NAME
        self.dimension = settings.EMBEDDING_DIMENSION
        self._st_model = None
        self._use_fallback = False
        self._initialize_model()

    def _initialize_model(self):
        """Try loading sentence-transformers multilingual model, fall back gracefully if unavailable."""
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading multilingual embedding model: {self.model_name}...")
            self._st_model = SentenceTransformer(self.model_name)
            logger.info("SentenceTransformer loaded successfully.")
        except Exception as e:
            logger.warning(f"Could not load SentenceTransformer ({e}). Utilizing fallback dense multilingual embedding engine.")
            self._use_fallback = True

    def get_embedding(self, text: str) -> List[float]:
        """Compute embedding vector for a single text."""
        return self.get_embeddings([text])[0]

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Compute embedding vectors for a batch of texts."""
        if not texts:
            return []

        if not self._use_fallback and self._st_model is not None:
            try:
                embeddings = self._st_model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
                return embeddings.tolist()
            except Exception as e:
                logger.error(f"Error in SentenceTransformer encoding: {e}. Falling back to dense projector.")
                return [self._fallback_projector(t) for t in texts]

        return [self._fallback_projector(t) for t in texts]

    def _fallback_projector(self, text: str) -> List[float]:
        """
        Agricultural domain-weighted TF-IDF hash projection (384-dim).
        Filters English stop words and heavily weights agricultural keywords,
        ensuring high semantic alignment even without PyTorch.
        """
        dim = self.dimension
        vec = np.zeros(dim, dtype=np.float32)
        words = re.findall(r'\w+', text.lower())

        if not words:
            return vec.tolist()

        stop_words = {
            "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
            "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but",
            "by", "can", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for",
            "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself",
            "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just",
            "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once",
            "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
            "she", "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them",
            "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too",
            "under", "until", "up", "very", "was", "we", "were", "what", "when", "where", "which",
            "while", "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself"
        }

        # Key agricultural root terms
        agri_boost = {
            "rice": 4.0, "paddy": 4.5, "wheat": 4.0, "cotton": 4.0, "maize": 4.0, "tomato": 4.0,
            "potato": 4.0, "groundnut": 4.0, "soybean": 4.0, "sugarcane": 4.0, "pulses": 4.0,
            "fertilizer": 4.0, "urea": 5.0, "dap": 5.0, "npk": 5.0, "potash": 4.5, "irrigation": 4.0,
            "pest": 4.0, "bollworm": 5.0, "blight": 5.0, "disease": 4.0, "soil": 4.0, "scheme": 4.0,
            "pmkisan": 5.0, "pmfby": 5.0, "gypsum": 4.5, "organic": 4.0, "jeevamrit": 5.0
        }

        # Compute term frequency
        tf = {}
        for w in words:
            if w not in stop_words and len(w) > 2:
                tf[w] = tf.get(w, 0) + 1

        if not tf:
            # Fall back to raw words if all were stops
            for w in words:
                tf[w] = 1

        for word, count in tf.items():
            weight = (1.0 + math.log(count)) * agri_boost.get(word, 1.5)
            h = _stable_hash(word)
            idx = abs(h) % dim
            sign = 1.0 if (h >> 3) & 1 else -1.0
            vec[idx] += sign * weight

            # Character 3-grams
            for i in range(len(word) - 2):
                tri = word[i:i+3]
                th = _stable_hash(tri)
                tidx = abs(th) % dim
                tsign = 1.0 if (th >> 2) & 1 else -1.0
                vec[tidx] += tsign * (weight * 0.3)

        # L2 normalize
        norm = np.linalg.norm(vec)
        if norm > 1e-6:
            vec = vec / norm
        return vec.tolist()

# Global singleton
embedding_service = EmbeddingService()
