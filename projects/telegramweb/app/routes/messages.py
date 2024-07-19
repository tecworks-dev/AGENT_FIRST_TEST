from flask import Blueprint, request, jsonify
from app.services.messages import MessageService
from flask_login import current_user, login_required

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    if request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        sender_id = current_user.id
        receiver_id = data.get('receiver_id')
        content = data.get('content')
        
        if not all([receiver_id, content]):
            missing_fields = []
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
@login_required
def message(message_id):
    # Existing logic for GET, PUT, DELETE (unchanged)
    pass