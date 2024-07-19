
# theme_management.py
"""
Manages custom themes and appearance settings for the Telegram clone application.
This module provides functions to set and retrieve user themes, as well as list available themes.
"""

import flask
from flask import current_app, jsonify
import traceback
from config import DEBUG
from database import get_user, update_user

# Define a list of available themes
AVAILABLE_THEMES = [
    {"name": "default", "primary_color": "#0088cc", "secondary_color": "#ffffff"},
    {"name": "dark", "primary_color": "#1c2733", "secondary_color": "#ffffff"},
    {"name": "light", "primary_color": "#ffffff", "secondary_color": "#000000"},
    {"name": "nature", "primary_color": "#4caf50", "secondary_color": "#e8f5e9"},
]

def set_theme(user_id, theme_name):
    """
    Set the theme for a specific user.

    Args:
        user_id (int): The ID of the user.
        theme_name (str): The name of the theme to set.

    Returns:
        bool: True if the theme was set successfully, False otherwise.
    """
    try:
        if DEBUG:
            print(f"Setting theme '{theme_name}' for user {user_id}")

        # Check if the theme exists
        theme = next((t for t in AVAILABLE_THEMES if t["name"] == theme_name), None)
        if not theme:
            if DEBUG:
                print(f"Theme '{theme_name}' not found")
            return False

        # Update the user's theme in the database
        user = get_user(user_id)
        if not user:
            if DEBUG:
                print(f"User {user_id} not found")
            return False

        user['theme'] = theme
        success = update_user(user_id, user)

        if DEBUG:
            print(f"Theme update {'successful' if success else 'failed'} for user {user_id}")

        return success
    except Exception as e:
        if DEBUG:
            print(f"Error in set_theme: {str(e)}")
            traceback.print_exc()
        return False

def get_user_theme(user_id):
    """
    Get the current theme for a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: The user's current theme, or the default theme if not set.
    """
    try:
        if DEBUG:
            print(f"Getting theme for user {user_id}")

        user = get_user(user_id)
        if not user or 'theme' not in user:
            if DEBUG:
                print(f"User {user_id} not found or theme not set, returning default theme")
            return AVAILABLE_THEMES[0]  # Return default theme

        if DEBUG:
            print(f"Retrieved theme for user {user_id}: {user['theme']}")

        return user['theme']
    except Exception as e:
        if DEBUG:
            print(f"Error in get_user_theme: {str(e)}")
            traceback.print_exc()
        return AVAILABLE_THEMES[0]  # Return default theme in case of error

def list_available_themes():
    """
    List all available themes.

    Returns:
        list: A list of all available themes.
    """
    if DEBUG:
        print("Listing available themes")
    return AVAILABLE_THEMES

# Flask route to set a user's theme
@current_app.route('/set_theme', methods=['POST'])
def set_user_theme():
    data = flask.request.json
    user_id = data.get('user_id')
    theme_name = data.get('theme_name')
    
    if not user_id or not theme_name:
        return jsonify({"error": "Missing user_id or theme_name"}), 400
    
    success = set_theme(user_id, theme_name)
    if success:
        return jsonify({"message": "Theme set successfully"}), 200
    else:
        return jsonify({"error": "Failed to set theme"}), 400

# Flask route to get a user's current theme
@current_app.route('/get_theme/<int:user_id>', methods=['GET'])
def get_theme(user_id):
    theme = get_user_theme(user_id)
    return jsonify(theme), 200

# Flask route to list all available themes
@current_app.route('/list_themes', methods=['GET'])
def list_themes():
    themes = list_available_themes()
    return jsonify(themes), 200
