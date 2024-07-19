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
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
import traceback

bp = Blueprint('auth', __name__)
data_validator = DataValidator()
notification_service = NotificationService()
encryption_service = EncryptionService()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', title='Sign In', form=form)

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
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Send password reset email
            # Note: Implement the actual email sending logic here
            flash('Check your email for the instructions to reset your password', 'info')
        else:
            flash('Email not found in our records', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)

# Error handling
@bp.errorhandler(Exception)
def handle_error(e):
    current_app.logger.error(f"An error occurred in the auth module: {str(e)}")
    current_app.logger.error(traceback.format_exc())
    flash('An unexpected error occurred. Please try again later.', 'danger')
    return redirect(url_for('main.index'))