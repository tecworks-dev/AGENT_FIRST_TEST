
# config.py
# Purpose: Configuration settings for the application
# Description: This file contains configuration classes for different environments

import os
import unittest

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = False
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max-limit
    
    # WebSocket settings
    SOCKETIO_ASYNC_MODE = 'eventlet'
    
    # API settings
    API_VERSION = 'v1'
    
    # Logging
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Development-specific settings."""
    DEBUG = True
    
    # Add any development-specific settings here
    SQLALCHEMY_ECHO = True  # Log SQL queries

class ProductionConfig(Config):
    """Production-specific settings."""
    DEBUG = False
    
    # Add any production-specific settings here
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

class TestingConfig(Config):
    """Testing-specific settings."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Dictionary to easily switch between configurations
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Unit tests for configuration
class TestConfig(unittest.TestCase):
    def test_config_values(self):
        self.assertTrue(Config.SECRET_KEY)
        self.assertTrue(Config.SQLALCHEMY_DATABASE_URI)
        self.assertFalse(Config.SQLALCHEMY_TRACK_MODIFICATIONS)
    
    def test_development_config(self):
        dev_config = DevelopmentConfig()
        self.assertTrue(dev_config.DEBUG)
        self.assertTrue(dev_config.SQLALCHEMY_ECHO)
    
    def test_production_config(self):
        prod_config = ProductionConfig()
        self.assertFalse(prod_config.DEBUG)
    
    def test_testing_config(self):
        test_config = TestingConfig()
        self.assertTrue(test_config.TESTING)
        self.assertEqual(test_config.SQLALCHEMY_DATABASE_URI, 'sqlite:///:memory:')

if __name__ == '__main__':
    unittest.main()
