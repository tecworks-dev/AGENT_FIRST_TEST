
# app/services/search.py
"""
This module implements search functionality for messages and media.
It provides methods to search through messages and media based on user input.
"""

import traceback
from app.models.message import Message
from app.models.media import Media
from app.extensions import db
from sqlalchemy import or_

class SearchService:
    @staticmethod
    def search_messages(user_id: int, query: str) -> list:
        """
        Search for messages related to the user based on the given query.

        Args:
            user_id (int): The ID of the user performing the search.
            query (str): The search query string.

        Returns:
            list: A list of dictionaries containing message information.
        """
        try:
            messages = Message.query.filter(
                or_(
                    Message.sender_id == user_id,
                    Message.receiver_id == user_id
                )
            ).filter(
                Message.content.ilike(f'%{query}%')
            ).all()

            results = [
                {
                    'id': message.id,
                    'sender_id': message.sender_id,
                    'receiver_id': message.receiver_id,
                    'content': message.content,
                    'timestamp': message.timestamp.isoformat()
                }
                for message in messages
            ]

            if __debug__:
                print(f"DEBUG: Found {len(results)} messages matching query '{query}' for user {user_id}")

            return results
        except Exception as e:
            print(f"Error in search_messages: {str(e)}")
            traceback.print_exc()
            return []

    @staticmethod
    def search_media(user_id: int, query: str) -> list:
        """
        Search for media files related to the user based on the given query.

        Args:
            user_id (int): The ID of the user performing the search.
            query (str): The search query string.

        Returns:
            list: A list of dictionaries containing media information.
        """
        try:
            media_files = Media.query.filter(
                Media.user_id == user_id
            ).filter(
                or_(
                    Media.filename.ilike(f'%{query}%'),
                    Media.file_type.ilike(f'%{query}%')
                )
            ).all()

            results = [
                {
                    'id': media.id,
                    'user_id': media.user_id,
                    'filename': media.filename,
                    'file_type': media.file_type,
                    'timestamp': media.timestamp.isoformat()
                }
                for media in media_files
            ]

            if __debug__:
                print(f"DEBUG: Found {len(results)} media files matching query '{query}' for user {user_id}")

            return results
        except Exception as e:
            print(f"Error in search_media: {str(e)}")
            traceback.print_exc()
            return []
