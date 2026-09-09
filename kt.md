# KT — Remove MiniLM Embedding Classifier

Knowledge transfer for the Track A change that replaced MiniLM / `sentence-transformers` with a lightweight rule-based intent classifier.

## Why

- MiniLM (`all-MiniLM-L6-v2` via `sentence-transformers`) pulled a heavy ML stack (torch / transformers).
- That inflated memory and blocked free-tier deploys (e.g. Render ~512 MB).
- Track A allows either rule-based or embedding-based intent classification.

## What changed

| Area | Before | After |
|------|--------|-------|
| Intent fallback | MiniLM cosine similarity (+ hash-vector offline fallback) | Expanded keyword/phrase rules only |
| Module | `app/embedding_classifier.py` | Deleted |
| Deps | `sentence-transformers>=3,<4` | Removed from `requirements.txt` |
| Public API | `IntentClassifier.classify(message, context=None)` | Unchanged |

Unchanged: FastAPI routes, frontend, SQLite, orchestrator, context manager, entity extractor, wardrobe / styling / shopping / booking services, request/response shapes.

Small related fix: soft pronouns (`it` / `that` / `this`) in `reference_resolver.py` no longer override an explicitly named clothing item in the same turn (e.g. “forget that. Find white sneakers…”).

## Current chat flow

```text
User message
  → normalize + extract entities
  → rule-based IntentClassifier (priority order)
  → ambient context update
  → reference resolver
  → ConversationOrchestrator
  → wardrobe / styling / shopping / booking service
  → response
```

## Intent priority

First strong match wins:

1. `BOOKING`
2. `WARDROBE_UPLOAD`
3. `PRODUCT_PURCHASE`
4. `STYLING_ADVICE`
5. `GENERAL` (default; never null)

Examples:

- “Book a stylist to help me choose an outfit” → `BOOKING`
- “Buy the trousers you recommended” → `PRODUCT_PURCHASE`
- Bare “blue jeans” (no action) → `GENERAL` (not wardrobe)

## Key files

- `app/classifier.py` — rule-based classifier
- `app/entity_extractor.py` — normalize + entities (unchanged)
- `app/reference_resolver.py` — `those` / soft refs; soft refs skip when category is explicit
- `app/orchestrator.py` — routing (unchanged interface)
- `requirements.txt` — `fastapi`, `uvicorn`, `pytest` only
- `tests/test_classifier.py` — five intents + priority / ambiguity cases
- `README.md` — documents rule-based architecture

## Run / verify

```bash
cd mrshop-track-a
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port $PORT   # or --reload locally
```

Tests (from `mrshop-track-a`):

```bash
set PYTHONPATH=.
python -m pytest -q
```

Expect: app starts with **no model download**; no `sentence_transformers` / `SentenceTransformer` / `all-MiniLM` in the tree.

## Deploy note

Build: `pip install -r requirements.txt`  
Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`  

No ML startup config. Memory should be substantially lower without MiniLM; do not claim a specific RAM number unless measured.

## Handoff checklist

- [x] MiniLM / SentenceTransformer removed
- [x] Embedding module deleted
- [x] `sentence-transformers` removed from requirements
- [x] Five intents + multi-turn / reference / topic-switch tests green
- [x] README reflects rule-based classifier
