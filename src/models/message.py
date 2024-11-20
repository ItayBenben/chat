from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class MessageType(Enum):
    GROUP = "GROUP"
    PRIVATE = "PRIVATE"


@dataclass
class Message:
    content: str
    sender_id: str
    timestamp: datetime
    message_type: MessageType
    recipient_id: Optional[str] = None

    def __str__(self) -> str:
        time_str = self.timestamp.strftime("%H:%M:%S")
        return f"[{time_str}] {self.sender_id}: {self.content}\n"
