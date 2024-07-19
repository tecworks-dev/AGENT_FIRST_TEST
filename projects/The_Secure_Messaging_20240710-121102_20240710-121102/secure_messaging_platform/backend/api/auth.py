
# Purpose: Handles user authentication and authorization
# Description: This module provides endpoints for user registration, login, and logout

import traceback
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models.user import User
from ..extensions import db, jwt, bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return jsonify({"message": "Missing required fields"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Username already exists"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email already exists"}), 400

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        if __debug__:
            print(f"Error in register: {str(e)}")
            traceback.print_exc()
        return jsonify({"message": "An error occurred during registration"}), 500

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"message": "Missing username or password"}), 400

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        if __debug__:
            print(f"Error in login: {str(e)}")
            traceback.print_exc()
        return jsonify({"message": "An error occurred during login"}), 500

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # In a stateless JWT system, we don't need to do anything server-side for logout
        # The client is responsible for discarding the token
        return jsonify({"message": "Successfully logged out"}), 200
    except Exception as e:
        if __debug__:
            print(f"Error in logout: {str(e)}")
            traceback.print_exc()
        return jsonify({"message": "An error occurred during logout"}), 500

# For testing purposes
if __name__ == '__main__':
    import unittest

    class TestAuth(unittest.TestCase):
        def setUp(self):
            # Set up test client and database
            pass

        def test_register(self):
            # Test user registration
            pass

        def test_login(self):
            # Test user login
            pass

        def test_logout(self):
            # Test user logout
            pass

    unittest.main()
