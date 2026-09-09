class ShoppingService:
    PRODUCTS = [
        {"name": "Grey Tailored Trousers", "category": "trousers", "color": "grey", "price": 2499, "sizes": ["M", "L", "XL"]},
        {"name": "Slim Grey Trousers", "category": "trousers", "color": "grey", "price": 2799, "sizes": ["S", "M", "L"]},
        {"name": "Classic Black Blazer", "category": "blazer", "color": "black", "price": 4499, "sizes": ["M", "L", "XL"]},
    ]

    def execute(self, message, entities, context):
        category = entities.get("category")
        if not category:
            return "Which item would you like me to find?"
        size = entities.get("size") or context.constraints.get("size")
        budget = entities.get("budget") or context.constraints.get("budget")
        if not size or not budget:
            missing = "size and approximate budget" if not size and not budget else ("size" if not size else "approximate budget")
            return f"Sure. What {missing} should I use?"
        color = entities.get("color")
        products = [p for p in self.PRODUCTS if p["category"] == category and size in p["sizes"] and p["price"] <= budget and (not color or p["color"] == color)]
        context.current_context["last_referenced_item"] = entities.get("resolved_item") or f"{color + ' ' if color else ''}{category}"
        if not products:
            return f"I couldn't find {context.current_context['last_referenced_item']} in size {size} under ₹{budget}."
        lines = [f"{index}. {p['name']} — ₹{p['price']} — {size}" for index, p in enumerate(products, 1)]
        return f"I found these options for {context.current_context['last_referenced_item']}, size {size}, within ₹{budget}:\n" + "\n".join(lines)
