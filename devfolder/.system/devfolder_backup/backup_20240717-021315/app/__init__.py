
# app/__init__.py
# Purpose: Initialize the Flask application and configure extensions
# Description: This file sets up the Flask app, database, migrations, login manager, and WebSocket support

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import Config
import logging
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
socketio = SocketIO()

def create_app(config=None):
    app = Flask(__name__)
    
    if config is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    socketio.init_app(app)

    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # Set up logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        try:
            log_file = 'logs/ai_software_factory.log'
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
        except PermissionError:
            print("Warning: Unable to set up file logging due to permission error.")
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('AI Software Factory startup')

    # Add user_loader function
    from app.models import User

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Import models at the bottom to avoid circular imports
from app import models
