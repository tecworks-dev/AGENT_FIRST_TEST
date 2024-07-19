
"""
utils/helpers.py

This file contains utility functions used across the application, specifically for password hashing and verification.
"""

import hashlib
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug flag
DEBUG = True

def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    try:
        if DEBUG:
            logger.debug(f"Hashing password: {password[:2]}{'*' * (len(password) - 2)}")
        
        hashed = hashlib.sha256(password.encode()).hexdigest()
        
        if DEBUG:
            logger.debug(f"Password hashed successfully.")
        
        return hashed
    except Exception as e:
        logger.error(f"Error in hash_password: {str(e)}")
        if DEBUG:
            logger.error(traceback.format_exc())
        return ""

def verify_password(hashed: str, password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        hashed (str): The stored hash of the password.
        password (str): The password to verify.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    try:
        if DEBUG:
            logger.debug(f"Verifying password: {password[:2]}{'*' * (len(password) - 2)}")
        
        return hash_password(password) == hashed
    except Exception as e:
        logger.error(f"Error in verify_password: {str(e)}")
        if DEBUG:
            logger.error(traceback.format_exc())
        return False

if DEBUG:
    # Test the functions
    test_password = "testpassword123"
    hashed_password = hash_password(test_password)
    logger.debug(f"Test hashed password: {hashed_password}")
    logger.debug(f"Verification result: {verify_password(hashed_password, test_password)}")
