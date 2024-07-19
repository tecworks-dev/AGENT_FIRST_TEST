from flask import Blueprint, jsonify
from app.services.users import UserService

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    users = UserService.get_all_users()
    return jsonify(users)