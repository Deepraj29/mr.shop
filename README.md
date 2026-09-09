# Mr.Shop — Track A conversational prototype

This is a prototype created for technical evaluation and is not production-grade. It simulates an Instagram-style chat locally; it does not integrate with Instagram, marketplaces, or booking providers.

## Objective

Demonstrate **intent understanding → structured ambient memory → reference resolution → topic switching → service routing → response**. The five supported intents are wardrobe upload, styling advice, product purchase, booking, and general conversation.

## Architecture

```text
Browser UI, CLI, or POST /chat → normalizer + entity extractor → intent classifier
                  → SQLite structured-memory manager → reference resolver
                  → orchestrator → wardrobe / styling / shopping / booking service
```

The orchestrator owns routing and state mutations. The classifier only interprets the message, so a future LLM classifier cannot directly purchase or book anything.

## Memory and topic switching

`UserContext` stores wardrobe, preferences, constraints (size/budget), and current context (topic/occasion/last referenced item). Updates merge only supplied fields, preserving unrelated facts. `it`, `those`, `that`, `this`, and named clothing references resolve to `last_referenced_item`.

For the main flow, "Make it more formal" stores `grey tailored trousers`. "Find those under ₹3000, size L" resolves that item, extracts budget and size, classifies as purchase, and switches the topic without repeating the outfit. A booking request then switches from purchasing to booking while retaining the same memory.

## Run

Requires Python 3.10+.

```bash
cd mrshop-track-a
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Send a request to `POST /chat`:

```json
{"user_id":"demo_user","message":"Find those under ₹3000, size L"}
```

Or use the local CLI:

```bash
python -m app.main
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) after starting Uvicorn to use the responsive browser chat interface. A user ID is required before chat begins; it identifies the SQLite-backed wardrobe and is shown as the profile name. The left sidebar displays the current user's inventory and item status, and the mobile profile panel exposes the same information.

Run tests:

```bash
pytest
```

Four clean-start demo scripts are in [demo/conversations.md](demo/conversations.md).

## Intent and entities

The hybrid classifier first uses deterministic rules for explicit commands, then uses `all-MiniLM-L6-v2` embeddings and cosine similarity against representative examples for looser phrasing. If the embedding package is unavailable, it falls back to local hashed text vectors so the prototype remains runnable offline. It normalizes `blk`, `gry`, `tee`, and `tshirt`; extracts category, color, size, budget, occasion, and style; and responds with a clarification prompt for low confidence. Purchase requests missing size or budget ask only for the missing information. A bare "Find those" with no prior item asks which item is meant.

## Design trade-offs and scaling

SQLite persistence keeps user context and wardrobe items in local relational tables without adding a database dependency. Structured memory is more reliable for reusable facts than raw history alone. Rule-based classification is fast, deterministic, cheap, and testable; its language coverage is intentionally limited.

To scale, retain the `IntentClassifier` interface and add entries to the orchestrator registry: **intent → handler → required entities → service**. The embedding classifier can be upgraded to a domain-tuned model, while deterministic services remain in control. Future intents can include order status, returns, outfit history, analytics, price alerts, and trend discovery without rewriting the conversation pipeline.

For production, protect user data, separate authentication, validate all fields, use idempotency for mutations, rate-limit requests, log classification outcomes rather than sensitive raw chats where possible, and monitor classification/topic-switch failures.

## Limitations

Products, availability, wardrobe input, and chat interface are mocked. There is no image understanding, authentication, real inventory, real booking, payment, or production data store.
