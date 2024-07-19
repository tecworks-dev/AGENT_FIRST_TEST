
import traceback
from database import execute_query
from encryption import encrypt_message, decrypt_message

def store_message(sender_id, receiver_id, content):
    """
    Stores an encrypted message in the database.

    Args:
    sender_id (int): The ID of the message sender.
    receiver_id (int): The ID of the message receiver.
    content (str): The content of the message.

    Returns:
    bool: True if the message was stored successfully, False otherwise.
    """
    try:
        # Encrypt the message content
        encrypted_content = encrypt_message(content, receiver_id)  # Assuming receiver's public key is their ID for simplicity

        # SQL query to insert the message
        query = """
        INSERT INTO messages (sender_id, receiver_id, content, timestamp)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        """
        params = (sender_id, receiver_id, encrypted_content)

        # Execute the query
        execute_query(query, params)
        return True
    except Exception as e:
        print(f"Error storing message: {str(e)}")
        traceback.print_exc()
        return False

def retrieve_messages(user_id, other_user_id):
    """
    Retrieves and decrypts message history between two users.

    Args:
    user_id (int): The ID of the current user.
    other_user_id (int): The ID of the other user in the conversation.

    Returns:
    list: A list of decrypted messages in chronological order.
    """
    try:
        # SQL query to retrieve messages
        query = """
        SELECT sender_id, receiver_id, content, timestamp
        FROM messages
        WHERE (sender_id = %s AND receiver_id = %s)
        OR (sender_id = %s AND receiver_id = %s)
        ORDER BY timestamp ASC
        """
        params = (user_id, other_user_id, other_user_id, user_id)

        # Execute the query
        results = execute_query(query, params)

        # Decrypt messages
        decrypted_messages = []
        for row in results:
            sender_id, receiver_id, encrypted_content, timestamp = row
            decrypted_content = decrypt_message(encrypted_content, user_id)  # Assuming user's private key is their ID for simplicity
            decrypted_messages.append({
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'content': decrypted_content,
                'timestamp': timestamp
            })

        return decrypted_messages
    except Exception as e:
        print(f"Error retrieving messages: {str(e)}")
        traceback.print_exc()
        return []

def search_messages(user_id, query):
    """
    Searches messages for a given query.

    Args:
    user_id (int): The ID of the user performing the search.
    query (str): The search query.

    Returns:
    list: A list of messages matching the search query.
    """
    try:
        # SQL query to retrieve all messages for the user
        query_all_messages = """
        SELECT sender_id, receiver_id, content, timestamp
        FROM messages
        WHERE sender_id = %s OR receiver_id = %s
        ORDER BY timestamp DESC
        """
        params = (user_id, user_id)

        # Execute the query
        results = execute_query(query_all_messages, params)

        # Decrypt messages and search
        matching_messages = []
        for row in results:
            sender_id, receiver_id, encrypted_content, timestamp = row
            decrypted_content = decrypt_message(encrypted_content, user_id)  # Assuming user's private key is their ID for simplicity
            
            # Check if the decrypted content contains the search query
            if query.lower() in decrypted_content.lower():
                matching_messages.append({
                    'sender_id': sender_id,
                    'receiver_id': receiver_id,
                    'content': decrypted_content,
                    'timestamp': timestamp
                })

        return matching_messages
    except Exception as e:
        print(f"Error searching messages: {str(e)}")
        traceback.print_exc()
        return []
