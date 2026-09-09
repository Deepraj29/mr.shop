from .entity_extractor import extract_entities


def resolve_reference(message: str, context) -> dict:
    text, entities = message.lower(), extract_entities(message)
    last = context.current_context.get("last_referenced_item")
    hard_refs = ("those", "the shirt", "the trousers", "the outfit")
    soft_refs = ("it", "that", "this")
    # Soft pronouns like "forget that" must not override an explicitly named item.
    should_resolve = last and (
        any(ref in text for ref in hard_refs)
        or (any(ref in text for ref in soft_refs) and "category" not in entities)
    )
    if should_resolve:
        entities["resolved_item"] = last
        if "category" not in entities:
            last_entities = extract_entities(last)
            entities.update({key: value for key, value in last_entities.items() if key not in entities})
    return entities
