
# Purpose: Admin dashboard for user management
# Description: This module provides functionality for admin users to manage platform users,
# including retrieving user lists, banning users, and resetting user passwords.

import traceback
from app.core import authentication
from app.utils import config, logger

# Set up logger
log = logger.setup_logger()

# Load configuration
DEBUG = config.get_config_value('DEBUG')

def get_user_list() -> list:
    """
    Returns a list of all users on the platform.

    Returns:
        list: A list of dictionaries containing user information.
    """
    try:
        # In a real application, this would query a database
        users = authentication.get_all_users()
        if DEBUG:
            log.debug(f"Retrieved {len(users)} users")
        return users
    except Exception as e:
        log.error(f"Error retrieving user list: {str(e)}")
        if DEBUG:
            log.error(traceback.format_exc())
        return []

def ban_user(user_id: int) -> bool:
    """
    Bans a user from the platform.

    Args:
        user_id (int): The ID of the user to ban.

    Returns:
        bool: True if the user was successfully banned, False otherwise.
    """
    try:
        # In a real application, this would update the user's status in the database
        success = authentication.update_user_status(user_id, 'banned')
        if success:
            log.info(f"User {user_id} has been banned")
            if DEBUG:
                log.debug(f"Ban user operation successful for user {user_id}")
        else:
            log.warning(f"Failed to ban user {user_id}")
        return success
    except Exception as e:
        log.error(f"Error banning user {user_id}: {str(e)}")
        if DEBUG:
            log.error(traceback.format_exc())
        return False

def reset_user_password(user_id: int) -> str:
    """
    Resets a user's password and returns a new one.

    Args:
        user_id (int): The ID of the user whose password needs to be reset.

    Returns:
        str: A new randomly generated password, or an empty string if the operation failed.
    """
    try:
        # In a real application, this would generate a secure random password
        # and update it in the database
        new_password = authentication.generate_random_password()
        success = authentication.update_user_password(user_id, new_password)
        if success:
            log.info(f"Password reset for user {user_id}")
            if DEBUG:
                log.debug(f"Password reset successful for user {user_id}")
            return new_password
        else:
            log.warning(f"Failed to reset password for user {user_id}")
            return ""
    except Exception as e:
        log.error(f"Error resetting password for user {user_id}: {str(e)}")
        if DEBUG:
            log.error(traceback.format_exc())
        return ""

if DEBUG:
    log.debug("Admin dashboard module loaded")
