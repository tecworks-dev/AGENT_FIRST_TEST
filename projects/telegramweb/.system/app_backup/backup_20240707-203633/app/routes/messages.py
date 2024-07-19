from flask import Blueprint, request, jsonify, current_app
from app.services.messages import MessageService
from flask_login import current_user, login_required

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages', methods=['GET', 'POST'])
@login_required
def handle_messages():
    """
    Handle GET and POST requests for messages.
    GET: Retrieve messages for a user.
    POST: Send a new message.
    """
    try:
        if request.method == 'GET':
            user_id = current_user.id
            messages = MessageService.get_messages(user_id)
            return jsonify(messages), 200
        elif request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            sender_id = current_user.id
            receiver_id = data.get('receiver_id')
            content = data.get('content')
            
            if not all([receiver_id, content]):
                return jsonify({"error": "Missing required fields"}), 400
            
            message = MessageService.send_message(sender_id, receiver_id, content)
            return jsonify(message), 201
    except Exception as e:
        current_app.logger.error(f"Error in handle_messages: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@messages_bp.route('/messages/<int:message_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def handle_message(message_id):
    """
    Handle GET, PUT, and DELETE requests for a specific message.
    GET: Retrieve a specific message.
    PUT: Update a specific message.
    DELETE: Delete a specific message.
    """
    try:
        if request.method == 'GET':
            message = MessageService.get_message(message_id)
            if message:
                return jsonify(message), 200
            return jsonify({"error": "Message not found"}), 404
        
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            content = data.get('content')
            
            if not content:
                return jsonify({"error": "Missing content field"}), 400
            
            updated_message = MessageService.update_message(message_id, content)
            if updated_message:
                return jsonify(updated_message), 200
            return jsonify({"error": "Message not found or update failed"}), 404
        
        elif request.method == 'DELETE':
            success = MessageService.delete_message(message_id)
            if success:
                return jsonify({"message": "Message deleted successfully"}), 200
            return jsonify({"error": "Message not found or delete failed"}), 404
    
    except Exception as e:
        current_app.logger.error(f"Error in handle_message: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500