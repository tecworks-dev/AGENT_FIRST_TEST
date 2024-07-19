
# Purpose: Initialize Flask extensions for the Secure Messaging Platform
# Description: This file sets up and configures various Flask extensions used throughout the application

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_redis import FlaskRedis
from celery import Celery
import traceback

# Initialize SQLAlchemy for database operations
db = SQLAlchemy()

# Initialize Flask-Migrate for database migrations
migrate = Migrate()

# Initialize Flask-JWT-Extended for JSON Web Token handling
jwt = JWTManager()

# Initialize Flask-Bcrypt for password hashing
bcrypt = Bcrypt()

# Initialize Flask-Redis for Redis operations
redis_client = FlaskRedis()

# Initialize Celery for background tasks
celery = Celery()

def init_extensions(app):
    """
    Initialize and configure all Flask extensions
    :param app: Flask application instance
    """
    try:
        db.init_app(app)
        migrate.init_app(app, db)
        jwt.init_app(app)
        bcrypt.init_app(app)
        redis_client.init_app(app)

        celery.conf.update(app.config)

        if app.config['DEBUG']:
            print("Extensions initialized successfully")
    except Exception as e:
        print(f"Error initializing extensions: {str(e)}")
        traceback.print_exc()

# Unit tests
import unittest
from unittest.mock import MagicMock, patch

class TestExtensions(unittest.TestCase):

    @patch('flask_sqlalchemy.SQLAlchemy.init_app')
    @patch('flask_migrate.Migrate.init_app')
    @patch('flask_jwt_extended.JWTManager.init_app')
    @patch('flask_bcrypt.Bcrypt.init_app')
    @patch('flask_redis.FlaskRedis.init_app')
    def test_init_extensions(self, mock_redis, mock_bcrypt, mock_jwt, mock_migrate, mock_db):
        mock_app = MagicMock()
        mock_app.config = {'DEBUG': True}

        init_extensions(mock_app)

        mock_db.assert_called_once_with(mock_app)
        mock_migrate.assert_called_once_with(mock_app, db)
        mock_jwt.assert_called_once_with(mock_app)
        mock_bcrypt.assert_called_once_with(mock_app)
        mock_redis.assert_called_once_with(mock_app)

    @patch('traceback.print_exc')
    def test_init_extensions_error(self, mock_traceback):
        mock_app = MagicMock()
        mock_app.config = {'DEBUG': True}

        # Simulate an error during initialization
        with patch('flask_sqlalchemy.SQLAlchemy.init_app', side_effect=Exception("Test error")):
            init_extensions(mock_app)

        mock_traceback.assert_called_once()

if __name__ == '__main__':
    unittest.main()
