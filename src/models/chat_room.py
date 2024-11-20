from collections import deque
from typing import Set, List

from src.logging.logger import logger
from src.models import Message


class ChatRoom:
    def __init__(self, chat_id: str, history_size: int = 100):
        self.id = chat_id
        self.messages = deque(maxlen=history_size)
        self.members: Set[str] = set()

    def add_message(self, message: Message) -> None:
        logger.debug("Adding message")
        self.messages.append(message)

    def get_recent_messages(self, count: int) -> List[Message]:
        return list(self.messages)[-count:]

    def add_member(self, user_id: str) -> None:
        logger.info(f"Adding {user_id} to member list")
        self.members.add(user_id)

    def remove_member(self, user_id: str) -> None:
        logger.info(f"Removing {user_id} from member list")
        self.members.discard(user_id)


class PrivateChatRoom(ChatRoom):
    def __init__(self, chat_id: str, history_size: int = 100):
        super().__init__(chat_id, history_size)

    def add_member(self, user_id: str) -> None:
        if len(self.members) >= 2:
            print("Invalid member insertion")
            logger.error(f"Invalid member {user_id} insertion")
            raise ValueError
        logger.info(f"Successfully added {user_id} as member")
        self.members.add(user_id)
