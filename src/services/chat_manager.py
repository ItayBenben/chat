from typing import Dict

from src.models import ChatRoom, PrivateChatRoom
from src.utils import ChatType
from src.utils.util import generate_private_chat_id


class ChatManager:
    def __init__(self):
        self.chats: Dict[str, ChatRoom] = {}
        self.user_sessions: Dict[str, set] = {}  # user_id -> set of socket connections

    def get_or_create_chat(self, user_id, chat_type: ChatType, target: str) -> ChatRoom:
        if chat_type == ChatType.PUBLIC:
            # target is chat_id
            if target not in self.chats:
                self.chats[target] = ChatRoom(target)
            return self.chats[target]

        elif chat_type == ChatType.PRIVATE:
            # target is the only other user_id in chat:
            chat_id = generate_private_chat_id(user_id, target)
            if chat_id not in self.chats:
                self.chats[chat_id] = PrivateChatRoom(chat_id)
            return self.chats[chat_id]

    def add_user_session(self, user_id: str, socket) -> None:
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = set()
        self.user_sessions[user_id].add(socket)

    def remove_user_session(self, user_id: str, chat_id: str, socket) -> None:
        if user_id in self.user_sessions:
            self.user_sessions[user_id].discard(socket)
            if not self.user_sessions[user_id]:
                del self.user_sessions[user_id]
        if chat_id in self.chats:
            self.chats[chat_id].remove_member(user_id)
