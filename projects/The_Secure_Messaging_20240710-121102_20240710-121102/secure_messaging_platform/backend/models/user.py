
# Purpose: Define the User model for the Secure Messaging Platform
# Description: This file contains the User SQLAlchemy model with methods for password hashing and verification

import traceback
from ..extensions import db, bcrypt
import unittest

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password: str) -> None:
        """
        Set the hashed password for the user.

        Args:
            password (str): The plain text password to be hashed.

        Returns:
            None
        """
        try:
            self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        except Exception as e:
            print(f"Error setting password: {str(e)}")
            traceback.print_exc()

    def check_password(self, password: str) -> bool:
        """
        Check if the provided password matches the stored hash.

        Args:
            password (str): The plain text password to be checked.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        try:
            return bcrypt.check_password_hash(self.password_hash, password)
        except Exception as e:
            print(f"Error checking password: {str(e)}")
            traceback.print_exc()
            return False

    def __repr__(self):
        return f'<User {self.username}>'

# Debug statements
if __name__ == '__main__':
    DEBUG = True
    if DEBUG:
        print("Debug mode is active for User model")
        print(f"User model tablename: {User.__tablename__}")
        print(f"User model columns: {User.__table__.columns.keys()}")

# Unit tests for User model
class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(username="testuser", email="test@example.com", password="testpassword")

    def test_password_hashing(self):
        self.assertNotEqual(self.user.password_hash, "testpassword")
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertFalse(self.user.check_password("wrongpassword"))

    def test_user_representation(self):
        self.assertEqual(repr(self.user), "<User testuser>")

if __name__ == '__main__':
    unittest.main()
