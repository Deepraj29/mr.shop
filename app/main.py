from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .orchestrator import ConversationOrchestrator

app = FastAPI(title="Mr.Shop Track A")
engine = ConversationOrchestrator(Path(__file__).parents[1] / "data" / "mrshop.db")
FRONTEND = Path(__file__).parent / "frontend" / "index.html"


class ChatRequest(BaseModel):
    user_id: str
    message: str


class WardrobeItemRequest(BaseModel):
    item: str


def valid_user_id(user_id: str) -> str:
    user_id = user_id.strip()
    if not 1 <= len(user_id) <= 80:
        raise HTTPException(status_code=422, detail="User ID must be 1 to 80 characters.")
    return user_id


@app.post("/chat")
def chat(request: ChatRequest):
    return engine.chat(valid_user_id(request.user_id), request.message)


@app.get("/users/{user_id}/context")
def user_context(user_id: str):
    return engine.contexts.load(valid_user_id(user_id)).to_dict()


@app.delete("/users/{user_id}/wardrobe")
def remove_wardrobe_item(user_id: str, request: WardrobeItemRequest):
    user_id, item = valid_user_id(user_id), request.item.strip()
    if not item:
        raise HTTPException(status_code=422, detail="Wardrobe item is required.")
    if not engine.contexts.remove_wardrobe_item(user_id, item):
        raise HTTPException(status_code=404, detail="Wardrobe item was not found.")
    return {"removed": item}


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND)


def cli() -> None:
    print("Mr.Shop mock Instagram chat. Type 'quit' to exit.")
    user_id = input("User ID [demo_user]: ").strip() or "demo_user"
    while (message := input("You: ").strip()) != "quit":
        if message:
            print("Mr.Shop:", engine.chat(user_id, message)["response"])


if __name__ == "__main__":
    cli()
