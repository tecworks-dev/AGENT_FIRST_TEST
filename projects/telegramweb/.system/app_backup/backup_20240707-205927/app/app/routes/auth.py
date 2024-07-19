from flask import Blueprint, request, jsonify, current_app, url_for, redirect, render_template
from app.services.auth import AuthService
from app.extensions import db
from flask_login import login_user, logout_user, login_required
import traceback

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    try:
        data = request.form.to_dict() if request.form else request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        auth_service = AuthService()
        result = auth_service.login(username, password)

        if result.get('success'):
            user = result.get('user')
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return jsonify({'success': True, 'redirect': next_page}), 200
        else:
            return jsonify({'error': result.get('message')}), 401

    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'An unexpected error occurred'}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.form.to_dict() if request.form else request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        auth_service = AuthService()
        result = auth_service.register(username, password)

        if result.get('status') == 'success':
            return jsonify(result), 201
        else:
            return jsonify({'error': result.get('message')}), 400

    except Exception as e:
        current_app.logger.error(f"Registration error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))