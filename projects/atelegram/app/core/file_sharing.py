
"""
File: /app/core/file_sharing.py
Purpose: Handles secure file sharing and large file support.
Description: This module provides functionality for uploading, downloading, and sharing files securely within the application.
"""

import os
import uuid
import traceback
from app.core import encryption
from app.utils import config, logger

# Initialize logger
log = logger.setup_logger()

# Load configuration
file_storage_path = config.get_config_value('file_storage_path')
max_file_size = config.get_config_value('max_file_size')

DEBUG = True

def upload_file(user_id: int, file_path: str) -> str:
    """
    Uploads a file and returns a secure link.

    Args:
    user_id (int): The ID of the user uploading the file.
    file_path (str): The path to the file to be uploaded.

    Returns:
    str: A secure link to the uploaded file.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_size = os.path.getsize(file_path)
        if file_size > max_file_size:
            raise ValueError(f"File size exceeds maximum allowed size of {max_file_size} bytes")

        file_id = str(uuid.uuid4())
        destination_path = os.path.join(file_storage_path, file_id)

        with open(file_path, 'rb') as source_file, open(destination_path, 'wb') as dest_file:
            encrypted_content = encryption.encrypt_message(source_file.read(), str(user_id))
            dest_file.write(encrypted_content)

        secure_link = f"/files/{file_id}"
        
        if DEBUG:
            log.info(f"File uploaded successfully. User ID: {user_id}, File ID: {file_id}")

        return secure_link

    except Exception as e:
        log.error(f"Error uploading file: {str(e)}")
        log.error(traceback.format_exc())
        return ""

def download_file(user_id: int, file_id: str) -> bytes:
    """
    Downloads a file.

    Args:
    user_id (int): The ID of the user downloading the file.
    file_id (str): The ID of the file to be downloaded.

    Returns:
    bytes: The decrypted content of the file.
    """
    try:
        file_path = os.path.join(file_storage_path, file_id)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_id}")

        with open(file_path, 'rb') as file:
            encrypted_content = file.read()
            decrypted_content = encryption.decrypt_message(encrypted_content, str(user_id))

        if DEBUG:
            log.info(f"File downloaded successfully. User ID: {user_id}, File ID: {file_id}")

        return decrypted_content

    except Exception as e:
        log.error(f"Error downloading file: {str(e)}")
        log.error(traceback.format_exc())
        return b""

def share_file(file_id: str, recipient_id: int) -> bool:
    """
    Shares a file with another user.

    Args:
    file_id (str): The ID of the file to be shared.
    recipient_id (int): The ID of the user to share the file with.

    Returns:
    bool: True if the file was shared successfully, False otherwise.
    """
    try:
        file_path = os.path.join(file_storage_path, file_id)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_id}")

        # Here you would implement the logic to share the file with the recipient
        # This could involve creating a database entry, setting permissions, etc.
        # For this example, we'll just log the action

        log.info(f"File shared. File ID: {file_id}, Recipient ID: {recipient_id}")

        if DEBUG:
            log.info(f"File shared successfully. File ID: {file_id}, Recipient ID: {recipient_id}")

        return True

    except Exception as e:
        log.error(f"Error sharing file: {str(e)}")
        log.error(traceback.format_exc())
        return False

if DEBUG:
    log.info("File sharing module loaded successfully.")
