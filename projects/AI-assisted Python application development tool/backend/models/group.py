
# Group model and related classes for the secure messaging platform
# This file defines the Group and GroupMember models using SQLAlchemy

from flask_sqlalchemy import SQLAlchemy
from backend.database import db
from datetime import datetime
import traceback

class Group(db.Model):
    """
    Represents a group in the system
    """
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    members = db.relationship('GroupMember', back_populates='group', cascade='all, delete-orphan')
    messages = db.relationship('Message', back_populates='group', cascade='all, delete-orphan')

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Group {self.name}>'

    def to_dict(self):
        """
        Convert the Group object to a dictionary
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'member_count': len(self.members)
        }

class GroupMember(db.Model):
    """
    Represents a group membership
    """
    __tablename__ = 'group_members'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(20), default='member')  # e.g., 'admin', 'member'
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    group = db.relationship('Group', back_populates='members')
    user = db.relationship('User', back_populates='group_memberships')

    def __init__(self, group_id, user_id, role='member'):
        self.group_id = group_id
        self.user_id = user_id
        self.role = role

    def __repr__(self):
        return f'<GroupMember {self.user_id} in Group {self.group_id}>'

    def to_dict(self):
        """
        Convert the GroupMember object to a dictionary
        """
        return {
            'id': self.id,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'role': self.role,
            'joined_at': self.joined_at.isoformat()
        }

# Debug function to print model details
def print_model_details():
    if __debug__:
        print("Group Model Details:")
        print(f"Table name: {Group.__tablename__}")
        print("Columns:")
        for column in Group.__table__.columns:
            print(f"- {column.name}: {column.type}")
        
        print("\nGroupMember Model Details:")
        print(f"Table name: {GroupMember.__tablename__}")
        print("Columns:")
        for column in GroupMember.__table__.columns:
            print(f"- {column.name}: {column.type}")

# Call debug function
print_model_details()

# Error handling wrapper
def handle_db_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Database error in {func.__name__}: {str(e)}")
            print(traceback.format_exc())
            db.session.rollback()
            raise
    return wrapper

# Apply error handling to model methods
Group.to_dict = handle_db_error(Group.to_dict)
GroupMember.to_dict = handle_db_error(GroupMember.to_dict)

# Unit tests
import unittest

class TestGroupModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_group(self):
        group = Group(name="Test Group", description="A test group")
        db.session.add(group)
        db.session.commit()
        self.assertIsNotNone(group.id)
        self.assertEqual(group.name, "Test Group")

    def test_create_group_member(self):
        group = Group(name="Test Group")
        user = User(username="testuser", email="test@example.com")
        db.session.add(group)
        db.session.add(user)
        db.session.commit()

        member = GroupMember(group_id=group.id, user_id=user.id, role="admin")
        db.session.add(member)
        db.session.commit()

        self.assertIsNotNone(member.id)
        self.assertEqual(member.role, "admin")
        self.assertEqual(member.group, group)
        self.assertEqual(member.user, user)

if __name__ == '__main__':
    unittest.main()
