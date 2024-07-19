
# app/services/logging_service.py

"""
This module implements centralized logging for the application.
It provides a LoggingService class with methods for logging information,
errors, and debug messages.
"""

import logging
import traceback
from typing import Optional

class LoggingService:
    def __init__(self):
        # Configure the logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def log_info(self, message: str) -> None:
        """
        Log an informational message.

        Args:
            message (str): The message to be logged.
        """
        self.logger.info(message)

    def log_error(self, message: str, exception: Optional[Exception] = None) -> None:
        """
        Log an error message along with exception details if provided.

        Args:
            message (str): The error message to be logged.
            exception (Exception, optional): The exception object, if any.
        """
        if exception:
            error_details = f"{message}\n{traceback.format_exc()}"
            self.logger.error(error_details)
        else:
            self.logger.error(message)

    def log_debug(self, message: str) -> None:
        """
        Log a debug message.

        Args:
            message (str): The debug message to be logged.
        """
        self.logger.debug(message)

# Add debugging statements
if __name__ == "__main__":
    logging_service = LoggingService()
    logging_service.log_info("This is an info message")
    logging_service.log_debug("This is a debug message")
    try:
        raise ValueError("This is a test exception")
    except ValueError as e:
        logging_service.log_error("An error occurred", e)
