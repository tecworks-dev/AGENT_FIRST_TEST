
"""
Logging utility for the entire application.

This module provides logging functionality for the entire application,
including setup of the logger and convenience functions for logging
errors and info messages.
"""

import logging
import traceback
import sys

DEBUG = True

def setup_logger() -> logging.Logger:
    """
    Sets up and returns a logger object.

    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger('SecureMessagingApp')
    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)

    return logger

def log_error(message: str):
    """
    Logs an error message.

    Args:
        message (str): The error message to log.
    """
    logger = logging.getLogger('SecureMessagingApp')
    logger.error(message)
    if DEBUG:
        logger.error(traceback.format_exc())

def log_info(message: str):
    """
    Logs an info message.

    Args:
        message (str): The info message to log.
    """
    logger = logging.getLogger('SecureMessagingApp')
    logger.info(message)

# Initialize the logger when the module is imported
logger = setup_logger()

if DEBUG:
    logger.debug("Debugging is enabled.")

# Exception hook to log unhandled exceptions
def exception_handler(exc_type, exc_value, exc_traceback):
    """
    Global exception handler to log unhandled exceptions.
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = exception_handler
