from typing import Dict

from src.models import ChatRoom, PrivateChat


class ChatManager:
    def __init__(self):
        self.rooms: Dict[str, ChatRoom] = {}
        self.private_chats: Dict[str, PrivateChat] = {}
        self.user_sessions: Dict[str, set] = {}  # user_id -> set of socket connections

    def create_room(self, room_id: str, name: str) -> ChatRoom:
        if room_id not in self.rooms:
            self.rooms[room_id] = ChatRoom(room_id, name)
        return self.rooms[room_id]

    def get_or_create_private_chat(self, user1_id: str, user2_id: str) -> PrivateChat:
        chat_id = f"{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"
        if chat_id not in self.private_chats:
            self.private_chats[chat_id] = PrivateChat(user1_id, user2_id)
        return self.private_chats[chat_id]

    def add_user_session(self, user_id: str, socket) -> None:
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = set()
        self.user_sessions[user_id].add(socket)

    def remove_user_session(self, user_id: str, socket) -> None:
        if user_id in self.user_sessions:
            self.user_sessions[user_id].discard(socket)
            if not self.user_sessions[user_id]:
                del self.user_sessions[user_id]
