from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class Intent(str, Enum):
    WARDROBE_UPLOAD = "WARDROBE_UPLOAD"
    STYLING_ADVICE = "STYLING_ADVICE"
    PRODUCT_PURCHASE = "PRODUCT_PURCHASE"
    BOOKING = "BOOKING"
    GENERAL = "GENERAL"


@dataclass
class UserContext:
    user_id: str
    wardrobe: list[str] = field(default_factory=list)
    wardrobe_status: dict[str, str] = field(default_factory=dict)
    preferences: dict[str, Any] = field(default_factory=lambda: {"style": None, "colors": []})
    constraints: dict[str, Any] = field(default_factory=lambda: {"size": None, "budget": None})
    current_context: dict[str, Any] = field(default_factory=lambda: {"topic": None, "occasion": None, "last_referenced_item": None})

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserContext":
        return cls(**data)


@dataclass
class Classification:
    intent: Intent
    confidence: float
    entities: dict[str, Any]
