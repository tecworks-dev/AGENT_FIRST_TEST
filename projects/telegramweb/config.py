# config.py
# Purpose: Defines configuration settings for the messaging platform application.
# Description: This file contains a Config class with various configuration variables
#              used throughout the application, including database settings, secret keys,
#              and other environment-specific configurations.

import os
import logging

class Config:
    # Secret key for Flask sessions and other security features
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size

    # SocketIO configuration
    SOCKETIO_ASYNC_MODE = 'eventlet'

    # Logging configuration
    LOG_LEVEL = logging.DEBUG if os.environ.get('FLASK_ENV') == 'development' else logging.INFO
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Security settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

    # CSRF protection
    WTF_CSRF_ENABLED = True

    # Debug mode (set to True for development)
    DEBUG = True

    @staticmethod
    def init_app(app):
        # You can perform any additional configuration here
        pass

    def __init__(self):
        # Ensure upload folder exists
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)

        if self.DEBUG:
            print("Running in DEBUG mode")
            print(f"Database URI: {self.SQLALCHEMY_DATABASE_URI}")
            print(f"Upload folder: {self.UPLOAD_FOLDER}")