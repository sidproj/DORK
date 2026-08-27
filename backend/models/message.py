from dataclasses import asdict,dataclass
from datetime import datetime


@dataclass
class Message:
    id: int | None
    conversation_id: int
    role: str
    content: str
    tool_calls:str
    created_at: datetime | None = None
    
    def to_dict(self):
        return asdict(self)