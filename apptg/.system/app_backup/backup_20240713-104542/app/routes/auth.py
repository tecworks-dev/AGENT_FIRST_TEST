# Authentication routes (login, register, logout)
# This file handles user authentication, including login, registration, and logout functionalities.

import traceback
from flask import Blueprint, request, jsonify, current_app, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user import User
from app.utils import validators
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('root'))

    if request.method == 'POST':
        try:
            data = request.get_json() or request.form
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return jsonify({'message': 'Username, email, and password are required'}), 400

            if User.query.filter_by(username=username).first():
                return jsonify({'message': 'Username already exists'}), 400

            if User.query.filter_by(email=email).first():
                return jsonify({'message': 'Email already exists'}), 400

            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'User registered successfully'}), 201
        except Exception as e:
            if current_app.config['DEBUG']:
                print(f"Error in register route: {str(e)}")
                traceback.print_exc()
            return jsonify({'message': 'An error occurred during registration'}), 500

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root'))

    if request.method == 'POST':
        try:
            data = request.get_json() or request.form
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return jsonify({'message': 'Email and password are required'}), 400

            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                if user.is_banned:
                    return jsonify({'message': 'This account has been banned'}), 403
                login_user(user)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('admin.admin_panel') if user.is_admin else url_for('root'))
            else:
                return jsonify({'message': 'Invalid email or password'}), 401

        except Exception as e:
            if current_app.config['DEBUG']:
                print(f"Error in login route: {str(e)}")
                traceback.print_exc()
            return jsonify({'message': 'An error occurred during login'}), 500
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))