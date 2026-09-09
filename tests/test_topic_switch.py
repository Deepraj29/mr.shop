from app.orchestrator import ConversationOrchestrator


def test_styling_to_purchase_and_booking(tmp_path):
    engine = ConversationOrchestrator(tmp_path / "memory.db")
    engine.chat("u", "I have a black shirt and blue jeans. What should I wear to a party?")
    engine.chat("u", "Make it more formal")
    purchase = engine.chat("u", "Find those under ₹3000, size L")
    booking = engine.chat("u", "Can I talk to a stylist about this outfit?")
    assert purchase["intent"] == "PRODUCT_PURCHASE"
    assert purchase["context"]["wardrobe"] == ["black shirt", "blue jeans"]
    assert booking["intent"] == "BOOKING"


def test_latest_purchase_request_overrides_previous(tmp_path):
    engine = ConversationOrchestrator(tmp_path / "memory.db")
    engine.chat("u", "Find black shoes under 5000, size L")
    result = engine.chat("u", "Actually, forget that. Find white sneakers under 5000, size L")
    assert result["context"]["current_context"]["last_referenced_item"] == "white sneakers"


def test_styling_varies_with_occasion_and_wardrobe(tmp_path):
    engine = ConversationOrchestrator(tmp_path / "memory.db")
    party = engine.chat("u", "I have a white shirt and blue jeans. What should I wear to a party?")
    office = engine.chat("u", "What should I wear to the office?")
    assert "party" in party["response"]
    assert "white shirt" in party["response"]
    assert "office" in office["response"]
    assert party["response"] != office["response"]
