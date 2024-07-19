
# Channel model definition for broadcast communications
# This file defines the Channel model for managing broadcast channels in the application

from app import db
from datetime import datetime
import unittest

class Channel(db.Model):
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(500))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = db.relationship('User', back_populates='created_channels', foreign_keys=[creator_id])
    subscribers = db.relationship('User', secondary='channel_subscribers', back_populates='subscribed_channels')
    messages = db.relationship('Message', back_populates='channel', cascade='all, delete-orphan')

    def __init__(self, name, description, creator_id):
        self.name = name
        self.description = description
        self.creator_id = creator_id

    def __repr__(self):
        return f'<Channel {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'creator_id': self.creator_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'subscriber_count': len(self.subscribers)
        }

    def add_subscriber(self, user):
        if user not in self.subscribers:
            self.subscribers.append(user)

    def remove_subscriber(self, user):
        if user in self.subscribers:
            self.subscribers.remove(user)

# Association table for channel subscribers
channel_subscribers = db.Table('channel_subscribers',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('channel_id', db.Integer, db.ForeignKey('channels.id'), primary_key=True)
)

# Unit tests for the Channel model
class TestChannelModel(unittest.TestCase):
    def setUp(self):
        self.channel = Channel(name="Test Channel", description="This is a test channel", creator_id=1)

    def test_channel_creation(self):
        self.assertEqual(self.channel.name, "Test Channel")
        self.assertEqual(self.channel.description, "This is a test channel")
        self.assertEqual(self.channel.creator_id, 1)

    def test_channel_repr(self):
        self.assertEqual(repr(self.channel), "<Channel Test Channel>")

    def test_channel_to_dict(self):
        channel_dict = self.channel.to_dict()
        self.assertIsInstance(channel_dict, dict)
        self.assertEqual(channel_dict['name'], "Test Channel")
        self.assertEqual(channel_dict['description'], "This is a test channel")
        self.assertEqual(channel_dict['creator_id'], 1)

if __name__ == '__main__':
    unittest.main()
