
"""
Web-based user interface implementation.

This module manages the web-based user interface for the secure messaging platform.
It provides methods for rendering login and main pages, as well as displaying messages to users.
"""

import traceback
from flask import Flask, render_template, request, jsonify
from app.core import messaging, file_sharing, calls
from app.utils import config, logger

DEBUG = True

class WebUI:
    """Manages the web-based user interface."""

    def __init__(self):
        """Initialize the WebUI class."""
        self.app = Flask(__name__)
        self.logger = logger.setup_logger()
        self.config = config.load_config("config.json")

        if DEBUG:
            self.logger.info("WebUI initialized in debug mode")

        # Set up routes
        self.app.route("/")(self.render_login_page)
        self.app.route("/main")(self.render_main_page)
        self.app.route("/message", methods=["POST"])(self.handle_message)

    def render_login_page(self):
        """Render the login page."""
        try:
            if DEBUG:
                self.logger.info("Rendering login page")
            return render_template("login.html")
        except Exception as e:
            self.logger.error(f"Error rendering login page: {str(e)}")
            self.logger.error(traceback.format_exc())
            return self.display_message("An error occurred while loading the login page.")

    def render_main_page(self):
        """Render the main page."""
        try:
            if DEBUG:
                self.logger.info("Rendering main page")
            # Here you would typically check if the user is authenticated
            # For simplicity, we're just rendering the main page
            return render_template("main.html")
        except Exception as e:
            self.logger.error(f"Error rendering main page: {str(e)}")
            self.logger.error(traceback.format_exc())
            return self.display_message("An error occurred while loading the main page.")

    def display_message(self, message: str):
        """Display a message to the user."""
        if DEBUG:
            self.logger.info(f"Displaying message: {message}")
        return render_template("message.html", message=message)

    def handle_message(self):
        """Handle incoming messages."""
        try:
            data = request.json
            sender_id = data.get("sender_id")
            recipient_id = data.get("recipient_id")
            message_content = data.get("message")

            if DEBUG:
                self.logger.info(f"Handling message: {sender_id} -> {recipient_id}: {message_content}")

            # Use the messaging module to send the message
            success = messaging.send_message(sender_id, recipient_id, message_content)

            if success:
                return jsonify({"status": "success", "message": "Message sent successfully"})
            else:
                return jsonify({"status": "error", "message": "Failed to send message"}), 400
        except Exception as e:
            self.logger.error(f"Error handling message: {str(e)}")
            self.logger.error(traceback.format_exc())
            return jsonify({"status": "error", "message": "An error occurred while processing the message"}), 500

    def run(self):
        """Run the Flask application."""
        try:
            if DEBUG:
                self.logger.info("Starting WebUI Flask application")
            self.app.run(debug=DEBUG)
        except Exception as e:
            self.logger.error(f"Error running WebUI: {str(e)}")
            self.logger.error(traceback.format_exc())

# This allows the Flask app to be run directly for testing purposes
if __name__ == "__main__":
    web_ui = WebUI()
    web_ui.run()
