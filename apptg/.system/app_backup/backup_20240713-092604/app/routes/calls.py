
# Purpose: Routes for voice and video calling features
# Description: This file contains Flask routes for initiating and ending voice and video calls

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services import websocket
import traceback

calls = Blueprint('calls', __name__)

DEBUG = True

@calls.route('/initiate_call/<int:user_id>', methods=['POST'])
@login_required
def initiate_call(user_id):
    """
    Initiates a call with another user
    """
    try:
        # Check if the user exists and is available
        # This should be implemented in a user service
        if not user_exists(user_id):
            return jsonify({'error': 'User not found'}), 404
        
        if not user_available(user_id):
            return jsonify({'error': 'User is not available'}), 400

        # Generate a unique call ID
        call_id = generate_call_id()

        # Initialize the call using WebSocket service
        websocket.initialize_call(current_user.id, user_id, call_id)

        if DEBUG:
            print(f"Initiating call: {current_user.id} -> {user_id}, Call ID: {call_id}")

        return jsonify({
            'message': 'Call initiated successfully',
            'call_id': call_id
        }), 200

    except Exception as e:
        if DEBUG:
            print(f"Error in initiate_call: {str(e)}")
            traceback.print_exc()
        return jsonify({'error': 'An error occurred while initiating the call'}), 500

@calls.route('/end_call/<string:call_id>', methods=['POST'])
@login_required
def end_call(call_id):
    """
    Ends an ongoing call
    """
    try:
        # Verify that the call exists and the current user is part of it
        if not call_exists(call_id):
            return jsonify({'error': 'Call not found'}), 404
        
        if not user_in_call(current_user.id, call_id):
            return jsonify({'error': 'User is not part of this call'}), 403

        # End the call using WebSocket service
        websocket.end_call(call_id)

        if DEBUG:
            print(f"Ending call: {call_id}, User: {current_user.id}")

        return jsonify({'message': 'Call ended successfully'}), 200

    except Exception as e:
        if DEBUG:
            print(f"Error in end_call: {str(e)}")
            traceback.print_exc()
        return jsonify({'error': 'An error occurred while ending the call'}), 500

# Helper functions (these should be implemented in appropriate services)
def user_exists(user_id):
    # Check if user exists in the database
    # This is a placeholder and should be implemented
    return True

def user_available(user_id):
    # Check if user is available for a call
    # This is a placeholder and should be implemented
    return True

def generate_call_id():
    # Generate a unique call ID
    # This is a placeholder and should be implemented
    import uuid
    return str(uuid.uuid4())

def call_exists(call_id):
    # Check if the call exists
    # This is a placeholder and should be implemented
    return True

def user_in_call(user_id, call_id):
    # Check if the user is part of the call
    # This is a placeholder and should be implemented
    return True

# Unit tests
import unittest
from app import create_app
from app.models import User
from flask_login import login_user

class CallRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create a test user and log them in
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password')
        login_user(self.user)

    def tearDown(self):
        self.app_context.pop()

    def test_initiate_call(self):
        response = self.client.post('/initiate_call/2')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('call_id', data)

    def test_end_call(self):
        # First initiate a call
        init_response = self.client.post('/initiate_call/2')
        call_id = init_response.get_json()['call_id']

        # Then end the call
        end_response = self.client.post(f'/end_call/{call_id}')
        self.assertEqual(end_response.status_code, 200)
        data = end_response.get_json()
        self.assertEqual(data['message'], 'Call ended successfully')

if __name__ == '__main__':
    unittest.main()
