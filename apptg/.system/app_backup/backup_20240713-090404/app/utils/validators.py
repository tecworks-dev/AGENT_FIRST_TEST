
# Purpose: Input validation functions for user-related data
# Description: This module provides functions to validate email addresses, passwords, and usernames

import re
import traceback

# Enable debugging
DEBUG = True

def validate_email(email):
    """
    Validates the format of an email address.

    Args:
    email (str): The email address to validate.

    Returns:
    bool: True if the email is valid, False otherwise.
    """
    try:
        if DEBUG:
            print(f"Validating email: {email}")

        # Regular expression for email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(email_regex, email):
            if DEBUG:
                print("Email is valid")
            return True
        else:
            if DEBUG:
                print("Email is invalid")
            return False
    except Exception as e:
        print(f"Error validating email: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        return False

def validate_password(password):
    """
    Validates the strength of a password.

    Args:
    password (str): The password to validate.

    Returns:
    bool: True if the password is strong enough, False otherwise.
    """
    try:
        if DEBUG:
            print("Validating password strength")

        # Password must be at least 8 characters long
        if len(password) < 8:
            if DEBUG:
                print("Password is too short")
            return False

        # Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character
        if not re.search(r'[A-Z]', password):
            if DEBUG:
                print("Password lacks an uppercase letter")
            return False
        if not re.search(r'[a-z]', password):
            if DEBUG:
                print("Password lacks a lowercase letter")
            return False
        if not re.search(r'\d', password):
            if DEBUG:
                print("Password lacks a digit")
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            if DEBUG:
                print("Password lacks a special character")
            return False

        if DEBUG:
            print("Password is valid")
        return True
    except Exception as e:
        print(f"Error validating password: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        return False

def validate_username(username):
    """
    Validates the format of a username.

    Args:
    username (str): The username to validate.

    Returns:
    bool: True if the username is valid, False otherwise.
    """
    try:
        if DEBUG:
            print(f"Validating username: {username}")

        # Username must be 3-20 characters long and contain only alphanumeric characters and underscores
        username_regex = r'^[a-zA-Z0-9_]{3,20}$'
        
        if re.match(username_regex, username):
            if DEBUG:
                print("Username is valid")
            return True
        else:
            if DEBUG:
                print("Username is invalid")
            return False
    except Exception as e:
        print(f"Error validating username: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        return False

# Unit tests
import unittest

class TestValidators(unittest.TestCase):
    def test_validate_email(self):
        self.assertTrue(validate_email("user@example.com"))
        self.assertFalse(validate_email("invalid-email"))
        self.assertFalse(validate_email("user@example"))

    def test_validate_password(self):
        self.assertTrue(validate_password("StrongP@ss1"))
        self.assertFalse(validate_password("weak"))
        self.assertFalse(validate_password("NoSpecialChar1"))

    def test_validate_username(self):
        self.assertTrue(validate_username("valid_user123"))
        self.assertFalse(validate_username("sh"))
        self.assertFalse(validate_username("invalid username"))

if __name__ == "__main__":
    unittest.main()
