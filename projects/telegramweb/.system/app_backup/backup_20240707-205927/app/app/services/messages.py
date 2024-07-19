# app/services/messages.py

"""
Implements messaging logic.

This module provides functionality for sending, retrieving, updating, and deleting messages.
It also handles message encryption and decryption for secure communication.
"""

import traceback
from app.models.message import Message
from app.utils.encryption import encrypt_message, decrypt_message
from app.extensions import db
from datetime import datetime

class MessageService:
    @staticmethod
    def send_message(sender_id: int, receiver_id: int, content: str) -> dict:
        """
        Send a new message.

        Args:
            sender_id (int): ID of the message sender
            receiver_id (int): ID of the message receiver
            content (str): Content of the message

        Returns:
            dict: Dictionary containing message details
        """
        try:
            encrypted_content = encrypt_message(content, db.app.config['SECRET_KEY'].encode())
            new_message = Message(
                sender_id=sender_id,
                receiver_id=receiver_id,
                content=encrypted_content,
                timestamp=datetime.utcnow()
            )
            db.session.add(new_message)
            db.session.commit()

            return {
                'id': new_message.id,
                'sender_id': new_message.sender_id,
                'receiver_id': new_message.receiver_id,
                'content': content,
                'timestamp': new_message.timestamp.isoformat()
            }
        except Exception as e:
            db.session.rollback()
            print(f"Error sending message: {str(e)}")
            traceback.print_exc()
            raise

    @staticmethod
    def get_message(message_id: int) -> dict:
        """
        Retrieve a message by its ID.

        Args:
            message_id (int): ID of the message to retrieve

        Returns:
            dict: Dictionary containing message details
        """
        try:
            message = Message.query.get(message_id)
            if message:
                decrypted_content = decrypt_message(message.content, db.app.config['SECRET_KEY'].encode())
                return {
                    'id': message.id,
                    'sender_id': message.sender_id,
                    'receiver_id': message.receiver_id,
                    'content': decrypted_content,
                    'timestamp': message.timestamp.isoformat()
                }
            else:
                return None
        except Exception as e:
            print(f"Error retrieving message: {str(e)}")
            traceback.print_exc()
            raise

    @staticmethod
    def update_message(message_id: int, content: str) -> dict:
        """
        Update the content of an existing message.

        Args:
            message_id (int): ID of the message to update
            content (str): New content for the message

        Returns:
            dict: Dictionary containing updated message details
        """
        try:
            message = Message.query.get(message_id)
            if message:
                encrypted_content = encrypt_message(content, db.app.config['SECRET_KEY'].encode())
                message.content = encrypted_content
                db.session.commit()

                return {
                    'id': message.id,
                    'sender_id': message.sender_id,
                    'receiver_id': message.receiver_id,
                    'content': content,
                    'timestamp': message.timestamp.isoformat()
                }
            else:
                return None
        except Exception as e:
            db.session.rollback()
            print(f"Error updating message: {str(e)}")
            traceback.print_exc()
            raise

    @staticmethod
    def delete_message(message_id: int) -> bool:
        """
        Delete a message by its ID.

        Args:
            message_id (int): ID of the message to delete

        Returns:
            bool: True if the message was successfully deleted, False otherwise
        """
        try:
            message = Message.query.get(message_id)
            if message:
                db.session.delete(message)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting message: {str(e)}")
            traceback.print_exc()
            raise

    @staticmethod
    def get_messages(user_id: int) -> list:
        """
        Retrieve all messages for a user.

        Args:
            user_id (int): ID of the user

        Returns:
            list: List of dictionaries containing message details
        """
        try:
            messages = Message.query.filter((Message.sender_id == user_id) | (Message.receiver_id == user_id)).all()
            return [
                {
                    'id': message.id,
                    'sender_id': message.sender_id,
                    'receiver_id': message.receiver_id,
                    'content': decrypt_message(message.content, db.app.config['SECRET_KEY'].encode()),
                    'timestamp': message.timestamp.isoformat()
                }
                for message in messages
            ]
        except Exception as e:
            print(f"Error retrieving messages: {str(e)}")
            traceback.print_exc()
            raise