
# Purpose: Manages WebSocket connections for real-time communication
# Description: This module handles WebSocket connections, room management, and message handling for real-time communication in the application.

import traceback
from flask_socketio import emit, join_room, leave_room
from flask import current_app
from app.models.user import User
from app.models.message import Message
from app.services import encryption
from app import socketio

DEBUG = True

@socketio.on('connect')
def handle_connect():
    """
    Handles new WebSocket connections.
    """
    if DEBUG:
        print("New WebSocket connection established")
    try:
        # Add any connection handling logic here
        emit('connect_response', {'data': 'Connected'})
    except Exception as e:
        current_app.logger.error(f"Error in handle_connect: {str(e)}")
        if DEBUG:
            print(f"Error in handle_connect: {traceback.format_exc()}")

@socketio.on('disconnect')
def handle_disconnect():
    """
    Handles WebSocket disconnections.
    """
    if DEBUG:
        print("WebSocket disconnected")
    try:
        # Add any disconnection handling logic here
        emit('disconnect_response', {'data': 'Disconnected'})
    except Exception as e:
        current_app.logger.error(f"Error in handle_disconnect: {str(e)}")
        if DEBUG:
            print(f"Error in handle_disconnect: {traceback.format_exc()}")

@socketio.on('join')
def handle_join_room(data):
    """
    Handles joining a room.

    Args:
        data (dict): The data containing the room identifier to join.
    """
    room = data.get('room')
    if DEBUG:
        print(f"Joining room: {room}")
    try:
        join_room(room)
        emit('room_join_response', {'data': f'Joined room {room}'}, room=room)
    except Exception as e:
        current_app.logger.error(f"Error in handle_join_room: {str(e)}")
        if DEBUG:
            print(f"Error in handle_join_room: {traceback.format_exc()}")

@socketio.on('leave')
def handle_leave_room(data):
    """
    Handles leaving a room.

    Args:
        data (dict): The data containing the room identifier to leave.
    """
    room = data.get('room')
    if DEBUG:
        print(f"Leaving room: {room}")
    try:
        leave_room(room)
        emit('room_leave_response', {'data': f'Left room {room}'}, room=room)
    except Exception as e:
        current_app.logger.error(f"Error in handle_leave_room: {str(e)}")
        if DEBUG:
            print(f"Error in handle_leave_room: {traceback.format_exc()}")

@socketio.on('message')
def handle_message(data):
    """
    Handles incoming messages.

    Args:
        data (dict): The message data containing sender_id, recipient_id, and message content.
    """
    if DEBUG:
        print(f"Received message: {data}")
    try:
        sender_id = data.get('sender_id')
        recipient_id = data.get('recipient_id')
        content = data.get('content')
        
        # Encrypt the message content
        encrypted_content = encryption.encrypt_message(content, current_app.config['ENCRYPTION_KEY'])
        
        # Save the message to the database
        message = Message(sender_id=sender_id, recipient_id=recipient_id, content=encrypted_content)
        current_app.db.session.add(message)
        current_app.db.session.commit()
        
        # Emit the message to the recipient
        recipient_room = f"user_{recipient_id}"
        emit('new_message', {
            'sender_id': sender_id,
            'content': content,
            'timestamp': message.timestamp.isoformat()
        }, room=recipient_room)
        
    except Exception as e:
        current_app.logger.error(f"Error in handle_message: {str(e)}")
        if DEBUG:
            print(f"Error in handle_message: {traceback.format_exc()}")

# Unit tests
import unittest
from unittest.mock import patch, MagicMock

class TestWebSocket(unittest.TestCase):
    
    @patch('app.services.websocket.emit')
    def test_handle_connect(self, mock_emit):
        handle_connect()
        mock_emit.assert_called_once_with('connect_response', {'data': 'Connected'})
    
    @patch('app.services.websocket.emit')
    def test_handle_disconnect(self, mock_emit):
        handle_disconnect()
        mock_emit.assert_called_once_with('disconnect_response', {'data': 'Disconnected'})
    
    @patch('app.services.websocket.join_room')
    @patch('app.services.websocket.emit')
    def test_handle_join_room(self, mock_emit, mock_join_room):
        data = {'room': 'test_room'}
        handle_join_room(data)
        mock_join_room.assert_called_once_with('test_room')
        mock_emit.assert_called_once_with('room_join_response', {'data': 'Joined room test_room'}, room='test_room')
    
    @patch('app.services.websocket.leave_room')
    @patch('app.services.websocket.emit')
    def test_handle_leave_room(self, mock_emit, mock_leave_room):
        data = {'room': 'test_room'}
        handle_leave_room(data)
        mock_leave_room.assert_called_once_with('test_room')
        mock_emit.assert_called_once_with('room_leave_response', {'data': 'Left room test_room'}, room='test_room')
    
    @patch('app.services.websocket.current_app')
    @patch('app.services.websocket.encryption')
    @patch('app.services.websocket.emit')
    def test_handle_message(self, mock_emit, mock_encryption, mock_current_app):
        mock_db = MagicMock()
        mock_current_app.db = mock_db
        mock_current_app.config = {'ENCRYPTION_KEY': 'test_key'}
        mock_encryption.encrypt_message.return_value = 'encrypted_content'
        
        data = {
            'sender_id': 1,
            'recipient_id': 2,
            'content': 'Hello, World!'
        }
        handle_message(data)
        
        mock_encryption.encrypt_message.assert_called_once_with('Hello, World!', 'test_key')
        mock_db.session.add.assert_called_once()
        mock_db.session.commit.assert_called_once()
        mock_emit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
