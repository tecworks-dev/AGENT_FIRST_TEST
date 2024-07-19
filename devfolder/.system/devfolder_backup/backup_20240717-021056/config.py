
"""
Configuration settings for the application.

This file contains the configuration classes for different environments
and a function to get the appropriate configuration based on the environment.
"""

import os

class Config:
    """Base configuration class with common settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
    MAX_TOKENS = 4000
    TEMPERATURE = 0.7
    DEBUG = False  # Default DEBUG setting

class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Configuration for production environment."""
    DEBUG = False

class TestingConfig(Config):
    """Configuration for testing environment."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

def get_config():
    """Returns the appropriate configuration based on the environment."""
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()

# Additional configurations for components mentioned in the application plan
Config.SOCKETIO_MESSAGE_QUEUE = os.environ.get('SOCKETIO_MESSAGE_QUEUE') or None
Config.REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379'
Config.CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379'
Config.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379'

# Feature flags configuration
Config.FEATURE_FLAGS = {
    'USE_AI_CODE_REVIEW': os.environ.get('USE_AI_CODE_REVIEW', 'False').lower() == 'true',
    'ENABLE_WEBSOCKETS': os.environ.get('ENABLE_WEBSOCKETS', 'True').lower() == 'true',
    'USE_CELERY_TASKS': os.environ.get('USE_CELERY_TASKS', 'False').lower() == 'true',
}

# Logging configuration
Config.LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', 'False').lower() == 'true'
Config.LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# Security configurations
Config.SSL_REDIRECT = os.environ.get('SSL_REDIRECT', 'False').lower() == 'true'
Config.BCRYPT_LOG_ROUNDS = int(os.environ.get('BCRYPT_LOG_ROUNDS', 13))
Config.WTF_CSRF_ENABLED = True

# File upload configurations
Config.UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
Config.MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max-limit

# Email configurations (for password reset, notifications, etc.)
Config.MAIL_SERVER = os.environ.get('MAIL_SERVER')
Config.MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
Config.MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'False').lower() == 'true'
Config.MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
Config.MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# Pagination settings
Config.POSTS_PER_PAGE = 10

if __name__ == "__main__":
    print("This script is not meant to be run directly. Import it in your Flask application.")
