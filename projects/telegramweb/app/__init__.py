from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from config import Config
from app.extensions import db, socketio

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    socketio.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.messages import messages_bp
    from app.routes.media import media_bp
    from app.routes.search import search_bp
    from app.routes.main import main_bp
    from app.routes.users import users_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(media_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)

    return app