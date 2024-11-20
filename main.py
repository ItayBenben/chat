from src.logging.logger import logger
from src.server.server import ChatServer

if __name__ == "__main__":
    try:
        logger.info("Starting Chat Server")
        server = ChatServer()
        server.start()
    except Exception as e:
        logger.info(f"Critical server error: {e}")
        raise
