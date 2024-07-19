# config.py
# Purpose: Configuration settings for the application
# Description: This file contains the Config class that holds configuration variables
# such as SECRET_KEY and SQLALCHEMY_DATABASE_URI for the Flask application.

import os
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug mode
DEBUG = True

class Config:
    """
    Configuration class for the application.
    Holds various configuration variables used throughout the app.
    """
    
    try:
        # Secret key for session management
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        
        # Database URI
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///app.db'
        
        # Disable SQLAlchemy modification tracking
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        
        # Upload folder for media files
        UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
        
        # Maximum allowed file size for uploads (16 MB)
        MAX_CONTENT_LENGTH = 16 * 1024 * 1024
        
        # CSRF protection
        WTF_CSRF_ENABLED = True
        
        # API rate limiting
        RATELIMIT_DEFAULT = "100/hour"
        
        # Debug mode
        DEBUG = DEBUG
        
        if DEBUG:
            logger.info("Configuration loaded successfully")
            logger.debug(f"SECRET_KEY: {SECRET_KEY}")
            logger.debug(f"SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")
            logger.debug(f"UPLOAD_FOLDER: {UPLOAD_FOLDER}")
    
    except Exception as e:
        logger.error(f"Error in Config class: {str(e)}")
        logger.error(traceback.format_exc())
        raise

# Additional configuration classes can be added here for different environments
# For example:
# class DevelopmentConfig(Config):
#     DEBUG = True

# class ProductionConfig(Config):
#     DEBUG = False
#     # Add production-specific settings

if DEBUG:
    logger.info("config.py loaded successfully")