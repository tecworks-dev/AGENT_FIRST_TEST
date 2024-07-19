
# app/__init__.py
"""
Initializes the Flask application and its extensions.
This module sets up the Flask app, configures it, and initializes all necessary extensions.
"""

import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
socketio = SocketIO()

def create_app(config_class=Config):
    """
    Creates and configures the Flask application.
    
    Args:
        config_class: Configuration class to use (default: Config)
    
    Returns:
        Initialized Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    socketio.init_app(app)

    # Set up login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Import models
    from app.models.user import User
    from app.models.message import Message
    from app.models.group import Group
    from app.models.channel import Channel
    from app.models.file import File

    # Import and register blueprints
    from app.routes import auth, messaging, groups, channels, calls, admin
    app.register_blueprint(auth.auth)
    app.register_blueprint(messaging.messaging)
    app.register_blueprint(groups.groups)
    app.register_blueprint(channels.channels)
    app.register_blueprint(calls.calls)
    app.register_blueprint(admin.admin, url_prefix='/admin')

    # Import and register API routes
    from app.api.v1 import routes as api_routes
    app.register_blueprint(api_routes.api_bp, url_prefix='/api/v1')

    # Add favicon route
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    # Error handling
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Not Found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal Server Error'}, 500

    # Shell context for flask cli
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Message': Message, 'Group': Group, 'Channel': Channel, 'File': File}

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

# Debug mode
DEBUG = True

if DEBUG:
    print("Debug mode is ON")
else:
    print("Debug mode is OFF")
