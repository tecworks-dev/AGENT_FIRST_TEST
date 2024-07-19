import traceback
from datetime import datetime

# In-memory storage for messages (replace with database in production)
messages = []

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
        messages.append(message)

        # In a real application, you would store this message in a database
        print(f"New message: {message}")

    except Exception as e:
        print(f"Error in handle_message: {str(e)}")
        traceback.print_exc()

def get_recent_messages(limit=50):
    """
    Retrieves recent messages.
    """
    return messages[-limit:]