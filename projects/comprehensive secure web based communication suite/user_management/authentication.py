"""
Purpose: Handles user authentication and authorization.
This module provides functionality for user registration and login.
"""

import traceback
from utils.helpers import hash_password, verify_password
from typing import Optional

DEBUG = True

class AuthManager:
    def __init__(self):
        self.users = {}  # In-memory user storage for demonstration purposes

    def register_user(self, username: str, password: str) -> bool:
        """
        Register a new user with the given username and password.

        Args:
            username (str): The username for the new user.
            password (str): The password for the new user.

        Returns:
            bool: True if registration is successful, False otherwise.
        """
        try:
            if username in self.users:
                if DEBUG:
                    print(f"Debug: User {username} already exists.")
                return False

            hashed_password = hash_password(password)
            self.users[username] = hashed_password

            if DEBUG:
                print(f"Debug: User {username} registered successfully.")
            return True
        except Exception as e:
            print(f"Error occurred while registering user: {str(e)}")
            if DEBUG:
                traceback.print_exc()
            return False

    def login_user(self, username: str, password: str) -> Optional[str]:
        """
        Authenticate a user with the given username and password.

        Args:
            username (str): The username of the user trying to log in.
            password (str): The password provided by the user.

        Returns:
            Optional[str]: A session token if login is successful, None otherwise.
        """
        try:
            if username not in self.users:
                if DEBUG:
                    print(f"Debug: User {username} not found.")
                return None

            stored_password = self.users[username]
            if verify_password(stored_password, password):
                session_token = f"{username}_session_token"  # Simple token generation for demonstration
                if DEBUG:
                    print(f"Debug: User {username} logged in successfully.")
                return session_token
            else:
                if DEBUG:
                    print(f"Debug: Invalid password for user {username}.")
                return None
        except Exception as e:
            print(f"Error occurred while logging in user: {str(e)}")
            if DEBUG:
                traceback.print_exc()
            return None

# Example usage and testing
if __name__ == "__main__":
    auth_manager = AuthManager()

    # Test user registration
    print(auth_manager.register_user("alice", "password123"))  # Should return True
    print(auth_manager.register_user("alice", "newpassword"))  # Should return False (user already exists)

    # Test user login
    print(auth_manager.login_user("alice", "password123"))  # Should return a session token
    print(auth_manager.login_user("alice", "wrongpassword"))  # Should return None
    print(auth_manager.login_user("bob", "password123"))  # Should return None (user doesn't exist)