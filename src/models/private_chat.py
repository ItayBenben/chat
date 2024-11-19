from collections import deque
from typing import List

from src.models import Message


class PrivateChat:
    def __init__(self, user1_id: str, user2_id: str, history_size: int = 100):
        self.chat_id = f"{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"
        self.participants = {user1_id, user2_id}
        self.messages = deque(maxlen=history_size)

    def add_message(self, message: Message) -> None:
        if message.sender_id in self.participants and message.recipient_id in self.participants:
            self.messages.append(message)

    def get_recent_messages(self, count: int) -> List[Message]:
        return list(self.messages)[-count:]
