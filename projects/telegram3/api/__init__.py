from flask_restful import Api
from flask import Blueprint
import logging

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

def init_api(app):
    try:
        from .resources import UserResource, MessageResource

        api.add_resource(UserResource, '/api/users', '/api/users/<int:user_id>')
        api.add_resource(MessageResource, '/api/messages', '/api/messages/<int:message_id>')

        app.register_blueprint(api_bp)
        logger.info("API components initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing API components: {str(e)}")
        raise