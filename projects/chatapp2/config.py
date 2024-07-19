import os

# Secret key for Flask sessions
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'

# URI for database connection
DATABASE_URI = os.environ.get('DATABASE_URI') or 'chat_app.db'

# Key for encryption operations
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or 'your-encryption-key-here'

# Debug mode (set to False in production)
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# SocketIO configuration
SOCKETIO_ASYNC_MODE = 'eventlet'

# File upload configuration
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for file uploads

# Session configuration
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False
SESSION_USE_SIGNER = True

# CSRF protection
CSRF_ENABLED = True
CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY') or 'your-csrf-session-key-here'

# Logging configuration
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# User session timeout (in minutes)
USER_SESSION_TIMEOUT = 30

# Maximum number of messages to retrieve in history
MAX_MESSAGE_HISTORY = 100

# Enable or disable user registration
ALLOW_USER_REGISTRATION = True

# Enable or disable file sharing feature
ENABLE_FILE_SHARING = True

# Dark mode default setting
DEFAULT_DARK_MODE = False

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}