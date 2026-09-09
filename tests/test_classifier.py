from app.classifier import IntentClassifier
from app.models import Intent


def test_core_intents():
    classifier = IntentClassifier()
    assert classifier.classify("Add this black shirt").intent == Intent.WARDROBE_UPLOAD
    assert classifier.classify("What should I wear?").intent == Intent.STYLING_ADVICE
    assert classifier.classify("Find a black blazer under 5000").intent == Intent.PRODUCT_PURCHASE
    assert classifier.classify("I want to talk to a stylist").intent == Intent.BOOKING


def test_wardrobe_intents():
    classifier = IntentClassifier()
    assert classifier.classify("Add my black shirt").intent == Intent.WARDROBE_UPLOAD
    assert classifier.classify("Remove my blue jeans").intent == Intent.WARDROBE_UPLOAD
    assert classifier.classify("Save this item in my wardrobe").intent == Intent.WARDROBE_UPLOAD
    assert classifier.classify("Put this in my closet").intent == Intent.WARDROBE_UPLOAD


def test_styling_intents():
    classifier = IntentClassifier()
    assert classifier.classify("What should I wear to a party?").intent == Intent.STYLING_ADVICE
    assert classifier.classify("What goes with my blue jeans?").intent == Intent.STYLING_ADVICE
    assert classifier.classify("Can you help me put together a look for tonight?").intent == Intent.STYLING_ADVICE
    assert classifier.classify("Suggest an outfit").intent == Intent.STYLING_ADVICE


def test_purchase_intents():
    classifier = IntentClassifier()
    assert classifier.classify("I want to buy shoes").intent == Intent.PRODUCT_PURCHASE
    assert classifier.classify("Find trousers under ₹3000").intent == Intent.PRODUCT_PURCHASE
    assert classifier.classify("Show me options to order").intent == Intent.PRODUCT_PURCHASE


def test_booking_intents():
    classifier = IntentClassifier()
    assert classifier.classify("Book a stylist").intent == Intent.BOOKING
    assert classifier.classify("Can I talk to a stylist?").intent == Intent.BOOKING
    assert classifier.classify("Schedule a consultation").intent == Intent.BOOKING


def test_general_intent():
    classifier = IntentClassifier()
    assert classifier.classify("Hello").intent == Intent.GENERAL
    assert classifier.classify("Thanks").intent == Intent.GENERAL
    assert classifier.classify("Who are you?").intent == Intent.GENERAL


def test_priority_booking_over_styling():
    assert IntentClassifier().classify("Book a stylist to help me choose an outfit").intent == Intent.BOOKING


def test_priority_purchase_over_styling():
    assert IntentClassifier().classify("Buy the trousers you recommended").intent == Intent.PRODUCT_PURCHASE


def test_bare_clothing_noun_is_not_wardrobe():
    assert IntentClassifier().classify("blue jeans").intent == Intent.GENERAL
