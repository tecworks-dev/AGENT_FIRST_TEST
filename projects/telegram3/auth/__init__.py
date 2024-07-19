"""
Authentication module initialization.

This module initializes the authentication components for the messaging platform.
It sets up Flask-Login for user session management and authentication.
"""

import traceback
from flask_login import LoginManager
from database import User

# Debug flag
DEBUG = True

def init_auth(app):
    """
    Initializes authentication components.

    This function sets up Flask-Login and configures the LoginManager
    for the application.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        None
    """
    try:
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = 'main.login'  # Specify the login view route

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        if DEBUG:
            print("Authentication components initialized successfully.")

    except Exception as e:
        print(f"Error initializing authentication components: {str(e)}")
        if DEBUG:
            traceback.print_exc()