
"""
main.py - Entry point of the Secure Messaging Platform application.

This module initializes and runs the Flask application for the Secure Messaging Platform.
It imports the necessary modules and defines the main function to start the application.
"""

import os
import traceback
from backend import create_app
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set DEBUG mode
DEBUG = True

def main():
    """
    Initialize and run the Flask application.

    This function creates the Flask app instance, configures it,
    and runs it in debug mode if DEBUG is set to True.
    """
    try:
        app = create_app()
        
        if DEBUG:
            logger.info("Starting the application in DEBUG mode")
            app.config['DEBUG'] = True
        
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"An error occurred while starting the application: {str(e)}")
        if DEBUG:
            logger.error(traceback.format_exc())

# IMPORTANT: do not remove main function as automated test will fail
if __name__ == "__main__":
    main()

# Test suite for main.py
import unittest
from unittest.mock import patch, MagicMock

class TestMain(unittest.TestCase):

    @patch('backend.create_app')
    def test_main_function(self, mock_create_app):
        # Mock the create_app function
        mock_app = MagicMock()
        mock_create_app.return_value = mock_app

        # Call the main function
        main()

        # Assert that create_app was called
        mock_create_app.assert_called_once()

        # Assert that app.run was called with the correct arguments
        mock_app.run.assert_called_once_with(host='0.0.0.0', port=5000)

    @patch('main.logger')
    @patch('backend.create_app')
    def test_main_function_exception_handling(self, mock_create_app, mock_logger):
        # Mock create_app to raise an exception
        mock_create_app.side_effect = Exception("Test exception")

        # Call the main function
        main()

        # Assert that the logger.error was called
        mock_logger.error.assert_called()

if __name__ == '__main__':
    unittest.main()
