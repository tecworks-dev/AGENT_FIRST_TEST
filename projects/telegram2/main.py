"""
main.py

Purpose: Entry point of the secure messaging platform application.
Description: This file initializes all components of the application and runs the main program loop.
"""

import sys
import traceback
from app.utils import config, logger
from app.core import authentication, encryption, messaging, file_sharing, calls
from app.ui import web_ui
from app.admin import dashboard, analytics, integration
from app.api import api_handler, bot_handler

# Set up logger
log = logger.setup_logger()

def initialize_components():
    """Initialize all components of the application."""
    components = [
        authentication, encryption, messaging, file_sharing, calls,
        dashboard, analytics, integration, api_handler, bot_handler
    ]
    
    for component in components:
        try:
            if hasattr(component, 'initialize'):
                component.initialize()
            log.info(f"{component.__name__} initialized successfully.")
        except Exception as e:
            log.error(f"Error initializing {component.__name__}: {str(e)}")
            log.error(traceback.format_exc())
            return False
    return True

def main():
    """Main function to run the application."""
    try:
        # Load configuration
        app_config = config.load_config("config.json")
        if not app_config:
            log.error("Failed to load configuration. Exiting.")
            return

        log.info("Initializing application components")

        if not initialize_components():
            log.error("Failed to initialize components. Exiting.")
            return

        # Initialize and run the web UI
        ui = web_ui.WebUI()
        ui.run()

        log.info("Application running successfully.")
    except Exception as e:
        log.error(f"Critical error in main function: {str(e)}")
        log.error(traceback.format_exc())
    finally:
        log.info("Application shutting down.")

if __name__ == "__main__":
    main()