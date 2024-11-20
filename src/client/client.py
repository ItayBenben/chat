import socket
import sys
import threading
import time
from enum import Enum

import typer


class ChatType(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class ChatClient:
    def __init__(self, host: str = 'localhost', port: int = 2000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def receive_messages(self) -> None:
        while True:
            try:
                input_messages = self.socket.recv(1024).decode()
                messages = input_messages.split('\n')
                if not messages:
                    break
                for message in messages[:-1]:
                    if message.strip():
                        print(message)
                        time.sleep(0.01)
            except (socket.error, ConnectionError, ConnectionAbortedError) as e:
                print("Disconnected from server")
                self.socket.close()
                sys.exit()

    def send_login_details(self, user_name: str, chat_type: ChatType, target: str, history_length: int) -> None:
        self.socket.send(f"/login/{user_name}/{chat_type.value}/{target}/{history_length}".encode())

    def start(self, user_name: str, chat_type: ChatType, target: str, history_length: int) -> None:
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        self.send_login_details(user_name, chat_type, target, history_length)

        while True:
            try:
                message = input()
                if message.lower() == '/quit':
                    break
                self.socket.send(message.encode())
            except (socket.error, ConnectionResetError, ConnectionAbortedError) as e:
                print(f"Connection error: {e}")
                break
            except EOFError as e:  # Handles input() errors when stdin is closed
                print(f"Input error: {e}")
                break
            except KeyboardInterrupt:  # Handles Ctrl+C gracefully
                print("\nClosing connection...")
                break

        self.socket.close()


def run_client(
        host: str = typer.Option(..., "--host", "-h", help="Server host address"),
        port: int = typer.Option(..., "--port", "-p", help="Server port"),
        user_name: str = typer.Option(..., "--name", "-n", help="Your username"),
        chat_type: ChatType = typer.Option(..., "--type", "-ty", help="Chat type: public or private"),
        target: str = typer.Option(..., "--target", "-ta",
                                   help="Chat room name for public mode or username for private mode"),
        history_length: int = typer.Option(10, "--length", "-len", help="Number of messages to retrieve")):
    try:
        client = ChatClient(host, port)
        client.start(user_name, chat_type, target, history_length)
    except (socket.timeout, ConnectionRefusedError) as e:
        print(f"Connection to server failed: {e}")


if __name__ == "__main__":
    typer.run(run_client)
