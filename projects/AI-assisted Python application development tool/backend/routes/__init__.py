
# Purpose: Initialize routes package and combine all route blueprints
# Description: This file imports all route blueprints and provides a function to register them with the Flask app

import logging
import traceback
from flask import Blueprint
from .auth import auth_bp
from .messages import messages_bp
from .groups import groups_bp
from .files import files_bp
from .admin import admin_bp

# Create a logger for this module
logger = logging.getLogger(__name__)

# Create a main blueprint to combine all route blueprints
main_bp = Blueprint('main', __name__)

def init_app(app):
    """
    Registers all blueprints with the Flask app
    
    Args:
        app: Flask application instance
    """
    try:
        # Register individual blueprints
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(messages_bp, url_prefix='/messages')
        app.register_blueprint(groups_bp, url_prefix='/groups')
        app.register_blueprint(files_bp, url_prefix='/files')
        app.register_blueprint(admin_bp, url_prefix='/admin')
        
        # Register the main blueprint
        app.register_blueprint(main_bp)
        
        logger.info("All blueprints registered successfully")
    except Exception as e:
        logger.error(f"Error registering blueprints: {str(e)}")
        if app.debug:
            logger.error(traceback.format_exc())
        raise

# Debug statements
if __name__ == "__main__":
    import unittest
    
    class TestRoutes(unittest.TestCase):
        def setUp(self):
            from flask import Flask
            self.app = Flask(__name__)
            self.app.config['TESTING'] = True
            self.app.config['DEBUG'] = True
        
        def test_init_app(self):
            init_app(self.app)
            self.assertTrue(len(self.app.blueprints) > 0, "Blueprints should be registered")
        
        def test_blueprint_registration(self):
            init_app(self.app)
            self.assertIn('auth', self.app.blueprints)
            self.assertIn('messages', self.app.blueprints)
            self.assertIn('groups', self.app.blueprints)
            self.assertIn('files', self.app.blueprints)
            self.assertIn('admin', self.app.blueprints)
            self.assertIn('main', self.app.blueprints)
    
    unittest.main()
