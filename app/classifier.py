from .entity_extractor import extract_entities, normalize
from .models import Classification, Intent


CLOTHING_ITEMS = (
    "shirt",
    "jeans",
    "trousers",
    "blazer",
    "shoes",
    "sneakers",
    "outfit",
    "clothes",
    "clothing",
)

WARDROBE_ACTIONS = ("add", "save", "upload", "own", "remove", "delete", "put this", "put these")
WARDROBE_STORAGE = ("wardrobe", "closet", "collection", "my wardrobe")

PURCHASE_PHRASES = (
    "buy",
    "purchase",
    "shop",
    "shopping",
    "find",
    "looking for",
    "show me",
    "order",
    "price",
    "under",
    "budget",
    "available",
    "where can i buy",
)

STYLING_PHRASES = (
    "what should i wear",
    "wear to",
    "wear",
    "outfit",
    "style me",
    "styling",
    "style",
    "match",
    "matching",
    "go with",
    "goes with",
    "pair",
    "formal",
    "casual",
    "suggest",
    "recommend",
    "put together a look",
    "put together",
    "what goes with",
    "what matches",
)


class IntentClassifier:
    """Lightweight rule-based intent classifier with fixed priority."""

    def classify(self, message: str, context=None) -> Classification:
        text, entities = normalize(message), extract_entities(message)

        if self._is_booking(text):
            return Classification(Intent.BOOKING, 0.96, entities)
        if self._is_wardrobe(text):
            return Classification(Intent.WARDROBE_UPLOAD, 0.95, entities)
        if self._is_purchase(text, entities):
            return Classification(Intent.PRODUCT_PURCHASE, 0.93, entities)
        if self._is_styling(text, context):
            return Classification(Intent.STYLING_ADVICE, 0.90, entities)
        return Classification(Intent.GENERAL, 0.35, entities)

    @staticmethod
    def _is_booking(text: str) -> bool:
        booking_words = (
            "book",
            "booking",
            "schedule",
            "appointment",
            "consultation",
            "talk to",
            "speak to",
            "stylist",
            "available slot",
            "slot",
        )
        return any(word in text for word in booking_words)

    @staticmethod
    def _is_wardrobe(text: str) -> bool:
        if "list wardrobe" in text or "show my wardrobe" in text:
            return True
        has_action = any(word in text for word in WARDROBE_ACTIONS)
        has_storage = any(word in text for word in WARDROBE_STORAGE)
        has_item = any(word in text for word in CLOTHING_ITEMS)
        if has_action and (has_storage or has_item):
            return True
        if has_storage and ("put" in text or "add" in text or "save" in text):
            return True
        return False

    @staticmethod
    def _is_purchase(text: str, entities: dict) -> bool:
        if any(phrase in text for phrase in PURCHASE_PHRASES):
            return True
        if "those" in text and ("budget" in entities or "size" in entities):
            return True
        if "size" in text and ("need" in text or "want" in text):
            return True
        return False

    @staticmethod
    def _is_styling(text: str, context) -> bool:
        if any(phrase in text for phrase in STYLING_PHRASES):
            return True
        if context and context.current_context.get("topic") == "styling":
            if text in {"it", "make it more formal", "more formal", "more casual"}:
                return True
        return False
