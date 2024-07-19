
# Purpose: Routes for group chat functionality
# Description: This file contains route handlers for creating groups, managing group members,
#              and sending messages to groups.

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Group, Message, User
from app import db
import traceback

groups = Blueprint('groups', __name__)

@groups.route('/create', methods=['POST'])
@login_required
def create_group():
    """Creates a new group"""
    if not request.json or 'name' not in request.json:
        return jsonify({'error': 'Group name is required'}), 400

    try:
        group_name = request.json['name']
        new_group = Group(name=group_name, created_by=current_user.id)
        new_group.members.append(current_user)
        db.session.add(new_group)
        db.session.commit()

        if current_app.config['DEBUG']:
            print(f"Group created: {new_group.name}")

        return jsonify({'message': 'Group created successfully', 'group_id': new_group.id}), 201
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'error': 'An error occurred while creating the group'}), 500

@groups.route('/<int:group_id>/add_member/<int:user_id>', methods=['POST'])
@login_required
def add_member(group_id, user_id):
    """Adds a member to a group"""
    try:
        group = Group.query.get(group_id)
        user = User.query.get(user_id)

        if not group or not user:
            return jsonify({'error': 'Group or user not found'}), 404

        if current_user.id != group.created_by:
            return jsonify({'error': 'Only group creator can add members'}), 403

        if user in group.members:
            return jsonify({'error': 'User is already a member of this group'}), 400

        group.members.append(user)
        db.session.commit()

        if current_app.config['DEBUG']:
            print(f"User {user.id} added to group {group.id}")

        return jsonify({'message': 'Member added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'error': 'An error occurred while adding the member'}), 500

@groups.route('/<int:group_id>/remove_member/<int:user_id>', methods=['DELETE'])
@login_required
def remove_member(group_id, user_id):
    """Removes a member from a group"""
    try:
        group = Group.query.get(group_id)
        user = User.query.get(user_id)

        if not group or not user:
            return jsonify({'error': 'Group or user not found'}), 404

        if current_user.id != group.created_by:
            return jsonify({'error': 'Only group creator can remove members'}), 403

        if user not in group.members:
            return jsonify({'error': 'User is not a member of this group'}), 400

        group.members.remove(user)
        db.session.commit()

        if current_app.config['DEBUG']:
            print(f"User {user.id} removed from group {group.id}")

        return jsonify({'message': 'Member removed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'error': 'An error occurred while removing the member'}), 500

@groups.route('/<int:group_id>/send_message', methods=['POST'])
@login_required
def send_group_message(group_id):
    """Sends a message to a group"""
    if not request.json or 'content' not in request.json:
        return jsonify({'error': 'Message content is required'}), 400

    try:
        group = Group.query.get(group_id)

        if not group:
            return jsonify({'error': 'Group not found'}), 404

        if current_user not in group.members:
            return jsonify({'error': 'You are not a member of this group'}), 403

        content = request.json['content']
        new_message = Message(content=content, sender_id=current_user.id, group_id=group_id)
        db.session.add(new_message)
        db.session.commit()

        if current_app.config['DEBUG']:
            print(f"Message sent to group {group.id}: {content[:20]}...")

        return jsonify({'message': 'Message sent successfully', 'message_id': new_message.id}), 201
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'error': 'An error occurred while sending the message'}), 500

# Add more group-related routes as needed

# Unit tests for the groups routes
import unittest
from app import create_app, db
from app.models import User, Group

class GroupRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_group(self):
        # Add test for create_group route
        pass

    def test_add_member(self):
        # Add test for add_member route
        pass

    def test_remove_member(self):
        # Add test for remove_member route
        pass

    def test_send_group_message(self):
        # Add test for send_group_message route
        pass

if __name__ == '__main__':
    unittest.main()
