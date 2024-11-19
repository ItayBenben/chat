import socket
import threading
from datetime import datetime
from typing import Optional

from src.models import Message, MessageType
from src.services import ChatManager

# TODO: MOVE TO FILE
RECENT_MESSAGE_COUNT = 10


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
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            thread.start()

    def handle_client(self, client_socket: socket.socket) -> None:
        try:
            send_to_client(client_socket, "Enter your user ID: \n")
            user_id = client_socket.recv(1024).decode().strip()
            self.chat_manager.add_user_session(user_id, client_socket)

            # Send available commands
            help_message = """
            Commands:
            /join <room_id> [recent_count]    - Join a group chat room (optional count of recent messages to view) 
            /private <user_id> [recent_count] - Start private chat with user (optional count of recent messages to view)
            /help                             - Show this message
            /quit                             - Exit the chat\n
            """
            send_to_client(client_socket, help_message)

            # new client - empty room/chat status.
            current_room = None
            current_private_chat = None

            while True:
                message = client_socket.recv(1024).decode().strip()
                if not message:
                    break

                if message.startswith('/'):
                    current_room, current_private_chat = self.handle_command(message, user_id, client_socket,
                                                                             current_room, current_private_chat)
                    continue

                # Handle message based on current context (room or private chat)
                if current_room:
                    self.broadcast_room_message(message, user_id, current_room)
                elif current_private_chat:
                    self.send_private_message(message, user_id, current_private_chat)
                else:
                    send_to_client(client_socket, "Please join a room or start a private chat first.\n")

        except Exception as e:
            print(f"Error handling client {user_id}: {e}")
        finally:
            if user_id:
                self.chat_manager.remove_user_session(user_id, client_socket)
            client_socket.close()

    def handle_command(self, command: str, user_id: str, client_socket: socket.socket, current_room: Optional[str],
                       current_private_chat: Optional[str]) -> tuple[Optional[str], Optional[str]]:
        parts = command.split()
        cmd = parts[0].lower()
        # get from input the count of previous messages to view
        if len(parts) < 3:
            recent_messages_count = 10
        else:
            try:
                recent_messages_count = int(parts[2])
            except (ValueError, IndexError):  # input from Client wasn't valid: set to default 10.
                recent_messages_count = RECENT_MESSAGE_COUNT

        if cmd == '/join':
            if len(parts) < 2:
                send_to_client(client_socket, "Usage: /join <room_id>\n")
                return current_room, current_private_chat

            room_id = parts[1]
            room = self.chat_manager.create_room(room_id, f"Room {room_id}")
            # todo: handle user override
            room.add_member(user_id)
            send_to_client(client_socket, f"Joined room {room_id}\n")
            for message in room.get_recent_messages(recent_messages_count):
                send_to_client(client_socket, message.format())
            return room_id, None

        elif cmd == '/private':
            if len(parts) < 2:
                send_to_client(client_socket, "Usage: /private <user_id>\n")
                return current_room, current_private_chat
            other_user_id = parts[1]
            # todo: handle user override
            self.chat_manager.get_or_create_private_chat(user_id, other_user_id)
            send_to_client(client_socket, f"Started private chat with {other_user_id}\n")
            for message in self.chat_manager.get_or_create_private_chat(user_id, other_user_id).get_recent_messages(
                    recent_messages_count):
                send_to_client(client_socket, message.format())
            return None, other_user_id

        elif cmd == '/quit':
            # Todo: remove client from room
            raise ConnectionError("User quit")

        return current_room, current_private_chat

    def broadcast_room_message(self, content: str, sender_id: str, room_id: str) -> None:
        message = Message(
            content=content,
            sender_id=sender_id,
            timestamp=datetime.now(),
            message_type=MessageType.GROUP
        )
        room = self.chat_manager.rooms.get(room_id)
        if room:
            room.add_message(message)
            formatted_message = message.format()

            for member_id in room.members:
                if member_id != sender_id:
                    for socket in self.chat_manager.user_sessions.get(member_id, set()):
                        send_to_client(socket, formatted_message)

    def send_private_message(self, content: str, sender_id: str, recipient_id: str) -> None:
        message = Message(
            content=content,
            sender_id=sender_id,
            timestamp=datetime.now(),
            message_type=MessageType.PRIVATE,
            recipient_id=recipient_id
        )

        chat = self.chat_manager.get_or_create_private_chat(sender_id, recipient_id)
        chat.add_message(message)
        formatted_message = message.format()

        for socket in self.chat_manager.user_sessions.get(recipient_id, set()):
            send_to_client(socket, formatted_message)


"""
if __name__ == "__main__":
    server = ChatServer()
    server.start()
"""
