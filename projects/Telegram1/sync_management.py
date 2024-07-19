
# sync_management.py
"""
Handles cross-platform synchronization of user data and messages.
This module provides functions for syncing user data across different devices,
checking sync status, and resolving conflicts in user data.
"""

import traceback
from flask import current_app
from database import get_user, update_user
from config import DEBUG

def sync_user_data(user_id, device_id, data):
    """
    Synchronize user data across devices.

    Args:
    user_id (int): The ID of the user.
    device_id (str): The ID of the device initiating the sync.
    data (dict): The user data to be synced.

    Returns:
    bool: True if sync was successful, False otherwise.
    """
    try:
        if DEBUG:
            current_app.logger.debug(f"Syncing data for user {user_id} from device {device_id}")
        
        user = get_user(user_id)
        if not user:
            current_app.logger.error(f"User {user_id} not found")
            return False

        # Merge the new data with existing user data
        updated_data = {**user.get('data', {}), **data}
        
        # Update the user's data in the database
        if update_user(user_id, {'data': updated_data, 'last_sync_device': device_id}):
            if DEBUG:
                current_app.logger.debug(f"Sync successful for user {user_id}")
            return True
        else:
            current_app.logger.error(f"Failed to update data for user {user_id}")
            return False

    except Exception as e:
        current_app.logger.error(f"Error in sync_user_data: {str(e)}")
        if DEBUG:
            current_app.logger.error(traceback.format_exc())
        return False

def get_sync_status(user_id):
    """
    Get the synchronization status for a user.

    Args:
    user_id (int): The ID of the user.

    Returns:
    dict: A dictionary containing sync status information.
    """
    try:
        if DEBUG:
            current_app.logger.debug(f"Fetching sync status for user {user_id}")
        
        user = get_user(user_id)
        if not user:
            current_app.logger.error(f"User {user_id} not found")
            return {}

        return {
            'last_sync_time': user.get('last_sync_time'),
            'last_sync_device': user.get('last_sync_device'),
            'sync_status': 'up_to_date' if user.get('is_synced', False) else 'needs_sync'
        }

    except Exception as e:
        current_app.logger.error(f"Error in get_sync_status: {str(e)}")
        if DEBUG:
            current_app.logger.error(traceback.format_exc())
        return {}

def resolve_conflicts(user_id, conflicting_data):
    """
    Resolve conflicts in user data across devices.

    Args:
    user_id (int): The ID of the user.
    conflicting_data (dict): The conflicting data to be resolved.

    Returns:
    bool: True if conflicts were resolved successfully, False otherwise.
    """
    try:
        if DEBUG:
            current_app.logger.debug(f"Resolving conflicts for user {user_id}")
        
        user = get_user(user_id)
        if not user:
            current_app.logger.error(f"User {user_id} not found")
            return False

        # Implement conflict resolution logic here
        # This is a simple example that always chooses the newer data
        resolved_data = {}
        for key, value in conflicting_data.items():
            if key not in user['data'] or value.get('timestamp', 0) > user['data'][key].get('timestamp', 0):
                resolved_data[key] = value['data']
            else:
                resolved_data[key] = user['data'][key]

        # Update the user's data with the resolved data
        if update_user(user_id, {'data': resolved_data, 'is_synced': True}):
            if DEBUG:
                current_app.logger.debug(f"Conflicts resolved successfully for user {user_id}")
            return True
        else:
            current_app.logger.error(f"Failed to update resolved data for user {user_id}")
            return False

    except Exception as e:
        current_app.logger.error(f"Error in resolve_conflicts: {str(e)}")
        if DEBUG:
            current_app.logger.error(traceback.format_exc())
        return False
