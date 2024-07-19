
# constants.py
# Purpose: Store constant values used throughout the application
# Description: This file contains only variable definitions without any functions or imports

# Debug mode flag
DEBUG = True

# Application name
APP_NAME = "AI-Assisted Python Developer"

# Version number
VERSION = "1.0.0"

# Maximum retries for API requests
MAX_RETRIES = 3

# Delay between retries (in seconds)
RETRY_DELAY = 5

# Maximum number of files to process in a single run
MAX_FILES = 10

# Default timeout for API requests (in seconds)
API_TIMEOUT = 30

# Backup folder name
BACKUP_FOLDER = "backups"

# Maximum length of file content to send in API requests
MAX_FILE_CONTENT_LENGTH = 100000

# File extensions to ignore during processing
IGNORED_EXTENSIONS = [".pyc", ".pyo", ".pyd", ".db", ".log"]

# Maximum number of lines to display in error messages
MAX_ERROR_LINES = 10

# Default model to use for AI requests
DEFAULT_MODEL = "claude-2"

# Temperature setting for AI responses (0.0 to 1.0)
AI_TEMPERATURE = 0.7

# Maximum tokens for AI response
MAX_TOKENS = 4000

# Prompt prefix for code generation
CODE_GENERATION_PREFIX = "You are a Python and Web Full Stack expert Developer. Your task is to write error-free code for the application based on the overall project logical structure."

# Prompt prefix for error fixing
ERROR_FIXING_PREFIX = "You are a Python debugging expert. Your task is to identify and fix errors in the following code:"

# Prompt prefix for unit test creation
UNITTEST_CREATION_PREFIX = "You are a Python testing expert. Your task is to create comprehensive unit tests for the following code:"

# Color codes for terminal output
COLORS = {
    "INFO": "cyan",
    "SUCCESS": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "DEBUG": "magenta"
}
