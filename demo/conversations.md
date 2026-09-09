# Demo conversations

Run each conversation with a fresh user ID (or delete `data/mrshop.db`).

## 1. Wardrobe

```text
User: Add my black shirt and blue jeans to my wardrobe.
Assistant: Added black shirt, blue jeans to your wardrobe.
```

## 2. Styling

```text
User: I have a black shirt and blue jeans. What should I wear to a party?
Assistant: Try your black shirt with blue jeans and white sneakers.
```

## 3. Styling → purchase

```text
User: I have a black shirt and blue jeans. What should I wear to a party?
Assistant: Try your black shirt with blue jeans and white sneakers.
User: Make it more formal.
Assistant: Keep the black shirt and switch to tailored grey trousers.
User: Find those under ₹3000, size L.
Assistant: I found these options for grey tailored trousers, size L, within ₹3000:
1. Grey Tailored Trousers — ₹2499 — L
2. Slim Grey Trousers — ₹2799 — L
```

## 4. Purchase → booking

```text
User: Find a black blazer under ₹5000, size L.
Assistant: I found these options for black blazer, size L, within ₹5000: ...
User: Can I talk to a stylist about this?
Assistant: I can help you book a stylist consultation. Available slots: Tomorrow 5:00 PM or Tomorrow 7:00 PM.
```
