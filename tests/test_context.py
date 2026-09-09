from app.orchestrator import ConversationOrchestrator


def test_context_retains_size(tmp_path):
    engine = ConversationOrchestrator(tmp_path / "memory.db")
    engine.chat("u", "Find a black blazer under 5000, size L")
    result = engine.chat("u", "Find trousers under 3000")
    assert result["context"]["constraints"]["size"] == "L"
