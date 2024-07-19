import traceback
from datetime import datetime
from flask_socketio import emit
from database import execute_query

def handle_message(data):
    """
    Processes incoming messages.
    """
    try:
        sender_id = data.get('sender_id')
        content = data.get('content')
        timestamp = datetime.now().isoformat()

        message = {
            'sender_id': sender_id,
            'content': content,
            'timestamp': timestamp
        }

        # Store message in the database
        query = "INSERT INTO messages (sender_id, content, timestamp) VALUES (?, ?, ?)"
        execute_query(query, (sender_id, content, timestamp))

        print(f"New message: {message}")

        # Emit the message to all connected clients
        emit('new_message', message, broadcast=True)

    except Exception as e:
        print(f"Error in handle_message: {str(e)}")
        traceback.print_exc()

def get_recent_messages(limit=50):
    """
    Retrieves recent messages from the database.
    """
    try:
        query = "SELECT * FROM messages ORDER BY timestamp DESC LIMIT ?"
        messages = execute_query(query, (limit,))
        return [{'sender_id': m[1], 'content': m[2], 'timestamp': m[3]} for m in messages]
    except Exception as e:
        print(f"Error retrieving recent messages: {str(e)}")
        traceback.print_exc()
        return []

def handle_connect(sid):
    """
    Handles new client connections.
    """
    print(f"Client connected: {sid}")

def handle_disconnect(sid):
    """
    Handles client disconnections.
    """
    print(f"Client disconnected: {sid}")