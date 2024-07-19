
# app/errors/__init__.py

"""
Initializes the Flask application with lazy imports and distributed initialization logic.
This file uses lazy loading techniques to improve startup time and reduce memory usage.
The initialization logic is distributed across multiple functions for better organization and maintainability.
"""

import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
socketio = SocketIO()

def create_app(config_class=Config):
    """Creates and configures the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_extensions(app)
    register_blueprints(app)
    configure_logging(app)

    return app

def init_extensions(app):
    """Initializes Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth.login'
    socketio.init_app(app)

def register_blueprints(app):
    """Registers application blueprints."""
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

def configure_logging(app):
    """Sets up application logging."""
    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/ai_software_factory.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('AI Software Factory startup')

# Error handlers
from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app = create_app()
    socketio.run(app)
