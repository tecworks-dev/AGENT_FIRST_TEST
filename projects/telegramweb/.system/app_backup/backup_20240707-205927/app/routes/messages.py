from flask import Blueprint, request, jsonify
from app.services.messages import MessageService

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        content = data.get('content')
        
        if not all([sender_id, receiver_id, content]):
            missing_fields = []
            if not sender_id:
                missing_fields.append('sender_id')
            if not receiver_id:
                missing_fields.append('receiver_id')
            if not content:
                missing_fields.append('content')
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
        
        message = MessageService.send_message(sender_id, receiver_id, content)
        return jsonify(message), 201
    else:
        # GET request logic (unchanged)
        pass

@messages_bp.route('/messages/<int:message_id>', methods=['GET', 'PUT', 'DELETE'])
def message(message_id):
    # Existing logic for GET, PUT, DELETE (unchanged)
    pass