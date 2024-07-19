
"""
File: app/utils/storage.py
Purpose: Implements file storage functions for secure file handling.

This module provides utility functions for storing, retrieving, and deleting files
in a secure manner. It uses werkzeug's secure_filename function to ensure filenames
are safe for storage.
"""

import os
import traceback
from werkzeug.utils import secure_filename
from flask import current_app

# Set the upload folder path
UPLOAD_FOLDER = 'uploads'

def store_file(file, filename: str) -> str:
    """
    Stores a file securely with a given filename.

    Args:
        file: The file object to be stored.
        filename (str): The name of the file.

    Returns:
        str: The path where the file is stored.

    Raises:
        IOError: If there's an error in storing the file.
    """
    try:
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        secure_name = secure_filename(filename)
        file_path = os.path.join(UPLOAD_FOLDER, secure_name)
        file.save(file_path)
        
        if current_app.config['DEBUG']:
            print(f"DEBUG: File stored successfully at {file_path}")
        
        return file_path
    except Exception as e:
        if current_app.config['DEBUG']:
            print(f"DEBUG: Error storing file: {str(e)}")
            traceback.print_exc()
        raise IOError(f"Error storing file: {str(e)}")

def retrieve_file(filename: str):
    """
    Retrieves a file with the given filename.

    Args:
        filename (str): The name of the file to retrieve.

    Returns:
        File: The retrieved file object.

    Raises:
        FileNotFoundError: If the file is not found.
    """
    try:
        file_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
        if os.path.exists(file_path):
            if current_app.config['DEBUG']:
                print(f"DEBUG: File retrieved successfully from {file_path}")
            return open(file_path, 'rb')
        else:
            raise FileNotFoundError(f"File not found: {filename}")
    except Exception as e:
        if current_app.config['DEBUG']:
            print(f"DEBUG: Error retrieving file: {str(e)}")
            traceback.print_exc()
        raise

def delete_file(filename: str) -> bool:
    """
    Deletes a file with the given filename.

    Args:
        filename (str): The name of the file to delete.

    Returns:
        bool: True if the file was successfully deleted, False otherwise.
    """
    try:
        file_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
        if os.path.exists(file_path):
            os.remove(file_path)
            if current_app.config['DEBUG']:
                print(f"DEBUG: File deleted successfully: {file_path}")
            return True
        else:
            if current_app.config['DEBUG']:
                print(f"DEBUG: File not found for deletion: {file_path}")
            return False
    except Exception as e:
        if current_app.config['DEBUG']:
            print(f"DEBUG: Error deleting file: {str(e)}")
            traceback.print_exc()
        return False
