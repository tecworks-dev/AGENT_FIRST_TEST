# main.py
"""
Entry point of the application. Initializes and runs the Flask app.
"""

import os
from app import create_app, db, socketio
from flask.logging import create_logger
from app.models.user import User
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_migrate import upgrade, init, Migrate, migrate

# Set DEBUG to True by default
DEBUG = True

def create_default_admin():
    """
    Creates a default admin user if it doesn't exist.
    """
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created.")

def initialize_migrations(app):
    """
    Initializes the migrations folder if it doesn't exist.
    """
    migrations_dir = os.path.join(app.root_path, 'migrations')
    if not os.path.exists(migrations_dir):
        with app.app_context():
            init()
        print("Migrations folder initialized.")

def create_migration(app):
    """
    Creates a new migration for the database schema changes.
    """
    with app.app_context():
        migrate()
    print("New migration created.")

def main():
    """
    Initializes and runs the Flask application.
    """
    try:
        # Create the Flask app
        app = create_app()
        
        # Create a logger
        logger = create_logger(app)
        
        if DEBUG:
            logger.debug("Application starting in DEBUG mode")
        
        if not os.path.exists("migrations"):
            # Initialize migrations
            initialize_migrations(app)
        
        # Create a new migration
        create_migration(app)
        
        with app.app_context():
            # Apply database migrations
            upgrade()
            
            # Create tables (this will be ignored if tables already exist)
            db.create_all()
            
            create_default_admin()
        
        # Add root route
        @app.route('/')
        def root():
            return render_template('user_interface.html')
        
        # Run the app with SocketIO
        port = int(os.environ.get("PORT", 5000))
        socketio.run(app, host='0.0.0.0', port=port, debug=DEBUG)
    
    except Exception as e:
        if DEBUG:
            print(f"An error occurred while starting the application: {str(e)}")
        raise

# IMPORTANT: do not remove main function as automated test will fail
# IMPORTANT: do not remove this comment
if __name__ == "__main__":
    main()

# For testing purposes
import unittest

class TestMain(unittest.TestCase):
    def test_main_function_exists(self):
        """Test that the main function exists"""
        self.assertTrue(callable(main))

if __name__ == "__main__":
    unittest.main()