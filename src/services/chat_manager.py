from typing import Dict

from src.models import ChatRoom
from src.utils import ChatType


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
        # elif chat_type == ChatType.PRIVATE:
        # target is the only other user_id in chat:
        #    chat_id = generate_private_chat_id(user_id, target)
        #    if chat_id not in self.chats:
        #        self.chats[target] = PrivateChatRoom(chat_id, user_id, target)
        #    return self.chats[target]

    """
    def create_room(self, room_id: str, name: str) -> ChatRoom:
        if room_id not in self.rooms:
            self.rooms[room_id] = ChatRoom(room_id, name)
        return self.rooms[room_id]

    def get_or_create_private_chat(self, user1_id: str, user2_id: str) -> PrivateChat:
        chat_id = f"{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"
        if chat_id not in self.private_chats:
            self.private_chats[chat_id] = PrivateChat(user1_id, user2_id)
        return self.private_chats[chat_id]
    """

    def add_user_session(self, user_id: str, socket) -> None:
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = set()
        self.user_sessions[user_id].add(socket)

    def remove_user_session(self, user_id: str, socket) -> None:
        if user_id in self.user_sessions:
            self.user_sessions[user_id].discard(socket)
            if not self.user_sessions[user_id]:
                del self.user_sessions[user_id]
