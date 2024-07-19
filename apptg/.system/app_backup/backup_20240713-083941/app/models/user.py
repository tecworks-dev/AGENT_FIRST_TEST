
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)

    # Add the relationship for created groups
    created_groups = db.relationship('Group', back_populates='creator', foreign_keys='Group.creator_id')
    
    # Add the relationship for created channels
    created_channels = db.relationship('Channel', back_populates='creator', foreign_keys='Channel.creator_id')
    
    # Add the relationship for subscribed channels
    subscribed_channels = db.relationship('Channel', secondary='channel_subscribers', back_populates='subscribers')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_administrator(self):
        return self.is_admin

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_banned': self.is_banned
        }
