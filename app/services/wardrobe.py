from ..entity_extractor import clothing_items


class WardrobeService:
    def execute(self, message, entities, context):
        items = clothing_items(message)
        if "list wardrobe" in message.lower() or "show my wardrobe" in message.lower():
            return "Your wardrobe: " + (", ".join(context.wardrobe) if context.wardrobe else "is currently empty.")
        for item in items:
            if item not in context.wardrobe:
                context.wardrobe.append(item)
            context.wardrobe_status[item] = "damaged" if "damaged" in message.lower() else "ready to wear"
        if not items:
            return "I can add clothing items such as a black shirt or blue jeans to your wardrobe."
        return f"Added {', '.join(items)} to your wardrobe."
