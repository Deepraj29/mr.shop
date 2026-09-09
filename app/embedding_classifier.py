"""Semantic intent fallback with a local embedding fallback for offline demos."""

import hashlib
import math
import re

from .entity_extractor import normalize
from .models import Intent


EXAMPLES = {
    Intent.WARDROBE_UPLOAD: ("save this item in my closet", "put these clothes in my collection", "record my new outfit"),
    Intent.STYLING_ADVICE: ("help me put together a look", "suggest an outfit for tonight", "what goes well with my clothes"),
    Intent.PRODUCT_PURCHASE: ("show me options to order", "help me shop for clothing", "locate something I can purchase"),
    Intent.BOOKING: ("arrange a consultation with an expert", "schedule a session with a fashion advisor", "reserve time with a personal shopper"),
    Intent.GENERAL: ("hello", "thank you", "what can you do"),
}


class EmbeddingIntentClassifier:
    """Uses MiniLM when installed; otherwise uses deterministic hashed text vectors."""

    def __init__(self):
        self.examples = [(intent, example) for intent, examples in EXAMPLES.items() for example in examples]
        try:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.vectors = self.model.encode([example for _, example in self.examples], normalize_embeddings=True)
        except Exception:
            # The first MiniLM run may need a model download; stay functional offline.
            self.model = None
            self.vectors = [self._hash_embed(example) for _, example in self.examples]

    @staticmethod
    def _hash_embed(text: str, dimensions: int = 256) -> dict[int, float]:
        tokens = re.findall(r"[a-z]+", normalize(text))
        features = tokens + [token[index:index + 3] for token in tokens for index in range(max(0, len(token) - 2))]
        vector: dict[int, float] = {}
        for feature in features:
            index = int.from_bytes(hashlib.blake2b(feature.encode(), digest_size=2).digest(), "big") % dimensions
            vector[index] = vector.get(index, 0) + 1
        length = math.sqrt(sum(value * value for value in vector.values())) or 1
        return {index: value / length for index, value in vector.items()}

    def classify(self, message: str) -> tuple[Intent, float]:
        if self.model:
            query = self.model.encode(normalize(message), normalize_embeddings=True)
            scores = [float(query @ vector) for vector in self.vectors]
        else:
            query = self._hash_embed(message)
            scores = [sum(query.get(index, 0) * value for index, value in vector.items()) for vector in self.vectors]
        index = max(range(len(scores)), key=scores.__getitem__)
        return self.examples[index][0], max(0.0, scores[index])
