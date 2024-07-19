
# file_sharing.py
# Purpose: Manages file uploads, downloads, and media support for the Telegram clone application.
# This module handles file operations, including uploading, downloading, and listing user files.

import os
import traceback
from flask import send_file, current_app
from werkzeug.utils import secure_filename
from config import DEBUG
from utils import generate_unique_id

# Assuming a database module exists for storing file metadata
from database import add_file_record, get_file_record, get_user_files

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4'}
UPLOAD_FOLDER = 'uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(user_id, file):
    """
    Upload a file for a specific user.
    
    Args:
    user_id (int): The ID of the user uploading the file.
    file (FileStorage): The file object to be uploaded.
    
    Returns:
    str: The unique ID of the uploaded file, or None if upload fails.
    """
    try:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_id = generate_unique_id()
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_id + '_' + filename)
            
            file.save(file_path)
            
            # Store file metadata in the database
            if add_file_record(file_id, user_id, filename, file_path):
                if DEBUG:
                    print(f"File uploaded successfully: {filename} for user {user_id}")
                return file_id
            else:
                if DEBUG:
                    print(f"Failed to add file record to database: {filename} for user {user_id}")
                return None
        else:
            if DEBUG:
                print(f"Invalid file type or no file provided for user {user_id}")
            return None
    except Exception as e:
        if DEBUG:
            print(f"Error in upload_file: {str(e)}")
            traceback.print_exc()
        return None

def download_file(file_id):
    """
    Download a file based on its unique ID.
    
    Args:
    file_id (str): The unique ID of the file to be downloaded.
    
    Returns:
    file: The requested file as a Flask send_file object, or None if file not found.
    """
    try:
        file_record = get_file_record(file_id)
        if file_record:
            file_path = file_record['file_path']
            if os.path.exists(file_path):
                if DEBUG:
                    print(f"Sending file: {file_path}")
                return send_file(file_path, as_attachment=True)
            else:
                if DEBUG:
                    print(f"File not found at path: {file_path}")
                return None
        else:
            if DEBUG:
                print(f"No file record found for file_id: {file_id}")
            return None
    except Exception as e:
        if DEBUG:
            print(f"Error in download_file: {str(e)}")
            traceback.print_exc()
        return None

def list_user_files(user_id):
    """
    List all files uploaded by a specific user.
    
    Args:
    user_id (int): The ID of the user whose files are to be listed.
    
    Returns:
    list: A list of dictionaries containing file information for the user.
    """
    try:
        files = get_user_files(user_id)
        if DEBUG:
            print(f"Retrieved {len(files)} files for user {user_id}")
        return files
    except Exception as e:
        if DEBUG:
            print(f"Error in list_user_files: {str(e)}")
            traceback.print_exc()
        return []

# Additional helper functions can be added here as needed

if DEBUG:
    print("file_sharing.py loaded successfully")
