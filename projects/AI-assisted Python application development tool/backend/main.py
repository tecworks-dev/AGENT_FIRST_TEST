
"""
backend/main.py

Entry point for the Flask application. Initializes the app, database, and WebSocket.
"""

import os
import traceback
from flask import Flask
from flask_socketio import SocketIO
from config import Config, DevelopmentConfig, ProductionConfig
from routes import init_app as init_routes
from models import db
from socket_events import init_socketio
from api_docs import setup_api_docs

DEBUG = True

def create_app():
    """Creates and configures the Flask app"""
    app = Flask(__name__)

    # Load configuration based on environment
    if os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Initialize database
    db.init_app(app)

    # Initialize routes
    init_routes(app)

    # Initialize SocketIO
    socketio = SocketIO(app)
    init_socketio(socketio)

    # Setup API documentation
    setup_api_docs(app)

    if DEBUG:
        print("Flask app created and configured")

    return app, socketio

def main():
    """Runs the application"""
    try:
        app, socketio = create_app()

        if DEBUG:
            print("Starting the application...")

        # Create database tables
        with app.app_context():
            db.create_all()
            if DEBUG:
                print("Database tables created")

        # Run the app
        port = int(os.environ.get('PORT', 5000))
        socketio.run(app, host='0.0.0.0', port=port, debug=DEBUG)

    except Exception as e:
        print(f"An error occurred while starting the application: {str(e)}")
        if DEBUG:
            traceback.print_exc()

if __name__ == '__main__':
    main()

# Unit tests
import unittest
from unittest.mock import patch, MagicMock

class TestMain(unittest.TestCase):

    @patch('main.Flask')
    @patch('main.SocketIO')
    @patch('main.init_routes')
    @patch('main.init_socketio')
    @patch('main.setup_api_docs')
    def test_create_app(self, mock_setup_api_docs, mock_init_socketio, mock_init_routes, mock_SocketIO, mock_Flask):
        app, socketio = create_app()
        
        mock_Flask.assert_called_once()
        mock_SocketIO.assert_called_once()
        mock_init_routes.assert_called_once()
        mock_init_socketio.assert_called_once()
        mock_setup_api_docs.assert_called_once()

    @patch('main.create_app')
    @patch('main.db')
    def test_main(self, mock_db, mock_create_app):
        mock_app = MagicMock()
        mock_socketio = MagicMock()
        mock_create_app.return_value = (mock_app, mock_socketio)

        main()

        mock_create_app.assert_called_once()
        mock_db.create_all.assert_called_once()
        mock_socketio.run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
