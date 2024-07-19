
"""
authentication.py

This file implements two-factor authentication functionality for the Telegram clone application.
It provides methods to enable, verify, and disable 2FA for users.

Imports:
- flask: For web application functionality
- pyotp: For generating and verifying one-time passwords
- database: Custom module for database operations
- config: Custom module for application configuration
- traceback: For detailed error logging
"""

import flask
from flask import current_app
import pyotp
import database
import config
import traceback

def enable_2fa(user_id):
    """
    Enable two-factor authentication for a user.

    Args:
    user_id (int): The ID of the user enabling 2FA

    Returns:
    str: The secret key for 2FA setup, or None if an error occurs
    """
    try:
        user = database.get_user(user_id)
        if not user:
            current_app.logger.error(f"User not found: {user_id}")
            return None

        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(user['email'], issuer_name="TelegramClone")

        if database.update_user(user_id, {'two_factor_secret': secret}):
            if config.DEBUG:
                current_app.logger.debug(f"2FA enabled for user: {user_id}")
            return provisioning_uri
        else:
            current_app.logger.error(f"Failed to update 2FA secret for user: {user_id}")
            return None
    except Exception as e:
        current_app.logger.error(f"Error enabling 2FA for user {user_id}: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return None

def verify_2fa(user_id, token):
    """
    Verify a 2FA token for a user.

    Args:
    user_id (int): The ID of the user verifying 2FA
    token (str): The 2FA token to verify

    Returns:
    bool: True if the token is valid, False otherwise
    """
    try:
        user = database.get_user(user_id)
        if not user or 'two_factor_secret' not in user:
            current_app.logger.error(f"User not found or 2FA not enabled: {user_id}")
            return False

        totp = pyotp.TOTP(user['two_factor_secret'])
        if totp.verify(token):
            if config.DEBUG:
                current_app.logger.debug(f"2FA verified for user: {user_id}")
            return True
        else:
            current_app.logger.warning(f"Invalid 2FA token for user: {user_id}")
            return False
    except Exception as e:
        current_app.logger.error(f"Error verifying 2FA for user {user_id}: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return False

def disable_2fa(user_id):
    """
    Disable two-factor authentication for a user.

    Args:
    user_id (int): The ID of the user disabling 2FA

    Returns:
    bool: True if 2FA was successfully disabled, False otherwise
    """
    try:
        user = database.get_user(user_id)
        if not user or 'two_factor_secret' not in user:
            current_app.logger.error(f"User not found or 2FA not enabled: {user_id}")
            return False

        if database.update_user(user_id, {'two_factor_secret': None}):
            if config.DEBUG:
                current_app.logger.debug(f"2FA disabled for user: {user_id}")
            return True
        else:
            current_app.logger.error(f"Failed to disable 2FA for user: {user_id}")
            return False
    except Exception as e:
        current_app.logger.error(f"Error disabling 2FA for user {user_id}: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return False

if config.DEBUG:
    current_app.logger.debug("authentication.py loaded successfully")
