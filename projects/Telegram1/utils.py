
# utils.py
"""
This file contains utility functions used across the Telegram clone application.
These functions provide common operations such as generating unique IDs,
validating email addresses, and formatting timestamps.
"""

import uuid
import re
from datetime import datetime
import traceback

# Import the DEBUG flag from config
try:
    from config import DEBUG
except ImportError:
    DEBUG = False

def generate_unique_id() -> str:
    """
    Generate a unique identifier using UUID.
    
    Returns:
        str: A unique identifier string.
    """
    try:
        unique_id = str(uuid.uuid4())
        if DEBUG:
            print(f"Generated unique ID: {unique_id}")
        return unique_id
    except Exception as e:
        print(f"Error generating unique ID: {str(e)}")
        traceback.print_exc()
        return ""

def validate_email(email: str) -> bool:
    """
    Validate an email address using a regular expression.
    
    Args:
        email (str): The email address to validate.
    
    Returns:
        bool: True if the email is valid, False otherwise.
    """
    try:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = re.match(email_regex, email) is not None
        if DEBUG:
            print(f"Email validation result for {email}: {is_valid}")
        return is_valid
    except Exception as e:
        print(f"Error validating email: {str(e)}")
        traceback.print_exc()
        return False

def format_timestamp(timestamp: float) -> str:
    """
    Format a Unix timestamp into a human-readable string.
    
    Args:
        timestamp (float): The Unix timestamp to format.
    
    Returns:
        str: A formatted string representation of the timestamp.
    """
    try:
        formatted_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        if DEBUG:
            print(f"Formatted timestamp {timestamp} to: {formatted_time}")
        return formatted_time
    except Exception as e:
        print(f"Error formatting timestamp: {str(e)}")
        traceback.print_exc()
        return ""

if DEBUG:
    print("Utility functions loaded successfully.")
