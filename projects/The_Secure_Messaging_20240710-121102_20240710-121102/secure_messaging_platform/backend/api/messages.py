
# Purpose: Handle message-related operations for the Secure Messaging Platform
# Description: This module provides API endpoints for sending and receiving messages

import traceback
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.message import Message
from ..models.user import User
from ..extensions import db
from ..services.encryption import encrypt_message, decrypt_message

messages = Blueprint('messages', __name__)

@messages.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    """
    Send a new message
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'recipient_id' not in data or 'content' not in data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        recipient = User.query.get(data['recipient_id'])
        if not recipient:
            return jsonify({'error': 'Recipient not found'}), 404
        
        # Encrypt the message content
        encrypted_content = encrypt_message(data['content'], recipient.encryption_key)
        
        new_message = Message(
            sender_id=current_user_id,
            recipient_id=data['recipient_id'],
            content=encrypted_content
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify({'message': 'Message sent successfully'}), 201
    
    except Exception as e:
        db.session.rollback()
        if __debug__:
            print(f"Error in send_message: {str(e)}")
            traceback.print_exc()
        return jsonify({'error': 'An error occurred while sending the message'}), 500

@messages.route('/receive', methods=['GET'])
@jwt_required()
def receive_messages():
    """
    Receive messages for the current user
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Fetch unread messages for the current user
        unread_messages = Message.query.filter_by(recipient_id=current_user_id, is_read=False).all()
        
        messages_data = []
        for message in unread_messages:
            # Decrypt the message content
            decrypted_content = decrypt_message(message.content, current_user.encryption_key)
            messages_data.append({
                'id': message.id,
                'sender_id': message.sender_id,
                'content': decrypted_content,
                'timestamp': message.timestamp.isoformat()
            })
            
            # Mark the message as read
            message.is_read = True
        
        db.session.commit()
        
        return jsonify({'messages': messages_data}), 200
    
    except Exception as e:
        db.session.rollback()
        if __debug__:
            print(f"Error in receive_messages: {str(e)}")
            traceback.print_exc()
        return jsonify({'error': 'An error occurred while fetching messages'}), 500

# Debug route to test the messages functionality
if __debug__:
    @messages.route('/debug', methods=['GET'])
    def debug_messages():
        return jsonify({'status': 'Messages module is working'}), 200

# Add unit tests
import unittest
from unittest.mock import patch, MagicMock

class TestMessages(unittest.TestCase):
    
    @patch('flask_jwt_extended.get_jwt_identity')
    @patch('secure_messaging_platform.backend.models.user.User.query')
    @patch('secure_messaging_platform.backend.services.encryption.encrypt_message')
    def test_send_message(self, mock_encrypt, mock_user_query, mock_get_jwt_identity):
        # Set up mocks
        mock_get_jwt_identity.return_value = 1
        mock_user_query.get.return_value = MagicMock(encryption_key='test_key')
        mock_encrypt.return_value = b'encrypted_content'
        
        # Test the send_message function
        with messages.test_request_context('/send', method='POST', json={
            'recipient_id': 2,
            'content': 'Test message'
        }):
            response = send_message()
            self.assertEqual(response[1], 201)
    
    @patch('flask_jwt_extended.get_jwt_identity')
    @patch('secure_messaging_platform.backend.models.user.User.query')
    @patch('secure_messaging_platform.backend.models.message.Message.query')
    @patch('secure_messaging_platform.backend.services.encryption.decrypt_message')
    def test_receive_messages(self, mock_decrypt, mock_message_query, mock_user_query, mock_get_jwt_identity):
        # Set up mocks
        mock_get_jwt_identity.return_value = 1
        mock_user_query.get.return_value = MagicMock(encryption_key='test_key')
        mock_message = MagicMock(id=1, sender_id=2, content=b'encrypted_content', timestamp='2023-05-01T12:00:00')
        mock_message_query.filter_by.return_value.all.return_value = [mock_message]
        mock_decrypt.return_value = 'decrypted_content'
        
        # Test the receive_messages function
        with messages.test_request_context('/receive', method='GET'):
            response = receive_messages()
            self.assertEqual(response[1], 200)

if __name__ == '__main__':
    unittest.main()
