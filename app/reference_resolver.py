from .entity_extractor import extract_entities


def resolve_reference(message: str, context) -> dict:
    text, entities = message.lower(), extract_entities(message)
    last = context.current_context.get("last_referenced_item")
    references = ("it", "those", "that", "this", "the shirt", "the trousers", "the outfit")
    if last and any(ref in text for ref in references):
        entities["resolved_item"] = last
        if "category" not in entities:
            last_entities = extract_entities(last)
            entities.update({key: value for key, value in last_entities.items() if key not in entities})
    return entities
