from collections import deque
from typing import Set, List

from src.models import Message, MessageType


class ChatRoom:
    def __init__(self, room_id: str, name: str, history_size: int = 100):
        self.room_id = room_id
        self.name = name
        self.messages = deque(maxlen=history_size)
        self.members: Set[str] = set()

    def add_message(self, message: Message) -> None:
        if message.message_type == MessageType.GROUP:
            self.messages.append(message)

    def get_recent_messages(self, count: int) -> List[Message]:
        return list(self.messages)[-count:]

    def add_member(self, user_id: str) -> None:
        self.members.add(user_id)

    def remove_member(self, user_id: str) -> None:
        self.members.discard(user_id)
