
# Purpose: Group model definition for managing group chats
# Description: This file defines the Group model using SQLAlchemy ORM

import traceback
from app import db
from datetime import datetime
import unittest
from app.models.user import User  # Import User model to avoid circular imports

DEBUG = True

# Define the association table
group_members = db.Table('group_members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
)

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    creator = db.relationship('User', back_populates='created_groups', foreign_keys=[creator_id])
    members = db.relationship('User', secondary=group_members, backref=db.backref('groups', lazy='dynamic'))
    messages = db.relationship('Message', backref='group', lazy='dynamic')

    def __init__(self, name, description, creator_id):
        self.name = name
        self.description = description
        self.creator_id = creator_id

    def __repr__(self):
        return f'<Group {self.name}>'

    # ... (rest of the methods remain unchanged)

# Unit tests for the Group model
class TestGroup(unittest.TestCase):
    def setUp(self):
        self.group = Group(name="Test Group", description="A test group", creator_id=1)

    def test_group_creation(self):
        self.assertEqual(self.group.name, "Test Group")
        self.assertEqual(self.group.description, "A test group")
        self.assertEqual(self.group.creator_id, 1)

    def test_group_representation(self):
        self.assertEqual(repr(self.group), "<Group Test Group>")

    # Add more unit tests for other methods as needed

if __name__ == '__main__':
    unittest.main()
