import re


NORMALIZATIONS = {"blk": "black", "gry": "grey", "tee": "t-shirt", "tshirt": "t-shirt"}
CATEGORIES = ("t-shirt", "shirt", "jeans", "trousers", "blazer", "shoes", "sneakers", "jacket", "dress")
COLORS = ("black", "white", "blue", "grey", "gray", "red", "green", "brown", "navy")
OCCASIONS = ("party", "wedding", "office", "date", "interview", "casual")
STYLES = ("formal", "minimal", "casual", "smart casual", "streetwear")


def normalize(message: str) -> str:
    text = message.lower().strip()
    for short, full in NORMALIZATIONS.items():
        text = re.sub(rf"\b{short}\b", full, text)
    return re.sub(r"\s+", " ", text)


def extract_entities(message: str) -> dict[str, object]:
    text = normalize(message)
    found: dict[str, object] = {}
    colors = ["grey" if value == "gray" else value for value in COLORS if re.search(rf"\b{value}\b", text)]
    categories = [value for value in CATEGORIES if re.search(rf"\b{re.escape(value)}\b", text)]
    if colors:
        found["color"] = colors[-1]
    if categories:
        found["category"] = categories[-1]
    size = re.search(r"\b(?:size\s*)?(xs|s|m|l|xl|xxl)\b", text, re.I)
    if size:
        found["size"] = size.group(1).upper()
    budget = re.search(r"(?:under|below|within|budget\s*(?:of|is)?|₹|rs\.?|inr)\s*₹?\s*([\d,]+)", text, re.I)
    if budget:
        found["budget"] = int(budget.group(1).replace(",", ""))
    for occasion in OCCASIONS:
        if re.search(rf"\b{re.escape(occasion)}\b", text):
            found["occasion"] = occasion
    for style in STYLES:
        if style in text:
            found["style"] = style
    return found


def clothing_items(message: str) -> list[str]:
    """Return simple color/category pairs for text wardrobe uploads."""
    text = normalize(message)
    items = []
    for category in CATEGORIES:
        match = re.search(rf"\b({'|'.join(COLORS)})\s+{re.escape(category)}\b", text)
        if match:
            items.append(f"{'grey' if match.group(1) == 'gray' else match.group(1)} {category}")
    return items
