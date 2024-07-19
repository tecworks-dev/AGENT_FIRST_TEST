# Purpose: Admin panel routes
# Description: This file contains routes for administrative functions such as retrieving users,
#              banning users, and deleting groups or channels.

import traceback
from flask import Blueprint, request, jsonify, render_template, current_app, redirect, url_for
from flask_login import login_required, current_user
from app.models import User, Group, Channel
from app import db

admin = Blueprint('admin', __name__)

DEBUG = True

@admin.route('/')
def admin_login():
    """
    Renders the admin login page.
    """
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.admin_panel'))
    return render_template('admin_login.html')

@admin.route('/login', methods=['POST'])
def admin_login_post():
    """
    Handles admin login POST request.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password) and user.is_admin:
        login_user(user)
        return jsonify({"message": "Admin logged in successfully"}), 200
    else:
        return jsonify({"message": "Invalid email or password, or not an admin"}), 401

@admin.route('/panel')
@login_required
def admin_panel():
    """
    Renders the admin panel interface.
    """
    if not current_user.is_admin:
        return jsonify({"message": "Access denied. Admin privileges required."}), 403
    return render_template('admin_interface.html')

# ... (rest of the file remains unchanged)