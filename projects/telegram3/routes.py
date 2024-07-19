# routes.py
"""
URL routing for the application.
This file defines the routes and views for the web application.
"""

import flask
import traceback
from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_login import login_required, current_user

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

DEBUG = True

def init_routes(app):
    """
    Registers blueprints with the app.
    
    :param app: Flask application instance
    :return: None
    """
    try:
        app.register_blueprint(main)
        if DEBUG:
            print("Routes initialized successfully")
    except Exception as e:
        print(f"Error initializing routes: {str(e)}")
        if DEBUG:
            traceback.print_exc()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

@main.route('/')
def index():
    """
    Renders the index page.
    
    :return: Rendered template for the index page
    """
    try:
        if DEBUG:
            print("Rendering index page")
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering index page: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        return "An error occurred while loading the page", 500

@main.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles login functionality.
    
    :return: Rendered template for the login page or redirects to chat page on successful login
    """
    try:
        if DEBUG:
            print("Handling login request")
        form = LoginForm()
        if form.validate_on_submit():
            # Here you would typically validate the login credentials
            # For now, we'll just redirect to the chat page
            flash('Login successful!', 'success')
            return redirect(url_for('main.chat'))
        return render_template('login.html', form=form)
    except Exception as e:
        print(f"Error handling login: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        flash('An error occurred during login. Please try again.', 'error')
        return render_template('login.html', form=form), 500

@main.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.
    
    :return: Rendered template for the registration page or redirects to login page on successful registration
    """
    try:
        if DEBUG:
            print("Handling registration request")
        form = RegistrationForm()
        if form.validate_on_submit():
            # Here you would typically handle the registration process
            # For now, we'll just redirect to the login page
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('main.login'))
        return render_template('register.html', form=form)
    except Exception as e:
        print(f"Error handling registration: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        flash('An error occurred during registration. Please try again.', 'error')
        return render_template('register.html', form=form), 500

@main.route('/chat')
@login_required
def chat():
    """
    Renders the chat page.
    
    :return: Rendered template for the chat page
    """
    try:
        if DEBUG:
            print("Rendering chat page")
        return render_template('chat.html', username=current_user.username)
    except Exception as e:
        print(f"Error rendering chat page: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        flash('An error occurred while loading the chat page. Please try again.', 'error')
        return redirect(url_for('main.index'))

# Error handling routes
@main.app_errorhandler(404)
def not_found_error(error):
    """
    Handles 404 Not Found errors.
    
    :param error: Error object
    :return: Rendered template for 404 error
    """
    if DEBUG:
        print(f"404 error: {error}")
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_error(error):
    """
    Handles 500 Internal Server Error.
    
    :param error: Error object
    :return: Rendered template for 500 error
    """
    if DEBUG:
        print(f"500 error: {error}")
        traceback.print_exc()
    return render_template('500.html'), 500