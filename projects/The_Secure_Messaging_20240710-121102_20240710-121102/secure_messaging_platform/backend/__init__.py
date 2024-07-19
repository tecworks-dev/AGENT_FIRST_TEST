
# Purpose: Initialize the Flask application and register blueprints
# Description: This file creates and configures the Flask application instance,
# registers blueprints, and sets up necessary extensions.

import os
import traceback
from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, bcrypt, redis_client, celery
from .api import auth, messages

def create_app(config_class=Config):
    """
    Create and configure the Flask application instance.

    Args:
        config_class (object): Configuration class to use. Defaults to Config.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    redis_client.init_app(app)
    celery.init_app(app)

    # Register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(messages.bp)

    # Error handling
    @app.errorhandler(Exception)
    def handle_error(e):
        if app.config['DEBUG']:
            print(f"An error occurred: {str(e)}")
            print(traceback.format_exc())
        return {"error": "An unexpected error occurred"}, 500

    # Debug mode logging
    if app.config['DEBUG']:
        @app.before_request
        def log_request_info():
            print(f"Request: {request.method} {request.url}")
            print(f"Headers: {request.headers}")
            print(f"Body: {request.get_data()}")

        @app.after_request
        def log_response_info(response):
            print(f"Response: {response.status}")
            print(f"Headers: {response.headers}")
            print(f"Body: {response.get_data()}")
            return response

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

# Test cases using unittest
import unittest
from flask_testing import TestCase

class TestApp(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app

    def test_app_creation(self):
        self.assertIsNotNone(self.app)
        self.assertTrue(self.app.config['TESTING'])

    def test_error_handling(self):
        @self.app.route('/test_error')
        def test_error():
            raise Exception("Test error")

        response = self.client.get('/test_error')
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json)

if __name__ == '__main__':
    unittest.main()
