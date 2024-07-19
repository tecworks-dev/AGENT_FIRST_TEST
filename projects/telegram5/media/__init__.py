# Purpose: Media handling initialization
# This file initializes media-related components for the messaging platform

import traceback
import logging
import os
from flask import current_app

DEBUG = True

def init_media(app):
    """
    Initializes media-related components for the Flask application.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        None
    """
    try:
        if DEBUG:
            print("Initializing media components...")

        # Set up file upload configurations
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
        app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3'}
        app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')

        # Ensure the upload folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Initialize image processing library (e.g., Pillow)
        from PIL import Image
        app.config['IMAGE_LIBRARY'] = Image

        if DEBUG:
            print("Media components initialized successfully.")

    except Exception as e:
        logging.error(f"Error initializing media components: {str(e)}")
        if DEBUG:
            print(f"Error initializing media components: {str(e)}")
            traceback.print_exc()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']