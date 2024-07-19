
# config.py
"""
This file stores configuration variables for the Telegram clone application.
It contains important settings such as database URI, secret key, and debug mode.
These variables can be imported and used throughout the application to maintain
consistent configuration across all modules.
"""

import os
from datetime import timedelta

# Database configuration
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///telegram_clone.db')

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-jwt-secret-key-here')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

# Debug mode
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Application settings
APP_NAME = "Telegram Clone"
APP_VERSION = "1.0.0"

# File upload settings
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

# Messaging settings
MAX_MESSAGE_LENGTH = 4096
MESSAGE_FETCH_LIMIT = 100

# User settings
MIN_PASSWORD_LENGTH = 8
MAX_USERNAME_LENGTH = 32

# Group and channel settings
MAX_GROUP_MEMBERS = 200
MAX_CHANNEL_SUBSCRIBERS = 5000

# Call settings
MAX_CALL_DURATION = 3600  # 1 hour in seconds

# Theme settings
DEFAULT_THEME = "light"

# Bot settings
MAX_BOTS_PER_USER = 20

# Search settings
SEARCH_RESULT_LIMIT = 50

# Two-factor authentication settings
TOTP_ISSUER = "TelegramClone"

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FILE = 'app.log'

# API rate limiting
RATELIMIT_DEFAULT = "100/hour"
RATELIMIT_STORAGE_URL = "memory://"

# Cross-Origin Resource Sharing (CORS) settings
CORS_ALLOW_ORIGINS = ['http://localhost:3000', 'https://telegramclone.com']

if DEBUG:
    print("Warning: Debug mode is enabled. Do not use in production.")
    print(f"Database URI: {DATABASE_URI}")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Max content length: {MAX_CONTENT_LENGTH}")
