# Purpose: Messaging functionality initialization
# This file initializes the messaging components for the web-based messaging platform

import traceback
import logging
from flask_socketio import SocketIO

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug flag
DEBUG = True

socketio = SocketIO()

def init_messaging(app):
    """
    Initializes messaging components.

    Args:
    app (Flask): The Flask application instance

    Returns:
    None
    """
    try:
        # Initialize SocketIO for real-time messaging
        socketio.init_app(app)

        # Set up message routing
        @socketio.on('send_message')
        def handle_message(data):
            # Process and broadcast the message
            socketio.emit('new_message', data, broadcast=True)

        # Initialize message encryption
        from cryptography.fernet import Fernet
        app.config['MESSAGE_ENCRYPTION_KEY'] = Fernet.generate_key()
        app.config['FERNET'] = Fernet(app.config['MESSAGE_ENCRYPTION_KEY'])

        if DEBUG:
            logger.debug("Messaging components initialized successfully.")

        logger.info("Messaging initialization completed.")

    except Exception as e:
        logger.error(f"Error initializing messaging components: {str(e)}")
        if DEBUG:
            logger.error(traceback.format_exc())

# Additional messaging-related functions or classes can be added here
def encrypt_message(message):
    return app.config['FERNET'].encrypt(message.encode()).decode()

def decrypt_message(encrypted_message):
    return app.config['FERNET'].decrypt(encrypted_message.encode()).decode()