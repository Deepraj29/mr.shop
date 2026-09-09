import sqlite3
from pathlib import Path

from .models import UserContext


class ContextManager:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY);
                CREATE TABLE IF NOT EXISTS user_context (
                    user_id TEXT PRIMARY KEY REFERENCES users(user_id),
                    style TEXT, colors TEXT NOT NULL DEFAULT '', size TEXT, budget INTEGER,
                    topic TEXT, occasion TEXT, last_referenced_item TEXT
                );
                CREATE TABLE IF NOT EXISTS wardrobe_items (
                    user_id TEXT REFERENCES users(user_id), item TEXT,
                    status TEXT NOT NULL DEFAULT 'ready to wear',
                    PRIMARY KEY (user_id, item)
                );
            """)

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def load(self, user_id: str) -> UserContext:
        with self._connect() as connection:
            row = connection.execute("SELECT style, colors, size, budget, topic, occasion, last_referenced_item FROM user_context WHERE user_id = ?", (user_id,)).fetchone()
            items = connection.execute("SELECT item, status FROM wardrobe_items WHERE user_id = ? ORDER BY rowid", (user_id,)).fetchall()
        if not row:
            return UserContext(user_id=user_id)
        style, colors, size, budget, topic, occasion, last_item = row
        return UserContext(user_id=user_id, wardrobe=[item for item, _ in items], wardrobe_status=dict(items), preferences={"style": style, "colors": colors.split(",") if colors else []}, constraints={"size": size, "budget": budget}, current_context={"topic": topic, "occasion": occasion, "last_referenced_item": last_item})

    def save(self, context: UserContext) -> None:
        with self._connect() as connection:
            connection.execute("INSERT OR IGNORE INTO users(user_id) VALUES (?)", (context.user_id,))
            connection.execute("""INSERT INTO user_context(user_id, style, colors, size, budget, topic, occasion, last_referenced_item)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET style=excluded.style, colors=excluded.colors, size=excluded.size, budget=excluded.budget, topic=excluded.topic, occasion=excluded.occasion, last_referenced_item=excluded.last_referenced_item""", (context.user_id, context.preferences["style"], ",".join(context.preferences["colors"]), context.constraints["size"], context.constraints["budget"], context.current_context["topic"], context.current_context["occasion"], context.current_context["last_referenced_item"]))
            connection.execute("DELETE FROM wardrobe_items WHERE user_id = ?", (context.user_id,))
            connection.executemany("INSERT INTO wardrobe_items(user_id, item, status) VALUES (?, ?, ?)", [(context.user_id, item, context.wardrobe_status.get(item, "ready to wear")) for item in context.wardrobe])

    def remove_wardrobe_item(self, user_id: str, item: str) -> bool:
        with self._connect() as connection:
            result = connection.execute("DELETE FROM wardrobe_items WHERE user_id = ? AND item = ?", (user_id, item))
        return result.rowcount == 1

    def update(self, context: UserContext, entities: dict, topic: str | None = None) -> UserContext:
        if "size" in entities:
            context.constraints["size"] = entities["size"]
        if "budget" in entities:
            context.constraints["budget"] = entities["budget"]
        if "style" in entities:
            context.preferences["style"] = entities["style"]
        if "color" in entities and entities["color"] not in context.preferences["colors"]:
            context.preferences["colors"].append(entities["color"])
        if "occasion" in entities:
            context.current_context["occasion"] = entities["occasion"]
        if topic:
            context.current_context["topic"] = topic
        return context
