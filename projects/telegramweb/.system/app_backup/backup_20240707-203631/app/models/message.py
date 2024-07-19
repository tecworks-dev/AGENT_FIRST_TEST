
# app/models/message.py

"""
Defines the Message model for the messaging platform.

This module contains the Message class, which represents a message in the system.
It includes attributes such as sender_id, receiver_id, content, and timestamp.
"""

from app.extensions import db
from datetime import datetime
import traceback

class Message(db.Model):
    """
    Message model representing a message in the system.

    Attributes:
        id (int): The unique identifier for the message.
        sender_id (int): The ID of the user who sent the message.
        receiver_id (int): The ID of the user who received the message.
        content (str): The content of the message.
        timestamp (datetime): The date and time when the message was sent.
    """

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, sender_id, receiver_id, content):
        """
        Initialize a new Message instance.

        Args:
            sender_id (int): The ID of the user sending the message.
            receiver_id (int): The ID of the user receiving the message.
            content (str): The content of the message.
        """
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content

    def __repr__(self):
        """
        Return a string representation of the Message instance.

        Returns:
            str: A string representation of the Message.
        """
        return f'<Message {self.id}: from {self.sender_id} to {self.receiver_id}>'

    def to_dict(self):
        """
        Convert the Message instance to a dictionary.

        Returns:
            dict: A dictionary representation of the Message.
        """
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data):
        """
        Create a new Message instance from a dictionary.

        Args:
            data (dict): A dictionary containing message data.

        Returns:
            Message: A new Message instance.
        """
        return Message(
            sender_id=data['sender_id'],
            receiver_id=data['receiver_id'],
            content=data['content']
        )

    @staticmethod
    def get_messages_between_users(user1_id, user2_id, limit=50):
        """
        Retrieve messages between two users.

        Args:
            user1_id (int): The ID of the first user.
            user2_id (int): The ID of the second user.
            limit (int): The maximum number of messages to retrieve (default: 50).

        Returns:
            list: A list of Message instances.
        """
        try:
            messages = Message.query.filter(
                ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) |
                ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
            ).order_by(Message.timestamp.desc()).limit(limit).all()
            return messages
        except Exception as e:
            print(f"Error retrieving messages: {str(e)}")
            traceback.print_exc()
            return []

# Add debugging statements
if __name__ == '__main__':
    DEBUG = True
    if DEBUG:
        print("Message model loaded successfully")
        print("Available attributes:", Message.__dict__.keys())
