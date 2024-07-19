
# user_management.py
# Purpose: Handles user registration, login, and profile management for the Telegram clone application.
# This module provides functions for user authentication and profile updates.

import traceback
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_user, update_user
from utils import validate_email, generate_unique_id

# Import the logging module
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_user(username, password, email):
    """
    Register a new user in the system.
    
    Args:
    username (str): The desired username for the new user.
    password (str): The password for the new user.
    email (str): The email address of the new user.
    
    Returns:
    bool: True if registration is successful, False otherwise.
    """
    try:
        if current_app.config['DEBUG']:
            logger.debug(f"Attempting to register user: {username}")

        # Validate email
        if not validate_email(email):
            logger.warning(f"Invalid email provided for user: {username}")
            return False

        # Check if username or email already exists
        existing_user = get_user(username=username)
        if existing_user:
            logger.warning(f"Username {username} already exists")
            return False

        existing_email = get_user(email=email)
        if existing_email:
            logger.warning(f"Email {email} already in use")
            return False

        # Create new user
        user_id = generate_unique_id()
        hashed_password = generate_password_hash(password)
        new_user = {
            'id': user_id,
            'username': username,
            'password': hashed_password,
            'email': email
        }

        # Add user to database
        success = update_user(user_id, new_user)
        
        if success:
            logger.info(f"User {username} registered successfully")
        else:
            logger.error(f"Failed to register user {username}")

        return success

    except Exception as e:
        logger.error(f"Error in register_user: {str(e)}")
        if current_app.config['DEBUG']:
            logger.error(traceback.format_exc())
        return False

def login_user(username, password):
    """
    Authenticate a user and log them in.
    
    Args:
    username (str): The username of the user trying to log in.
    password (str): The password provided by the user.
    
    Returns:
    dict: User data if login is successful, None otherwise.
    """
    try:
        if current_app.config['DEBUG']:
            logger.debug(f"Attempting to log in user: {username}")

        user = get_user(username=username)
        if user and check_password_hash(user['password'], password):
            logger.info(f"User {username} logged in successfully")
            return {k: v for k, v in user.items() if k != 'password'}
        else:
            logger.warning(f"Failed login attempt for user: {username}")
            return None

    except Exception as e:
        logger.error(f"Error in login_user: {str(e)}")
        if current_app.config['DEBUG']:
            logger.error(traceback.format_exc())
        return None

def update_profile(user_id, profile_data):
    """
    Update user profile information.
    
    Args:
    user_id (str): The ID of the user whose profile is being updated.
    profile_data (dict): A dictionary containing the updated profile information.
    
    Returns:
    bool: True if update is successful, False otherwise.
    """
    try:
        if current_app.config['DEBUG']:
            logger.debug(f"Attempting to update profile for user ID: {user_id}")

        # Ensure email is valid if it's being updated
        if 'email' in profile_data and not validate_email(profile_data['email']):
            logger.warning(f"Invalid email provided for user ID: {user_id}")
            return False

        # Update user in database
        success = update_user(user_id, profile_data)
        
        if success:
            logger.info(f"Profile updated successfully for user ID: {user_id}")
        else:
            logger.error(f"Failed to update profile for user ID: {user_id}")

        return success

    except Exception as e:
        logger.error(f"Error in update_profile: {str(e)}")
        if current_app.config['DEBUG']:
            logger.error(traceback.format_exc())
        return False
