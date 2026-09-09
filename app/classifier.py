from .entity_extractor import extract_entities, normalize
from .embedding_classifier import EmbeddingIntentClassifier
from .models import Classification, Intent


class IntentClassifier:
    """Rules handle precise commands; embeddings interpret looser natural language."""

    def __init__(self):
        self.embeddings = EmbeddingIntentClassifier()

    def classify(self, message: str, context=None) -> Classification:
        text, entities = normalize(message), extract_entities(message)
        if any(word in text for word in ("book", "appointment", "consultation", "talk to", "speak to", "stylist")):
            return Classification(Intent.BOOKING, 0.96, entities)
        if (any(word in text for word in ("add", "upload", "my wardrobe", "put this")) and any(word in text for word in ("shirt", "jeans", "trousers", "blazer", "shoes", "sneakers"))) or "list wardrobe" in text or "show my wardrobe" in text:
            return Classification(Intent.WARDROBE_UPLOAD, 0.95, entities)
        purchase_words = ("find", "buy", "purchase", "shop", "looking for", "show me")
        if any(word in text for word in purchase_words) or ("those" in text and ("budget" in entities or "size" in entities)):
            return Classification(Intent.PRODUCT_PURCHASE, 0.93, entities)
        styling_words = ("what should i wear", "wear to", "outfit", "style me", "more formal", "more casual")
        if any(word in text for word in styling_words) or (context and context.current_context.get("topic") == "styling" and text in {"it", "make it more formal"}):
            return Classification(Intent.STYLING_ADVICE, 0.90, entities)
        intent, confidence = self.embeddings.classify(text)
        if intent != Intent.GENERAL and confidence >= 0.42:
            return Classification(intent, confidence, entities)
        return Classification(Intent.GENERAL, confidence if intent == Intent.GENERAL else 0.35, entities)
