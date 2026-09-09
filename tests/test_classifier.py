from app.classifier import IntentClassifier
from app.models import Intent


def test_core_intents():
    classifier = IntentClassifier()
    assert classifier.classify("Add this black shirt").intent == Intent.WARDROBE_UPLOAD
    assert classifier.classify("What should I wear?").intent == Intent.STYLING_ADVICE
    assert classifier.classify("Find a black blazer under 5000").intent == Intent.PRODUCT_PURCHASE
    assert classifier.classify("I want to talk to a stylist").intent == Intent.BOOKING


def test_embedding_fallback_understands_looser_styling_language():
    assert IntentClassifier().classify("Can you help me put together a look for tonight?").intent == Intent.STYLING_ADVICE
