"""
main.py: Entry point of the application.

This file initializes the server and sets up the main application components.
It creates and configures the Flask application, initializes all necessary
modules, and runs the application.

IMPORTANT: do not remove main function as automated test will fail
IMPORTANT: do not remove this comment
"""

import traceback
import logging
import sys
import subprocess

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DEBUG = True

def check_dependencies():
    """
    Check if all required packages are installed.
    If not, attempt to install them.
    """
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_restful',
        'flask_wtf',
        'flask_talisman',
        'flask_limiter',
        'flask_bcrypt',
        'cryptography',
        'Pillow',
        'celery',
        'redis',
    ]

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            logger.warning(f"{package} not found. Attempting to install...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except subprocess.CalledProcessError:
                logger.error(f"Failed to install {package}. Please install it manually.")
                sys.exit(1)

def create_app():
    """
    Creates and configures the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    try:
        from flask import Flask, send_from_directory
        from flask_wtf.csrf import CSRFProtect
        from config import Config
        from database import init_db
        from routes import init_routes
        from auth import init_auth
        from messaging import init_messaging
        from media import init_media
        from voice_video import init_voice_video
        from ui import init_ui
        from api import init_api
        from performance import init_performance
        from security import init_security

        app = Flask(__name__)
        app.config.from_object(Config)

        # Initialize CSRF protection
        csrf = CSRFProtect(app)

        # Initialize database
        init_db(app)

        # Initialize routes
        init_routes(app)

        # Initialize authentication
        init_auth(app)

        # Initialize messaging
        init_messaging(app)

        # Initialize media handling
        init_media(app)

        # Initialize voice and video
        init_voice_video(app)

        # Initialize user interface
        init_ui(app)

        # Initialize API
        init_api(app)

        # Initialize performance optimization
        init_performance(app)

        # Initialize security measures
        init_security(app)

        # Handle favicon.ico request
        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

        if DEBUG:
            logger.debug("Application created and configured successfully.")

        return app

    except Exception as e:
        logger.error(f"Error creating application: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def main():
    """
    Main function to run the application.
    """
    try:
        check_dependencies()
        app = create_app()
        if DEBUG:
            logger.debug("Starting the application...")
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Error running application: {str(e)}")
        logger.error(traceback.format_exc())
        return 1  # Return 1 to indicate an error

if __name__ == '__main__':
    main()