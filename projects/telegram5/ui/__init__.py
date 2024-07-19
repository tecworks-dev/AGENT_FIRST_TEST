# ui/__init__.py
"""
User interface initialization.
This module initializes UI-related components for the messaging platform.
"""

import traceback
import logging
from flask import render_template

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug flag
DEBUG = True

def init_ui(app):
    """
    Initializes UI-related components.

    :param app: Flask application instance
    :return: None
    """
    try:
        if DEBUG:
            logger.info("Initializing UI components...")

        # Initialize UI-related components
        # Set up template filters
        app.template_filter('capitalize')(capitalize_filter)
        app.template_filter('truncate')(truncate_filter)

        # Set up custom Jinja2 functions
        app.jinja_env.globals.update(format_datetime=format_datetime)
        app.jinja_env.globals.update(get_user_avatar=get_user_avatar)

        # Set up error handlers
        app.errorhandler(404)(handle_404)
        app.errorhandler(500)(handle_500)

        if DEBUG:
            logger.info("UI components initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing UI components: {str(e)}")
        if DEBUG:
            logger.error(traceback.format_exc())

def capitalize_filter(value):
    """Custom filter to capitalize the first letter of each word."""
    return value.title()

def truncate_filter(value, length=100, end='...'):
    """Custom filter to truncate long text."""
    if len(value) <= length:
        return value
    return value[:length].rsplit(' ', 1)[0] + end

def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    """Custom function to format datetime objects."""
    return value.strftime(format)

def get_user_avatar(user_id):
    """Custom function to get user avatar URL."""
    # This is a placeholder. In a real application, you would fetch this from your user database.
    return f"/static/avatars/{user_id}.png"

def handle_404(error):
    """Custom 404 error handler."""
    return render_template('404.html'), 404

def handle_500(error):
    """Custom 500 error handler."""
    return render_template('500.html'), 500

# Additional UI-related helper functions can be added here

if DEBUG:
    logger.info("ui/__init__.py loaded successfully")