import traceback
from flask import session, redirect, url_for, request
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from database import execute_query

def init_user_management(app):
    app.secret_key = app.config['SECRET_KEY']  # Make sure this is set in your config

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def register_user(username, password, email):
    try:
        # Check if username or email already exists
        query = "SELECT * FROM users WHERE username = ? OR email = ?"
        result = execute_query(query, (username, email))
        
        if result:
            return False, "Username or email already exists."

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert new user into the database
        query = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
        execute_query(query, (username, hashed_password, email))

        return True, "User registered successfully."
    except Exception as e:
        traceback.print_exc()
        return False, f"An error occurred during registration: {str(e)}"

def authenticate_user(username, password):
    try:
        query = "SELECT * FROM users WHERE username = ?"
        result = execute_query(query, (username,))

        if result and check_password_hash(result[0][2], password):
            session['user_id'] = result[0][0]
            session['user'] = {'id': result[0][0], 'username': result[0][1], 'email': result[0][3]}
            return True
        return False
    except Exception as e:
        traceback.print_exc()
        return False

def logout():
    session.pop('user_id', None)
    session.pop('user', None)
    return True

def get_current_user():
    if 'user_id' in session:
        return session['user']
    return None

def update_profile(user_id, data):
    try:
        allowed_fields = ['username', 'email', 'full_name', 'bio']
        update_fields = []
        update_values = []

        for field, value in data.items():
            if field in allowed_fields:
                update_fields.append(f"{field} = ?")
                update_values.append(value)

        if not update_fields:
            return False, "No valid fields to update."

        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
        update_values.append(user_id)

        execute_query(query, tuple(update_values))

        return True, "Profile updated successfully."
    except Exception as e:
        traceback.print_exc()
        return False, f"An error occurred while updating the profile: {str(e)}"