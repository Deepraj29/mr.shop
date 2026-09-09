from pathlib import Path

from .classifier import IntentClassifier
from .context_manager import ContextManager
from .entity_extractor import clothing_items
from .models import Intent
from .reference_resolver import resolve_reference
from .services.booking import BookingService
from .services.shopping import ShoppingService
from .services.styling import StylingService
from .services.wardrobe import WardrobeService


class ConversationOrchestrator:
    TOPICS = {Intent.WARDROBE_UPLOAD: "wardrobe", Intent.STYLING_ADVICE: "styling", Intent.PRODUCT_PURCHASE: "purchase", Intent.BOOKING: "booking"}

    def __init__(self, storage_path: str | Path | None = None):
        self.contexts = ContextManager(storage_path or Path(__file__).parents[1] / "data" / "mrshop.db")
        self.classifier = IntentClassifier()
        self.services = {Intent.WARDROBE_UPLOAD: WardrobeService(), Intent.STYLING_ADVICE: StylingService(), Intent.PRODUCT_PURCHASE: ShoppingService(), Intent.BOOKING: BookingService()}

    def chat(self, user_id: str, message: str) -> dict:
        context = self.contexts.load(user_id)
        classification = self.classifier.classify(message, context)
        entities = resolve_reference(message, context)
        # A styling prompt can introduce wardrobe facts before it is routed.
        for item in clothing_items(message):
            if item not in context.wardrobe:
                context.wardrobe.append(item)
        if classification.intent == Intent.GENERAL:
            response = "I'm not completely sure what you'd like to do. Would you like styling advice, shopping help, wardrobe management, or a stylist booking?"
        else:
            self.contexts.update(context, entities, self.TOPICS[classification.intent])
            response = self.services[classification.intent].execute(message, entities, context)
        self.contexts.save(context)
        return {"response": response, "intent": classification.intent.value, "confidence": classification.confidence, "entities": entities, "context": context.to_dict()}
