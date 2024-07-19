# Purpose: Authentication routes (login, register, logout)
# Description: This file contains route handlers for user authentication,
#              including registration, login, and logout.

from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User
from app import db
import traceback

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """Registers a new user"""
    if current_user.is_authenticated:
        return jsonify({"message": "Already logged in"}), 400

    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({"message": "Username, email, and password are required"}), 400

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
        traceback.print_exc()
        return jsonify({"message": "An error occurred while registering the user"}), 500

@auth.route('/login', methods=['POST'])
def login():
    """Logs in a user"""
    if current_user.is_authenticated:
        return jsonify({"message": "Already logged in"}), 400

    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if user.is_banned:
                return jsonify({"message": "This account has been banned"}), 403
            login_user(user)
            return jsonify({"message": "Logged in successfully"}), 200
        else:
            return jsonify({"message": "Invalid email or password"}), 401
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": "An error occurred during login"}), 500

@auth.route('/logout')
@login_required
def logout():
    """Logs out a user"""
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200