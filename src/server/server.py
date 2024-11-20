import socket
import threading
from datetime import datetime
from typing import Optional

from src.logging.logger import logger
from src.models import Message
from src.services import ChatManager
from src.utils import ChatType


def send_to_client(client_socket, message):
    client_socket.send(message.encode())


class ChatServer:
    def __init__(self, host: str = 'localhost', port: int = 5559):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_manager = ChatManager()

    def start(self) -> None:
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        logger.info(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            thread.start()

    def handle_client(self, client_socket: socket.socket) -> None:
        logger.info("Thread started running")
        try:
            user_id = None
            chat_id = None

            while True:
                message = client_socket.recv(1024).decode().strip()
                if not message:
                    break

                if message.startswith('/login'):
                    logger.info("logging in a user")
                    user_id, chat_id = self.handle_command(message, client_socket)
                    self.chat_manager.add_user_session(user_id, client_socket)
                    continue
                if message.startswith('/quit'):
                    logger.info(f"removing a user {user_id} from {chat_id}")
                    self.chat_manager.remove_user_session(user_id, chat_id, client_socket)
                    client_socket.close()
                    break

                # Send message to chat
                if chat_id:
                    logger.debug(f"Sending message from {user_id} to {chat_id}")
                    self.send_chat_message(message, user_id, chat_id)
                else:
                    send_to_client(client_socket, "Please join a room or start a private chat first.\n")

        except Exception as e:
            logger.error(f"Error handling client {user_id}: {e}")
        finally:
            if user_id:
                self.chat_manager.remove_user_session(user_id, chat_id, client_socket)
            client_socket.close()

    def handle_command(self, message: str, client_socket: socket.socket) -> tuple[Optional[str], Optional[str]]:
        parts = message.split('/')
        # todo: load this params in a better way. use  dict\struct.
        user_id = parts[2]
        chat_type = ChatType(parts[3])
        target = parts[4]
        recent_messages_count = int(parts[5])

        # join or create a chat
        chat_room = self.chat_manager.get_or_create_chat(user_id, chat_type, target)
        # join myself to the chat
        chat_room.add_member(user_id)

        send_to_client(client_socket, f"Joined room {chat_room.id}\n")
        # show recent messages
        for message in chat_room.get_recent_messages(recent_messages_count):
            send_to_client(client_socket, str(message))
        logger.info(f"finished logging in {user_id} to {chat_room.id}")
        return user_id, chat_room.id

    def send_chat_message(self, content: str, sender_user_id: str, chat_id: str) -> None:
        message = Message(
            content=content,
            sender_id=sender_user_id,
            timestamp=datetime.now(),
        )
        chat = self.chat_manager.chats.get(chat_id)
        if chat:
            chat.add_message(message)

            for member_id in chat.members:
                if member_id != sender_user_id:
                    for client_socket in self.chat_manager.user_sessions.get(member_id, set()):
                        send_to_client(client_socket, str(message))
