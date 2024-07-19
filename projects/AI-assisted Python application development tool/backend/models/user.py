
# User model for the secure messaging platform
# This file defines the User class, representing users in the system

from flask_sqlalchemy import SQLAlchemy
from backend.database import db
import datetime
import unittest

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_login = db.Column(db.DateTime)
    two_factor_secret = db.Column(db.String(32))

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

# Unit tests for the User model
class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.user = User('testuser', 'test@example.com', 'password_hash')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.password_hash, 'password_hash')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_admin)

    def test_user_representation(self):
        self.assertEqual(repr(self.user), '<User testuser>')

    def test_user_to_dict(self):
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict['username'], 'testuser')
        self.assertEqual(user_dict['email'], 'test@example.com')
        self.assertTrue(user_dict['is_active'])
        self.assertFalse(user_dict['is_admin'])

if __name__ == '__main__':
    unittest.main()
