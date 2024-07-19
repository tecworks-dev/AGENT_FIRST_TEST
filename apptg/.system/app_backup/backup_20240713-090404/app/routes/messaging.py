
"""
Purpose: Routes for one-on-one messaging.
This file contains the routes and logic for sending and retrieving messages between users.
"""

import traceback
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models import Message, User
from app.services import encryption
from app import db

messaging = Blueprint('messaging', __name__)

@messaging.route('/send/<int:recipient_id>', methods=['POST'])
@login_required
def send_message(recipient_id):
    """
    Sends a message to a user.
    
    Args:
        recipient_id (int): The ID of the recipient user.
    
    Returns:
        JSON response with status and message.
    """
    try:
        if current_app.config['DEBUG']:
            print(f"Attempting to send message to user {recipient_id}")

        recipient = User.query.get(recipient_id)
        if not recipient:
            return jsonify({"status": "error", "message": "Recipient not found"}), 404

        content = request.json.get('content')
        if not content:
            return jsonify({"status": "error", "message": "Message content is required"}), 400

        # Encrypt the message content
        encrypted_content = encryption.encrypt_message(content, recipient.public_key)

        new_message = Message(
            sender_id=current_user.id,
            recipient_id=recipient_id,
            content=encrypted_content
        )
        db.session.add(new_message)
        db.session.commit()

        if current_app.config['DEBUG']:
            print(f"Message sent successfully to user {recipient_id}")

        return jsonify({"status": "success", "message": "Message sent successfully"}), 200
    except Exception as e:
        if current_app.config['DEBUG']:
            print(f"Error sending message: {str(e)}")
            traceback.print_exc()
        return jsonify({"status": "error", "message": "An error occurred while sending the message"}), 500

@messaging.route('/messages/<int:user_id>', methods=['GET'])
@login_required
def get_messages(user_id):
    """
    Retrieves messages for a conversation between the current user and the specified user.
    
    Args:
        user_id (int): The ID of the user to retrieve messages with.
    
    Returns:
        JSON response with status and list of messages.
    """
    try:
        if current_app.config['DEBUG']:
            print(f"Retrieving messages with user {user_id}")

        other_user = User.query.get(user_id)
        if not other_user:
            return jsonify({"status": "error", "message": "User not found"}), 404

        messages = Message.query.filter(
            ((Message.sender_id == current_user.id) & (Message.recipient_id == user_id)) |
            ((Message.sender_id == user_id) & (Message.recipient_id == current_user.id))
        ).order_by(Message.timestamp.asc()).all()

        decrypted_messages = []
        for message in messages:
            decrypted_content = encryption.decrypt_message(message.content, current_user.private_key)
            decrypted_messages.append({
                "id": message.id,
                "sender_id": message.sender_id,
                "recipient_id": message.recipient_id,
                "content": decrypted_content,
                "timestamp": message.timestamp.isoformat()
            })

        if current_app.config['DEBUG']:
            print(f"Retrieved {len(decrypted_messages)} messages with user {user_id}")

        return jsonify({"status": "success", "messages": decrypted_messages}), 200
    except Exception as e:
        if current_app.config['DEBUG']:
            print(f"Error retrieving messages: {str(e)}")
            traceback.print_exc()
        return jsonify({"status": "error", "message": "An error occurred while retrieving messages"}), 500

# Unit tests
import unittest
from app import create_app, db
from app.models import User, Message

class MessagingRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test users
        self.user1 = User(username='testuser1', email='test1@example.com')
        self.user1.set_password('password1')
        self.user2 = User(username='testuser2', email='test2@example.com')
        self.user2.set_password('password2')
        db.session.add_all([self.user1, self.user2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_send_message(self):
        with self.client:
            # Login as user1
            self.client.post('/auth/login', json={
                'email': 'test1@example.com',
                'password': 'password1'
            })

            # Send a message to user2
            response = self.client.post(f'/messaging/send/{self.user2.id}', json={
                'content': 'Hello, User2!'
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')

    def test_get_messages(self):
        with self.client:
            # Login as user1
            self.client.post('/auth/login', json={
                'email': 'test1@example.com',
                'password': 'password1'
            })

            # Send a message to user2
            self.client.post(f'/messaging/send/{self.user2.id}', json={
                'content': 'Hello, User2!'
            })

            # Get messages between user1 and user2
            response = self.client.get(f'/messaging/messages/{self.user2.id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertEqual(len(response.json['messages']), 1)

if __name__ == '__main__':
    unittest.main()
