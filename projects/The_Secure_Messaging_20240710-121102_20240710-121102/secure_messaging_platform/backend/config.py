
# Purpose: Define configuration settings for the Secure Messaging Platform application
# Description: This file contains the Config class that stores configuration variables as class attributes.

import os
import traceback

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour

    # Redis configuration
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'

    # Celery configuration
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

    # File upload configuration
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Encryption key (in a real-world scenario, this should be stored securely)
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or 'default-encryption-key'

    # Debug mode
    DEBUG = True

    @classmethod
    def init_app(cls, app):
        """
        Initialize the application with the configuration.

        :param app: Flask application instance
        """
        try:
            app.config.from_object(cls)
            
            # Ensure upload folder exists
            os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)

            if cls.DEBUG:
                print(f"Initialized app with config: {cls.__name__}")
                print(f"Database URI: {cls.SQLALCHEMY_DATABASE_URI}")
                print(f"Redis URL: {cls.REDIS_URL}")
                print(f"Upload folder: {cls.UPLOAD_FOLDER}")
        except Exception as e:
            print(f"Error initializing app config: {str(e)}")
            print(traceback.format_exc())

# Test configuration for unit tests
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Add more configuration classes if needed (e.g., ProductionConfig, DevelopmentConfig)

import unittest

class TestConfigTestCase(unittest.TestCase):
    def test_config_values(self):
        self.assertIsNotNone(Config.SECRET_KEY)
        self.assertIsNotNone(Config.SQLALCHEMY_DATABASE_URI)
        self.assertFalse(Config.SQLALCHEMY_TRACK_MODIFICATIONS)
        self.assertIsNotNone(Config.JWT_SECRET_KEY)
        self.assertEqual(Config.JWT_ACCESS_TOKEN_EXPIRES, 3600)
        self.assertIsNotNone(Config.REDIS_URL)
        self.assertIsNotNone(Config.CELERY_BROKER_URL)
        self.assertIsNotNone(Config.CELERY_RESULT_BACKEND)
        self.assertIsNotNone(Config.UPLOAD_FOLDER)
        self.assertEqual(Config.MAX_CONTENT_LENGTH, 16 * 1024 * 1024)
        self.assertIsNotNone(Config.ENCRYPTION_KEY)
        self.assertTrue(Config.DEBUG)

    def test_test_config(self):
        self.assertTrue(TestConfig.TESTING)
        self.assertEqual(TestConfig.SQLALCHEMY_DATABASE_URI, 'sqlite:///:memory:')
        self.assertFalse(TestConfig.WTF_CSRF_ENABLED)

if __name__ == '__main__':
    unittest.main()
