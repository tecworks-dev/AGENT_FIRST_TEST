
"""
This file defines API endpoints for the communication platform.
It includes resources for handling user, message, group, and channel-related API requests.
"""

import traceback
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.models import User, Message, Group, Channel
from .schemas import UserSchema, MessageSchema, GroupSchema, ChannelSchema
from flask_login import login_required, current_user
from app.services import encryption

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

DEBUG = True

class UserAPI(Resource):
    @login_required
    def get(self, user_id=None):
        try:
            if user_id:
                user = User.query.get_or_404(user_id)
                return UserSchema().dump(user)
            else:
                users = User.query.all()
                return UserSchema(many=True).dump(users)
        except Exception as e:
            if DEBUG:
                print(f"Error in UserAPI.get: {str(e)}")
                traceback.print_exc()
            return {'error': 'An error occurred while fetching user data'}, 500

    @login_required
    def post(self):
        try:
            data = request.get_json()
            user = User(**data)
            user.set_password(data['password'])
            user.save()
            return UserSchema().dump(user), 201
        except Exception as e:
            if DEBUG:
                print(f"Error in UserAPI.post: {str(e)}")
                traceback.print_exc()
            return {'error': 'An error occurred while creating the user'}, 500

class MessageAPI(Resource):
    @login_required
    def get(self, message_id=None):
        try:
            if message_id:
                message = Message.query.get_or_404(message_id)
                return MessageSchema().dump(message)
            else:
                messages = Message.query.filter_by(recipient_id=current_user.id).all()
                return MessageSchema(many=True).dump(messages)
        except Exception as e:
            if DEBUG:
                print(f"Error in MessageAPI.get: {str(e)}")
                traceback.print_exc()
            return {'error': 'An error occurred while fetching messages'}, 500

    @login_required
    def post(self):
        try:
            data = request.get_json()
            encrypted_content = encryption.encrypt_message(data['content'], current_user.encryption_key)
            message = Message(sender_id=current_user.id, recipient_id=data['recipient_id'], content=encrypted_content)
            message.save()
            return MessageSchema().dump(message), 201
        except Exception as e:
            if DEBUG:
                print(f"Error in MessageAPI.post: {str(e)}")
                traceback.print_exc()
            return {'error': 'An error occurred while sending the message'}, 500

class GroupAPI(Resource):
    @login_required
    def get(self, group_id=None):
        try:
            if group_id:
                group = Group.query.get_or_404(group_id)
                return GroupSchema().dump(group)
            else:
                groups = Group.query.filter(Group.members.any(id=current_user.id)).all()
                return GroupSchema(many=True).dump(groups)
        except Exception as e:
            if DEBUG:
                print(f"Error in GroupAPI.get: {str(e)}")
                traceback.print_exc()
            return {'error': 'An error occurred while fetching group data'}, 500

    @login_required
    def post(self):
        try:
            data = request.get_json()
            group = Group(name=data['name'], creator_id=current_user.id)
            group.members.append(current_user)
            group.save()
            return GroupSchema().dump(group), 201
        except Exception as e:
            if DEBUG:
                print(f"Error in GroupAPI.post: {str(e)}")
                traceback.print_exc()
            return {'error': 'An error occurred while creating the group'}, 500

class ChannelAPI(Resource):
    @login_required
    def get(self, channel_id=None):
        try:
            if channel_id:
                channel = Channel.query.get_or_404(channel_id)
                return ChannelSchema().dump(channel)
            else:
                channels = Channel.query.filter(Channel.subscribers.any(id=current_user.id)).all()
                return ChannelSchema(many=True).dump(channels)
        except Exception as e:
            if DEBUG:
                print(f"Error in ChannelAPI.get: {str(e)}")
                traceback.print_exc()
            return {'error': 'An error occurred while fetching channel data'}, 500

    @login_required
    def post(self):
        try:
            data = request.get_json()
            channel = Channel(name=data['name'], creator_id=current_user.id)
            channel.subscribers.append(current_user)
            channel.save()
            return ChannelSchema().dump(channel), 201
        except Exception as e:
            if DEBUG:
                print(f"Error in ChannelAPI.post: {str(e)}")
                traceback.print_exc()
            return {'error': 'An error occurred while creating the channel'}, 500

# Register API resources
api.add_resource(UserAPI, '/users', '/users/<int:user_id>')
api.add_resource(MessageAPI, '/messages', '/messages/<int:message_id>')
api.add_resource(GroupAPI, '/groups', '/groups/<int:group_id>')
api.add_resource(ChannelAPI, '/channels', '/channels/<int:channel_id>')

if __name__ == '__main__':
    import unittest

    class TestAPI(unittest.TestCase):
        def setUp(self):
            self.app = create_app('testing')
            self.client = self.app.test_client()

        def test_user_api(self):
            # Add test cases for UserAPI
            pass

        def test_message_api(self):
            # Add test cases for MessageAPI
            pass

        def test_group_api(self):
            # Add test cases for GroupAPI
            pass

        def test_channel_api(self):
            # Add test cases for ChannelAPI
            pass

    unittest.main()
