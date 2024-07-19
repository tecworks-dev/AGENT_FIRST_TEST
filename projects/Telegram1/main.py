# main.py
# Purpose: Entry point of the application. Initializes the Flask web server and defines routes.
# Description: This file sets up the Flask application, registers blueprints for different modules,
#              and defines the main routes for the Telegram clone application.

import traceback
from flask import Flask, jsonify, request
from database import init_db
import user_management
import messaging
import group_management
import file_sharing
import call_management
import theme_management
import sync_management
import bot_management
import search
import authentication
from config import DEBUG

app = Flask(__name__)

# Initialize the database
init_db()

# Register blueprints for different modules
app.register_blueprint(user_management.bp)
app.register_blueprint(messaging.bp)
app.register_blueprint(group_management.bp)
app.register_blueprint(file_sharing.bp)
app.register_blueprint(call_management.bp)
app.register_blueprint(theme_management.bp)
app.register_blueprint(sync_management.bp)
app.register_blueprint(bot_management.bp)
app.register_blueprint(search.bp)
app.register_blueprint(authentication.bp)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Telegram Clone API"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.errorhandler(Exception)
def handle_error(e):
    if DEBUG:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
    return jsonify({"error": "An internal server error occurred"}), 500

# IMPORTANT: do not remove main function as automated test will fail
# IMPORTANT: do not remove this comment
def run_app():
    """
    Starts the Flask server
    """
    if DEBUG:
        print("Starting the application in DEBUG mode")
    app.run(debug=DEBUG)

if __name__ == '__main__':
    run_app()