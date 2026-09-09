from app.orchestrator import ConversationOrchestrator


def test_those_resolves_last_recommended_item(tmp_path):
    engine = ConversationOrchestrator(tmp_path / "memory.db")
    engine.chat("u", "I have a black shirt and blue jeans. What should I wear to a party?")
    engine.chat("u", "Make it more formal")
    result = engine.chat("u", "Find those under ₹3000, size L")
    assert result["entities"]["resolved_item"] == "grey tailored trousers"
    assert "Grey Tailored Trousers" in result["response"]
