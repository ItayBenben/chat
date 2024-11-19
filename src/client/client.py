import socket
import sys
import threading
import time

import typer


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

    def start(self) -> None:
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

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


def main(host: str, port: int):
    try:
        client = ChatClient(host, port)
        client.start()
    except (socket.timeout, ConnectionRefusedError) as e:
        print(f"Connection to server failed: {e}")


if __name__ == "__main__":
    typer.run(main)
