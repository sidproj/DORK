from dataclasses import dataclass
from datetime import datetime


@dataclass
class Conversation:
    id: int | None
    title: str
    created_at: datetime | None = None
    updated_at: datetime | None = None