
# Purpose: Implements media handling logic for the messaging platform.
# Description: This file contains the MediaService class which provides methods for uploading,
#              retrieving, and deleting media files associated with user messages.

import traceback
from app.models.media import Media
from app.utils.storage import store_file, retrieve_file, delete_file
from app.extensions import db

class MediaService:
    @staticmethod
    def upload_media(user_id: int, file) -> dict:
        """
        Upload a media file for a user.

        Args:
            user_id (int): The ID of the user uploading the file.
            file: The file object to be uploaded.

        Returns:
            dict: A dictionary containing the media information.
        """
        try:
            filename = store_file(file, str(user_id))
            media = Media(user_id=user_id, filename=filename, file_type=file.content_type)
            db.session.add(media)
            db.session.commit()

            if __debug__:
                print(f"DEBUG: Media uploaded successfully. Media ID: {media.id}")

            return {
                'id': media.id,
                'filename': media.filename,
                'file_type': media.file_type,
                'timestamp': media.timestamp.isoformat()
            }
        except Exception as e:
            db.session.rollback()
            print(f"Error uploading media: {str(e)}")
            traceback.print_exc()
            return None

    @staticmethod
    def get_media(media_id: int) -> dict:
        """
        Retrieve media information and file by media ID.

        Args:
            media_id (int): The ID of the media to retrieve.

        Returns:
            dict: A dictionary containing the media information and file.
        """
        try:
            media = Media.query.get(media_id)
            if not media:
                if __debug__:
                    print(f"DEBUG: Media not found. Media ID: {media_id}")
                return None

            file = retrieve_file(media.filename)
            if not file:
                if __debug__:
                    print(f"DEBUG: Media file not found. Filename: {media.filename}")
                return None

            if __debug__:
                print(f"DEBUG: Media retrieved successfully. Media ID: {media_id}")

            return {
                'id': media.id,
                'filename': media.filename,
                'file_type': media.file_type,
                'timestamp': media.timestamp.isoformat(),
                'file': file
            }
        except Exception as e:
            print(f"Error retrieving media: {str(e)}")
            traceback.print_exc()
            return None

    @staticmethod
    def delete_media(media_id: int) -> bool:
        """
        Delete a media file and its associated database record.

        Args:
            media_id (int): The ID of the media to delete.

        Returns:
            bool: True if the media was successfully deleted, False otherwise.
        """
        try:
            media = Media.query.get(media_id)
            if not media:
                if __debug__:
                    print(f"DEBUG: Media not found for deletion. Media ID: {media_id}")
                return False

            if delete_file(media.filename):
                db.session.delete(media)
                db.session.commit()
                if __debug__:
                    print(f"DEBUG: Media deleted successfully. Media ID: {media_id}")
                return True
            else:
                if __debug__:
                    print(f"DEBUG: Failed to delete media file. Media ID: {media_id}")
                return False
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting media: {str(e)}")
            traceback.print_exc()
            return False
