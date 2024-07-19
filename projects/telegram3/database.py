
# database.py
"""
Database setup and models for the messaging platform.
This file defines the database initialization function and the User and Message models.
"""

import traceback
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

DEBUG = True

def init_db(app):
    """
    Initializes the database with the Flask app.
    
    :param app: Flask application instance
    :return: None
    """
    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()
        if DEBUG:
            print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        if DEBUG:
            traceback.print_exc()

class User(db.Model):
    """User model for storing user related details"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

class Message(db.Model):
    """Message model for storing message related details"""
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', foreign_keys=[sender_id], backref=db.backref('sent_messages', lazy='dynamic'))
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref=db.backref('received_messages', lazy='dynamic'))

    def __repr__(self):
        return f'<Message {self.id}>'

if DEBUG:
    print("Database models defined: User, Message")
