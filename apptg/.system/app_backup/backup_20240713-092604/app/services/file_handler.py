
# File: /project_root/app/services/file_handler.py
# Purpose: Manages file uploads and downloads for the communication platform.
# Description: This module provides functions to save uploaded files and retrieve files for download.

from flask import current_app
from werkzeug.utils import secure_filename
import os
import traceback
import uuid

# Set DEBUG to True for development, False for production
DEBUG = True

def save_file(file):
    """
    Saves an uploaded file to the server.
    
    Args:
        file: The file object to be saved.
    
    Returns:
        str: The filename of the saved file if successful, None otherwise.
    """
    try:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Generate a unique filename to prevent overwrites
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            if DEBUG:
                print(f"File saved successfully: {unique_filename}")
            
            return unique_filename
        else:
            if DEBUG:
                print("Invalid file or file type not allowed")
            return None
    except Exception as e:
        if DEBUG:
            print(f"Error saving file: {str(e)}")
            traceback.print_exc()
        return None

def get_file(filename):
    """
    Retrieves a file for download.
    
    Args:
        filename (str): The name of the file to be retrieved.
    
    Returns:
        str: The full path of the file if it exists, None otherwise.
    """
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            if DEBUG:
                print(f"File retrieved successfully: {filename}")
            return file_path
        else:
            if DEBUG:
                print(f"File not found: {filename}")
            return None
    except Exception as e:
        if DEBUG:
            print(f"Error retrieving file: {str(e)}")
            traceback.print_exc()
        return None

def allowed_file(filename):
    """
    Checks if the file type is allowed.
    
    Args:
        filename (str): The name of the file to be checked.
    
    Returns:
        bool: True if the file type is allowed, False otherwise.
    """
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Unit tests
import unittest
import tempfile

class TestFileHandler(unittest.TestCase):
    def setUp(self):
        self.app = current_app
        self.app.config['TESTING'] = True
        self.app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

    def test_save_file(self):
        with tempfile.NamedTemporaryFile(suffix='.txt') as temp_file:
            temp_file.write(b'Test content')
            temp_file.seek(0)
            filename = save_file(temp_file)
            self.assertIsNotNone(filename)
            self.assertTrue(os.path.exists(os.path.join(self.app.config['UPLOAD_FOLDER'], filename)))

    def test_get_file(self):
        with tempfile.NamedTemporaryFile(suffix='.txt', dir=self.app.config['UPLOAD_FOLDER'], delete=False) as temp_file:
            temp_file.write(b'Test content')
            temp_file.seek(0)
            filename = os.path.basename(temp_file.name)
        
        file_path = get_file(filename)
        self.assertIsNotNone(file_path)
        self.assertTrue(os.path.exists(file_path))

    def test_allowed_file(self):
        self.assertTrue(allowed_file('test.txt'))
        self.assertTrue(allowed_file('image.jpg'))
        self.assertFalse(allowed_file('script.py'))

if __name__ == '__main__':
    unittest.main()
