"""
main.py

Purpose: Entry point of the secure messaging platform application.
Description: This file initializes all components of the application and runs the main program loop.
"""

import traceback
import sys
from app.core import authentication, encryption, messaging, file_sharing, calls
from app.ui import desktop_ui, mobile_ui, web_ui
from app.admin import dashboard, analytics, integration
from app.api import api_handler, bot_handler
from app.utils import config, logger

# Set DEBUG to True for development, False for production
DEBUG = True

def initialize_components():
    """Initialize all components of the application."""
    if DEBUG:
        print("Initializing components...")
    
    try:
        # Initialize core components
        authentication.initialize()
        encryption.initialize()
        messaging.initialize()
        file_sharing.initialize()
        calls.initialize()

        # Initialize UI components
        desktop_ui.initialize()
        mobile_ui.initialize()
        web_ui.initialize()

        # Initialize admin components
        dashboard.initialize()
        analytics.initialize()
        integration.initialize()

        # Initialize API components
        api_handler.initialize()
        bot_handler.initialize()

        if DEBUG:
            print("All components initialized successfully.")
    except Exception as e:
        logger.log_error(f"Error initializing components: {str(e)}")
        if DEBUG:
            print(f"Error initializing components: {str(e)}")
            print(traceback.format_exc())
        sys.exit(1)

def start_application():
    """Start the main application loop."""
    if DEBUG:
        print("Starting application...")
    
    try:
        # Start the appropriate UI based on the configuration
        ui_type = config.get_config_value("ui_type")
        if ui_type == "desktop":
            desktop_ui.start()
        elif ui_type == "mobile":
            mobile_ui.start()
        elif ui_type == "web":
            web_ui.start()
        else:
            raise ValueError(f"Invalid UI type: {ui_type}")

        if DEBUG:
            print(f"Application started with {ui_type} UI.")
    except Exception as e:
        logger.log_error(f"Error starting application: {str(e)}")
        if DEBUG:
            print(f"Error starting application: {str(e)}")
            print(traceback.format_exc())
        sys.exit(1)

def main():
    """Main function to run the application."""
    if DEBUG:
        print("Starting main function...")
    
    try:
        # Load configuration
        config.load_config("config.json")

        # Setup logger
        logger.setup_logger()

        # Initialize all components
        initialize_components()

        # Start the application
        start_application()

        if DEBUG:
            print("Application running successfully.")
    except Exception as e:
        logger.log_error(f"Critical error in main function: {str(e)}")
        if DEBUG:
            print(f"Critical error in main function: {str(e)}")
            print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()