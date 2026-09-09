from pathlib import Path

from app import main
from app.orchestrator import ConversationOrchestrator


def test_context_endpoint_returns_uploaded_inventory(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "engine", ConversationOrchestrator(tmp_path / "memory.db"))
    main.chat(main.ChatRequest(user_id="alex", message="Add my black shirt to my wardrobe"))
    context = main.user_context("alex")
    assert context["wardrobe"] == ["black shirt"]
    assert context["wardrobe_status"] == {"black shirt": "ready to wear"}


def test_context_endpoint_returns_empty_context_for_new_user(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "engine", ConversationOrchestrator(tmp_path / "memory.db"))
    context = main.user_context("new-user")
    assert context["user_id"] == "new-user"
    assert context["wardrobe"] == []


def test_wardrobe_item_can_be_removed(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "engine", ConversationOrchestrator(tmp_path / "memory.db"))
    main.chat(main.ChatRequest(user_id="alex", message="Add my black shirt to my wardrobe"))
    assert main.remove_wardrobe_item("alex", main.WardrobeItemRequest(item="black shirt")) == {"removed": "black shirt"}
    assert main.user_context("alex")["wardrobe"] == []


def test_frontend_has_user_gate_switching_and_inventory_refresh():
    page = (Path(__file__).parents[1] / "app" / "frontend" / "index.html").read_text(encoding="utf-8")
    assert 'id="gate"' in page
    assert "sessionStorage" in page
    assert "Switch user" in page
    assert "refreshContext();" in page
    assert "inventoryDesktop" in page and "inventoryMobile" in page
