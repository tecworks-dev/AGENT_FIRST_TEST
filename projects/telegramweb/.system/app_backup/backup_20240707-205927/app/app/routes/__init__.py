from .auth import auth_bp
from .messages import messages_bp
from .media import media_bp
from .search import search_bp
from .main import main_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(media_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(main_bp)