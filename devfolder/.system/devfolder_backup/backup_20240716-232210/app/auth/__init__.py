
# app/auth/__init__.py
"""
Implements authentication-related functionality for the AI Software Factory application.
This module handles user authentication, registration, and password reset functionality.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from app.utils.data_validator import DataValidator
from app.services.notification_service import NotificationService
from app.utils.encryption_service import EncryptionService
import traceback

bp = Blueprint('auth', __name__)
data_validator = DataValidator()
notification_service = NotificationService()
encryption_service = EncryptionService()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        flash('Logged in successfully.', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validate input
        if not data_validator.validate_email(email):
            flash('Invalid email address.', 'danger')
            return redirect(url_for('auth.register'))
        
        if not data_validator.validate_username(username):
            flash('Invalid username. It should be 3-20 characters long and contain only letters, numbers, and underscores.', 'danger')
            return redirect(url_for('auth.register'))
        
        if not data_validator.validate_password(password):
            flash('Password must be at least 8 characters long and contain a mix of uppercase, lowercase, numbers, and symbols.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user
        new_user = User(email=email, username=username, password_hash=generate_password_hash(password, method='sha256'))
        
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            notification_service.send_notification(new_user.id, f"Welcome to AI Software Factory, {new_user.username}!")
            flash('Registration successful. Welcome!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error during user registration: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            try:
                # Generate a secure token
                token = encryption_service.encrypt(f"{user.id}:{user.email}")
                
                # Send password reset email
                # Note: In a production environment, you would use a proper email service here
                print(f"Password reset link: {url_for('auth.reset_password_confirm', token=token, _external=True)}")
                
                flash('Password reset instructions have been sent to your email.', 'info')
            except Exception as e:
                current_app.logger.error(f"Error during password reset: {str(e)}")
                flash('An error occurred. Please try again later.', 'danger')
        else:
            flash('Email not found.', 'danger')
        
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html')

@bp.route('/reset_password_confirm/<token>', methods=['GET', 'POST'])
def reset_password_confirm(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    try:
        decrypted_token = encryption_service.decrypt(token)
        user_id, email = decrypted_token.split(':')
        user = User.query.get(int(user_id))
        
        if not user or user.email != email:
            flash('Invalid or expired reset link.', 'danger')
            return redirect(url_for('auth.login'))
        
        if request.method == 'POST':
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if new_password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return render_template('reset_password_confirm.html')
            
            if not data_validator.validate_password(new_password):
                flash('Password must be at least 8 characters long and contain a mix of uppercase, lowercase, numbers, and symbols.', 'danger')
                return render_template('reset_password_confirm.html')
            
            user.password_hash = generate_password_hash(new_password, method='sha256')
            db.session.commit()
            
            flash('Your password has been reset successfully.', 'success')
            return redirect(url_for('auth.login'))
        
        return render_template('reset_password_confirm.html')
    
    except Exception as e:
        current_app.logger.error(f"Error during password reset confirmation: {str(e)}")
        flash('An error occurred. Please try again.', 'danger')
        return redirect(url_for('auth.login'))

def init_app(app):
    if app.config.get('DEBUG', False):
        @bp.route('/debug_users')
        def debug_users():
            users = User.query.all()
            return render_template('debug_users.html', users=users)

# Error handling
@bp.errorhandler(Exception)
def handle_error(e):
    current_app.logger.error(f"An error occurred in the auth module: {str(e)}")
    current_app.logger.error(traceback.format_exc())
    flash('An unexpected error occurred. Please try again later.', 'danger')
    return redirect(url_for('main.index'))
