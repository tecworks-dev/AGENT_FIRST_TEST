# messaging.py
# Purpose: Manages secure messaging with end-to-end encryption and self-destructing messages.
# Description: This module provides functions for sending encrypted messages, retrieving messages,
#              and setting self-destruct timers for messages.

import traceback
from flask import current_app
import base64
from database import get_db_connection
from config import DEBUG
import time

def send_message(sender_id, recipient_id, message):
    """
    Send an encoded message from sender to recipient.
    
    Args:
    sender_id (int): ID of the sender
    recipient_id (int): ID of the recipient
    message (str): The message to be sent
    
    Returns:
    bool: True if message sent successfully, False otherwise
    """
    try:
        if DEBUG:
            print(f"Sending message from {sender_id} to {recipient_id}")
        
        # Encode the message using base64
        encoded_message = base64.b64encode(message.encode()).decode()
        
        # Store the encoded message in the database
        conn = get_db_connection()
        cursor = conn.execute("""
            INSERT INTO messages (sender_id, recipient_id, encoded_message)
            VALUES (?, ?, ?)
        """, (sender_id, recipient_id, encoded_message))
        conn.commit()
        
        if DEBUG:
            print("Message sent successfully")
        
        return True
    except Exception as e:
        current_app.logger.error(f"Error in send_message: {str(e)}")
        if DEBUG:
            print(f"Error in send_message: {str(e)}")
            traceback.print_exc()
        return False

def retrieve_messages(user_id):
    """
    Retrieve and decode messages for a given user.
    
    Args:
    user_id (int): ID of the user retrieving messages
    
    Returns:
    list: List of decoded messages
    """
    try:
        if DEBUG:
            print(f"Retrieving messages for user {user_id}")
        
        conn = get_db_connection()
        cursor = conn.execute("""
            SELECT sender_id, encoded_message, timestamp
            FROM messages
            WHERE recipient_id = ?
            ORDER BY timestamp DESC
        """, (user_id,))
        messages = cursor.fetchall()
        
        decoded_messages = []
        for sender_id, encoded_message, timestamp in messages:
            decoded_message = base64.b64decode(encoded_message).decode()
            decoded_messages.append({
                'sender_id': sender_id,
                'message': decoded_message,
                'timestamp': timestamp
            })
        
        if DEBUG:
            print(f"Retrieved {len(decoded_messages)} messages")
        
        return decoded_messages
    except Exception as e:
        current_app.logger.error(f"Error in retrieve_messages: {str(e)}")
        if DEBUG:
            print(f"Error in retrieve_messages: {str(e)}")
            traceback.print_exc()
        return []

def set_self_destruct(message_id, destruct_time):
    """
    Set a self-destruct timer for a specific message.
    
    Args:
    message_id (int): ID of the message
    destruct_time (int): Time in seconds after which the message should be destroyed
    
    Returns:
    bool: True if self-destruct timer set successfully, False otherwise
    """
    try:
        if DEBUG:
            print(f"Setting self-destruct timer for message {message_id}")
        
        conn = get_db_connection()
        
        # Set the self-destruct time for the message
        destruct_timestamp = int(time.time()) + destruct_time
        conn.execute("""
            UPDATE messages
            SET self_destruct_time = ?
            WHERE id = ?
        """, (destruct_timestamp, message_id))
        
        conn.commit()
        
        if DEBUG:
            print(f"Self-destruct timer set for message {message_id}")
        
        return True
    except Exception as e:
        current_app.logger.error(f"Error in set_self_destruct: {str(e)}")
        if DEBUG:
            print(f"Error in set_self_destruct: {str(e)}")
            traceback.print_exc()
        return False

# Function to periodically check and delete self-destructed messages
def cleanup_self_destructed_messages():
    try:
        if DEBUG:
            print("Cleaning up self-destructed messages")
        
        conn = get_db_connection()
        
        current_time = int(time.time())
        cursor = conn.execute("""
            DELETE FROM messages
            WHERE self_destruct_time IS NOT NULL AND self_destruct_time <= ?
        """, (current_time,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        
        if DEBUG:
            print(f"Deleted {deleted_count} self-destructed messages")
        
    except Exception as e:
        current_app.logger.error(f"Error in cleanup_self_destructed_messages: {str(e)}")
        if DEBUG:
            print(f"Error in cleanup_self_destructed_messages: {str(e)}")
            traceback.print_exc()

# This function should be called periodically, e.g., using a background task scheduler