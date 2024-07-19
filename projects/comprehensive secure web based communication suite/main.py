"""
main.py

Purpose: Entry point of the secure communication suite application.
Description: Initializes all components and runs the application.

IMPORTANT: do not remove main function as automated test will fail
IMPORTANT: do not remove this comment
"""

import traceback
import logging
from config import Config
from encryption.crypto import EncryptionManager
from communication.messaging import MessagingManager
from communication.file_sharing import FileSharingManager
from communication.calls import CallManager
from user_management.authentication import AuthManager
from user_management.admin import AdminTools
from api.rest_api import APIManager
from bot.bot_framework import BotManager
from ui.desktop_ui import DesktopUI
from ui.mobile_ui import MobileUI
from ui.web_ui import WebUI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEBUG = True

def initialize_components():
    """Initialize all components of the application."""
    try:
        config = Config()
        encryption_manager = EncryptionManager()
        messaging_manager = MessagingManager(encryption_manager)
        file_sharing_manager = FileSharingManager(encryption_manager)
        call_manager = CallManager()
        auth_manager = AuthManager()
        admin_tools = AdminTools()
        api_manager = APIManager()
        bot_manager = BotManager()
        
        if DEBUG:
            logger.debug("All components initialized successfully.")
        
        return (config, encryption_manager, messaging_manager, file_sharing_manager,
                call_manager, auth_manager, admin_tools, api_manager, bot_manager)
    except Exception as e:
        logger.error(f"Error initializing components: {str(e)}")
        if DEBUG:
            logger.error(traceback.format_exc())
        return None

def start_ui(config):
    """Start the appropriate UI based on the configuration."""
    ui_type = config.get_setting('ui_type')
    try:
        if ui_type == 'desktop':
            ui = DesktopUI()
            ui.initialize_ui()
            ui.show_main_window()
        elif ui_type == 'mobile':
            ui = MobileUI()
            ui.initialize_ui()
            ui.show_main_screen()
        elif ui_type == 'web':
            ui = WebUI()
            ui.start_web_server()
        else:
            logger.error(f"Invalid UI type: {ui_type}")
            return False
        
        if DEBUG:
            logger.debug(f"{ui_type.capitalize()} UI started successfully.")
        return True
    except Exception as e:
        logger.error(f"Error starting {ui_type} UI: {str(e)}")
        if DEBUG:
            logger.error(traceback.format_exc())
        return False

def main():
    """
    Main function to initialize and run the application.
    """
    logger.info("Starting secure communication suite application...")
    
    components = initialize_components()
    if components is None:
        logger.error("Failed to initialize components. Exiting application.")
        return
    
    config, *_ = components
    
    if not start_ui(config):
        logger.error("Failed to start UI. Exiting application.")
        return
    
    logger.info("Application started successfully.")
    
    # Here you would typically have a main event loop or keep the application running
    # For this example, we'll just log a message
    logger.info("Application is running. Press Ctrl+C to exit.")
    
    try:
        # Simulating the application running
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Application interrupted. Shutting down...")
    finally:
        # Perform any cleanup operations here
        logger.info("Application shutdown complete.")

if __name__ == "__main__":
    main()