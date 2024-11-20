from collections import deque
from typing import Set, List

from src.models import Message


class ChatRoom:
    def __init__(self, chat_id: str, history_size: int = 100):
        self.id = chat_id
        self.messages = deque(maxlen=history_size)
        self.members: Set[str] = set()

    def add_message(self, message: Message) -> None:
        self.messages.append(message)

    def get_recent_messages(self, count: int) -> List[Message]:
        return list(self.messages)[-count:]

    def add_member(self, user_id: str) -> None:
        self.members.add(user_id)

    def remove_member(self, user_id: str) -> None:
        self.members.discard(user_id)
