
# Purpose: Define serialization schemas for API responses
# Description: This file contains Marshmallow schemas for serializing User, Message, Group, and Channel models

from marshmallow import Schema, fields
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug flag
DEBUG = True

class UserSchema(Schema):
    """Schema for User model serialization"""
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)
    last_seen = fields.DateTime(dump_only=True)
    is_active = fields.Boolean(dump_only=True)

    if DEBUG:
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            logger.debug(f"UserSchema initialized with args: {args}, kwargs: {kwargs}")

class MessageSchema(Schema):
    """Schema for Message model serialization"""
    id = fields.Int(dump_only=True)
    sender_id = fields.Int(required=True)
    recipient_id = fields.Int(required=True)
    content = fields.Str(required=True)
    timestamp = fields.DateTime(dump_only=True)
    is_read = fields.Boolean(dump_only=True)

    if DEBUG:
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            logger.debug(f"MessageSchema initialized with args: {args}, kwargs: {kwargs}")

class GroupSchema(Schema):
    """Schema for Group model serialization"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    creator_id = fields.Int(required=True)
    members = fields.List(fields.Nested(UserSchema), dump_only=True)

    if DEBUG:
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            logger.debug(f"GroupSchema initialized with args: {args}, kwargs: {kwargs}")

class ChannelSchema(Schema):
    """Schema for Channel model serialization"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    creator_id = fields.Int(required=True)
    subscribers = fields.List(fields.Nested(UserSchema), dump_only=True)

    if DEBUG:
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            logger.debug(f"ChannelSchema initialized with args: {args}, kwargs: {kwargs}")

# Error handling decorator
def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    return wrapper

# Apply error handling to all schema methods
for schema in [UserSchema, MessageSchema, GroupSchema, ChannelSchema]:
    for method_name in ['dump', 'load', 'validate']:
        if hasattr(schema, method_name):
            setattr(schema, method_name, error_handler(getattr(schema, method_name)))

if __name__ == "__main__":
    # Add some basic unit tests
    import unittest

    class TestSchemas(unittest.TestCase):
        def test_user_schema(self):
            schema = UserSchema()
            user_data = {
                "username": "testuser",
                "email": "test@example.com",
            }
            result = schema.load(user_data)
            self.assertEqual(result["username"], "testuser")
            self.assertEqual(result["email"], "test@example.com")

        def test_message_schema(self):
            schema = MessageSchema()
            message_data = {
                "sender_id": 1,
                "recipient_id": 2,
                "content": "Hello, world!",
            }
            result = schema.load(message_data)
            self.assertEqual(result["sender_id"], 1)
            self.assertEqual(result["recipient_id"], 2)
            self.assertEqual(result["content"], "Hello, world!")

        def test_group_schema(self):
            schema = GroupSchema()
            group_data = {
                "name": "Test Group",
                "description": "A test group",
                "creator_id": 1,
            }
            result = schema.load(group_data)
            self.assertEqual(result["name"], "Test Group")
            self.assertEqual(result["description"], "A test group")
            self.assertEqual(result["creator_id"], 1)

        def test_channel_schema(self):
            schema = ChannelSchema()
            channel_data = {
                "name": "Test Channel",
                "description": "A test channel",
                "creator_id": 1,
            }
            result = schema.load(channel_data)
            self.assertEqual(result["name"], "Test Channel")
            self.assertEqual(result["description"], "A test channel")
            self.assertEqual(result["creator_id"], 1)

    unittest.main()
