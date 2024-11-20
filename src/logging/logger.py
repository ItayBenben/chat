import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class MultiFormatLogger:
    def __init__(self,
                 log_dir: str = 'logs',
                 base_filename: str = 'chat_server',
                 log_level: int = logging.INFO):
        """
        Initialize a multi-format logger that writes to both text and JSON log files.

        :param log_dir: Directory to store log files
        :param base_filename: Base name for log files
        :param log_level: Logging level (default: logging.INFO)
        """
        # Create logs directory if it doesn't exist
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Text logger setup
        self.text_log_path = self.log_dir / f'{base_filename}.log'
        self.text_logger = logging.getLogger(f'{base_filename}_text')
        self.text_logger.setLevel(log_level)

        # Text log handler
        text_handler = logging.FileHandler(self.text_log_path)
        text_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        text_handler.setFormatter(text_formatter)

        # Clear existing handlers to prevent duplicate logs
        self.text_logger.handlers.clear()
        self.text_logger.addHandler(text_handler)

        # JSON log file setup
        self.json_log_path = self.log_dir / f'{base_filename}.json'
        self.json_file = open(self.json_log_path, 'a', encoding='utf-8')

    def info(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log an INFO level message"""
        self._log(message, logging.INFO, extra_data)

    def warning(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log a WARNING level message"""
        self._log(message, logging.WARNING, extra_data)

    def error(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log an ERROR level message"""
        self._log(message, logging.ERROR, extra_data)

    def debug(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log a DEBUG level message"""
        self._log(message, logging.DEBUG, extra_data)

    def _log(self,
             message: str,
             level: int = logging.INFO,
             extra_data: Optional[Dict[str, Any]] = None):
        """
        Internal method to log messages to both text and JSON formats.

        :param message: Log message
        :param level: Logging level
        :param extra_data: Additional context data to include in JSON log
        """
        # Log to text logger
        if level == logging.INFO:
            self.text_logger.info(message)
        elif level == logging.WARNING:
            self.text_logger.warning(message)
        elif level == logging.ERROR:
            self.text_logger.error(message)
        elif level == logging.DEBUG:
            self.text_logger.debug(message)

        # Prepare JSON log entry
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': logging.getLevelName(level),
            'message': message,
        }

        # Add extra data if provided
        if extra_data:
            log_entry['extra'] = extra_data

        # Write to JSON log file
        json.dump(log_entry, self.json_file)
        self.json_file.write('\n')
        self.json_file.flush()

    def close(self):
        """
        Close the JSON log file to ensure all logs are written.
        """
        if hasattr(self, 'json_file') and not self.json_file.closed:
            self.json_file.close()


# Create a global logger instance
logger = MultiFormatLogger()

import atexit

atexit.register(logger.close)
