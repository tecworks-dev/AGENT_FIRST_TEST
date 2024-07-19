
# Purpose: Define custom exceptions for the application
# Description: This file contains custom exception classes that are used throughout the application to handle specific error scenarios.

import traceback


class AIServiceException(Exception):
    """Exception raised for errors in the AI service."""

    def __init__(self, message="An error occurred in the AI service"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"AIServiceException: {self.message}"


class DatabaseConnectionError(Exception):
    """Exception raised for database connection errors."""

    def __init__(self, message="Failed to connect to the database"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"DatabaseConnectionError: {self.message}"


class InvalidInputError(Exception):
    """Exception raised for invalid user input."""

    def __init__(self, message="Invalid input provided"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"InvalidInputError: {self.message}"


class AuthenticationError(Exception):
    """Exception raised for authentication failures."""

    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"AuthenticationError: {self.message}"


# Debug mode
DEBUG = True

def log_exception(exc):
    """Log the exception details if in debug mode."""
    if DEBUG:
        print(f"Exception details:\n{traceback.format_exc()}")


# Example usage:
if __name__ == "__main__":
    try:
        # Simulate an AI service error
        raise AIServiceException("Failed to generate response")
    except AIServiceException as e:
        print(str(e))
        log_exception(e)

    try:
        # Simulate a database connection error
        raise DatabaseConnectionError("Unable to connect to MySQL database")
    except DatabaseConnectionError as e:
        print(str(e))
        log_exception(e)

    try:
        # Simulate an invalid input error
        raise InvalidInputError("Username must be at least 3 characters long")
    except InvalidInputError as e:
        print(str(e))
        log_exception(e)

    try:
        # Simulate an authentication error
        raise AuthenticationError("Invalid credentials provided")
    except AuthenticationError as e:
        print(str(e))
        log_exception(e)
