class StylingService:
    def execute(self, message, entities, context):
        top = next((item for item in context.wardrobe if any(category in item for category in ("shirt", "t-shirt", "blazer", "jacket"))), "black shirt")
        trousers = next((item for item in context.wardrobe if "trousers" in item), "grey tailored trousers")
        jeans = next((item for item in context.wardrobe if "jeans" in item), "blue jeans")
        footwear = next((item for item in context.wardrobe if "shoes" in item or "sneakers" in item), "white sneakers")
        occasion = entities.get("occasion") or context.current_context.get("occasion")
        formal = entities.get("style") == "formal" or "more formal" in message.lower()
        if formal:
            item = "grey tailored trousers"
            context.current_context["last_referenced_item"] = item
            return f"Keep the {top} and switch to tailored grey trousers for a more formal look."
        item = trousers if occasion in {"office", "interview", "wedding"} else jeans
        context.current_context["last_referenced_item"] = item
        if occasion:
            return f"For a {occasion}, try your {top} with {item} and {footwear}."
        return f"Try your {top} with {item} and {footwear}."
