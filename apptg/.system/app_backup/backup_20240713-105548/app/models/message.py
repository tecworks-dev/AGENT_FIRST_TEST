
# Purpose: Message model definition for storing chat messages
# Description: This file defines the Message model using SQLAlchemy ORM

from app import db
from datetime import datetime
import traceback

DEBUG = True

class Message(db.Model):
    """Message model for storing chat messages"""
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    is_encrypted = db.Column(db.Boolean, default=True)

    # Add the relationship to Channel
    channel = db.relationship('Channel', back_populates='messages')

    def __init__(self, content, sender_id, recipient_id, group_id=None, channel_id=None, is_encrypted=True):
        self.content = content
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.group_id = group_id
        self.channel_id = channel_id
        self.is_encrypted = is_encrypted

    def __repr__(self):
        return f'<Message {self.id}>'

    def to_dict(self):
        """Convert message to dictionary for API responses"""
        try:
            return {
                'id': self.id,
                'content': self.content,
                'timestamp': self.timestamp.isoformat(),
                'sender_id': self.sender_id,
                'recipient_id': self.recipient_id,
                'group_id': self.group_id,
                'channel_id': self.channel_id,
                'is_encrypted': self.is_encrypted
            }
        except Exception as e:
            if DEBUG:
                print(f"Error in Message.to_dict(): {str(e)}")
                traceback.print_exc()
            return None

    @staticmethod
    def from_dict(data):
        """Create a new Message instance from a dictionary"""
        try:
            return Message(
                content=data['content'],
                sender_id=data['sender_id'],
                recipient_id=data['recipient_id'],
                group_id=data.get('group_id'),
                channel_id=data.get('channel_id'),
                is_encrypted=data.get('is_encrypted', True)
            )
        except KeyError as e:
            if DEBUG:
                print(f"Missing key in Message.from_dict(): {str(e)}")
                traceback.print_exc()
            return None
        except Exception as e:
            if DEBUG:
                print(f"Error in Message.from_dict(): {str(e)}")
                traceback.print_exc()
            return None

# Add unittest for Message model
import unittest

class TestMessageModel(unittest.TestCase):
    def setUp(self):
        self.message_data = {
            'content': 'Test message',
            'sender_id': 1,
            'recipient_id': 2,
            'group_id': None,
            'channel_id': None,
            'is_encrypted': True
        }

    def test_message_creation(self):
        message = Message.from_dict(self.message_data)
        self.assertIsNotNone(message)
        self.assertEqual(message.content, 'Test message')
        self.assertEqual(message.sender_id, 1)
        self.assertEqual(message.recipient_id, 2)
        self.assertIsNone(message.group_id)
        self.assertIsNone(message.channel_id)
        self.assertTrue(message.is_encrypted)

    def test_message_to_dict(self):
        message = Message.from_dict(self.message_data)
        message_dict = message.to_dict()
        self.assertIsNotNone(message_dict)
        self.assertEqual(message_dict['content'], 'Test message')
        self.assertEqual(message_dict['sender_id'], 1)
        self.assertEqual(message_dict['recipient_id'], 2)
        self.assertIsNone(message_dict['group_id'])
        self.assertIsNone(message_dict['channel_id'])
        self.assertTrue(message_dict['is_encrypted'])

    def test_message_creation_with_missing_data(self):
        incomplete_data = {
            'content': 'Incomplete message',
            'sender_id': 1
        }
        message = Message.from_dict(incomplete_data)
        self.assertIsNone(message)

if __name__ == '__main__':
    unittest.main()
