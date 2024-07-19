
"""
Purpose: Centralizes input validation and sanitization for the application.
Description: This module provides a centralized location for input validation and sanitization,
improving security and reducing code duplication across the application.
"""

import re
from email_validator import validate_email, EmailNotValidError
import traceback

DEBUG = True

class InputValidator:
    def __init__(self):
        if DEBUG:
            print("InputValidator initialized")

    def validate_string(self, input: str, min_length: int, max_length: int) -> bool:
        """
        Validates string input based on minimum and maximum length.

        Args:
            input (str): The string to validate.
            min_length (int): The minimum allowed length.
            max_length (int): The maximum allowed length.

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        try:
            if not isinstance(input, str):
                return False
            if len(input) < min_length or len(input) > max_length:
                return False
            return True
        except Exception as e:
            if DEBUG:
                print(f"Error in validate_string: {str(e)}")
                traceback.print_exc()
            return False

    def validate_email(self, email: str) -> bool:
        """
        Validates email addresses.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email is valid, False otherwise.
        """
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
        except Exception as e:
            if DEBUG:
                print(f"Error in validate_email: {str(e)}")
                traceback.print_exc()
            return False

    def validate_integer(self, input: str, min_value: int, max_value: int) -> bool:
        """
        Validates integer input based on minimum and maximum values.

        Args:
            input (str): The string representation of the integer to validate.
            min_value (int): The minimum allowed value.
            max_value (int): The maximum allowed value.

        Returns:
            bool: True if the input is a valid integer within the specified range, False otherwise.
        """
        try:
            value = int(input)
            return min_value <= value <= max_value
        except ValueError:
            return False
        except Exception as e:
            if DEBUG:
                print(f"Error in validate_integer: {str(e)}")
                traceback.print_exc()
            return False

    def sanitize_input(self, input: str) -> str:
        """
        Sanitizes input to prevent XSS attacks.

        Args:
            input (str): The input string to sanitize.

        Returns:
            str: The sanitized input string.
        """
        try:
            # Remove HTML tags
            sanitized = re.sub(r'<[^>]*?>', '', input)
            # Encode special characters
            sanitized = sanitized.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#x27;')
            return sanitized
        except Exception as e:
            if DEBUG:
                print(f"Error in sanitize_input: {str(e)}")
                traceback.print_exc()
            return ""

if DEBUG:
    # Test the InputValidator class
    validator = InputValidator()
    print(f"String validation: {validator.validate_string('test', 2, 10)}")
    print(f"Email validation: {validator.validate_email('test@example.com')}")
    print(f"Integer validation: {validator.validate_integer('5', 1, 10)}")
    print(f"Input sanitization: {validator.sanitize_input('<script>alert("XSS")</script>')}")
