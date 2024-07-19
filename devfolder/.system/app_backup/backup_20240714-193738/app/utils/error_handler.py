
# app/utils/error_handler.py
"""
This module implements a global exception handler and centralizes error handling logic.
It provides functions and classes for handling errors, logging them, and returning
appropriate responses to the client.
"""

import traceback
from typing import Tuple, Dict, Any
from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException

def handle_error(error: Exception) -> Tuple[str, int]:
    """
    Handles and logs errors.

    Args:
        error (Exception): The error to handle.

    Returns:
        Tuple[str, int]: A tuple containing the error message and HTTP status code.
    """
    if isinstance(error, HTTPException):
        status_code = error.code
        message = error.description
    else:
        status_code = 500
        message = "An unexpected error occurred. Please try again later."

    log_error(error, {"status_code": status_code})
    return jsonify({"error": message}), status_code

def log_error(error: Exception, context: Dict[str, Any]) -> None:
    """
    Logs detailed error information.

    Args:
        error (Exception): The error to log.
        context (Dict[str, Any]): Additional context information about the error.
    """
    error_message = f"Error: {str(error)}\nContext: {context}\n"
    error_message += "".join(traceback.format_tb(error.__traceback__))
    current_app.logger.error(error_message)

class GlobalExceptionHandler:
    """
    A class that provides a global exception handler for the Flask application.
    """

    def __init__(self, app):
        """
        Initializes the GlobalExceptionHandler.

        Args:
            app (Flask): The Flask application instance.
        """
        self.app = app
        self.app.register_error_handler(Exception, self.handle_exception)

    def handle_exception(self, error: Exception):
        """
        Handles uncaught exceptions globally.

        Args:
            error (Exception): The uncaught exception.

        Returns:
            Response: A Flask response object containing the error details.
        """
        return handle_error(error)

# Debugging statements
if current_app.config.get('DEBUG', True):
    print("Debug mode is enabled for error_handler.py")
    print("GlobalExceptionHandler is ready to catch and handle exceptions")
