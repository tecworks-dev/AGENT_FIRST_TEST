Create a file named '/project_root/app/services/websocket.py' with the following description: 
                Manages WebSocket connections for real-time communication.
                Imports: from flask_socketio import SocketIO, emit, join_room, leave_room
                Functions:
                - handle_connect(): Handles new WebSocket connections
                - handle_disconnect(): Handles WebSocket disconnections
                - handle_join_room(room): Handles joining a room
                - handle_leave_room(room): Handles leaving a room
                - handle_message(data): Handles incoming messages
            

For python files include famework such as unittest


Here's the overall application plan which you should follow while writing the file:
<application_plan>
    <overview>
        A sophisticated web-based communication platform inspired by Telegram, offering secure messaging, group chats, file sharing, voice/video calls, and a robust API. Built with Flask, it prioritizes security, scalability, and user experience.
    </overview>
    
    <mechanics>
        - End-to-end encrypted messaging
        - Group and channel management
        - File sharing and media transfer
        - Voice and video calling
        - User status updates
        - Admin panel for platform management
        - RESTful API for third-party integrations
        - WebSocket for real-time communications
    </mechanics>
    
    <components>
        - Flask web application
        - SQLAlchemy ORM
        - Flask-SocketIO for WebSocket support
        - Encryption service
        - File handling service
        - Push notification service
        - RESTful API
        - Admin panel
        - User authentication system
    </components>
    
    <files>
        <file>
            <name>/project_root/main.py</name>
            <description>
                Entry point of the application. Initializes and runs the Flask app.
                Imports: from app import create_app
                Functions:
                - main(): No parameters, initializes and runs the Flask application
            </description>
        </file>
        <file>
            <name>/project_root/config.py</name>
            <description>
                Configuration settings for the application.
                Imports: os
                Classes:
                - Config: Holds configuration variables
                - DevelopmentConfig(Config): Development-specific settings
                - ProductionConfig(Config): Production-specific settings
            </description>
        </file>
        <file>
            <name>/project_root/app/__init__.py</name>
            <description>
                Initializes the Flask application and its extensions.
                Imports: flask, flask_sqlalchemy, flask_migrate, flask_login, flask_socketio
                Functions:
                - create_app(config_class=Config): Returns initialized Flask app
            </description>
        </file>
        <file>
            <name>/project_root/app/models/user.py</name>
            <description>
                User model definition.
                Imports: from app import db, login_manager; from flask_login import UserMixin; from werkzeug.security import generate_password_hash, check_password_hash
                Classes:
                - User(db.Model, UserMixin): User model with authentication methods
            </description>
        </file>
        <file>
            <name>/project_root/app/models/message.py</name>
            <description>
                Message model definition.
                Imports: from app import db; from datetime import datetime
                Classes:
                - Message(db.Model): Message model for storing chat messages
            </description>
        </file>
        <file>
            <name>/project_root/app/models/group.py</name>
            <description>
                Group model definition.
                Imports: from app import db
                Classes:
                - Group(db.Model): Group model for managing group chats
            </description>
        </file>
        <file>
            <name>/project_root/app/models/channel.py</name>
            <description>
                Channel model definition.
                Imports: from app import db
                Classes:
                - Channel(db.Model): Channel model for broadcast communications
            </description>
        </file>
        <file>
            <name>/project_root/app/models/file.py</name>
            <description>
                File model definition for shared files.
                Imports: from app import db; from datetime import datetime
                Classes:
                - File(db.Model): File model for managing shared files
            </description>
        </file>
        <file>
            <name>/project_root/app/routes/auth.py</name>
            <description>
                Authentication routes (login, register, logout).
                Imports: from flask import Blueprint, request, jsonify; from flask_login import login_user, logout_user, login_required; from app.models import User; from app.utils import validators
                Functions:
                - login(): Handles user login
                - register(): Handles user registration
                - logout(): Handles user logout
            </description>
        </file>
        <file>
            <name>/project_root/app/routes/messaging.py</name>
            <description>
                Routes for one-on-one messaging.
                Imports: from flask import Blueprint, request, jsonify; from flask_login import login_required, current_user; from app.models import Message, User; from app.services import encryption
                Functions:
                - send_message(recipient_id): Sends a message to a user
                - get_messages(user_id): Retrieves messages for a conversation
            </description>
        </file>
        <file>
            <name>/project_root/app/routes/groups.py</name>
            <description>
                Routes for group chat functionality.
                Imports: from flask import Blueprint, request, jsonify; from flask_login import login_required, current_user; from app.models import Group, Message
                Functions:
                - create_group(): Creates a new group
                - add_member(group_id, user_id): Adds a member to a group
                - remove_member(group_id, user_id): Removes a member from a group
                - send_group_message(group_id): Sends a message to a group
            </description>
        </file>
        <file>
            <name>/project_root/app/routes/channels.py</name>
            <description>
                Routes for broadcast channels.
                Imports: from flask import Blueprint, request, jsonify; from flask_login import login_required, current_user; from app.models import Channel, Message
                Functions:
                - create_channel(): Creates a new channel
                - post_to_channel(channel_id): Posts a message to a channel
                - subscribe_to_channel(channel_id): Subscribes a user to a channel
            </description>
        </file>
        <file>
            <name>/project_root/app/routes/calls.py</name>
            <description>
                Routes for voice and video calling features.
                Imports: from flask import Blueprint, request, jsonify; from flask_login import login_required, current_user; from app.services import websocket
                Functions:
                - initiate_call(user_id): Initiates a call with another user
                - end_call(call_id): Ends an ongoing call
            </description>
        </file>
        <file>
            <name>/project_root/app/routes/admin.py</name>
            <description>
                Admin panel routes.
                Imports: from flask import Blueprint, request, jsonify; from flask_login import login_required; from app.models import User, Group, Channel
                Functions:
                - get_users(): Retrieves all users
                - ban_user(user_id): Bans a user
                - delete_group(group_id): Deletes a group
                - delete_channel(channel_id): Deletes a channel
            </description>
        </file>
        <file>
            <name>/project_root/app/services/encryption.py</name>
            <description>
                Handles end-to-end encryption for messages.
                Imports: from cryptography.fernet import Fernet
                Functions:
                - generate_key(): Generates a new encryption key
                - encrypt_message(message, key): Encrypts a message
                - decrypt_message(encrypted_message, key): Decrypts a message
            </description>
        </file>
        <file>
            <name>/project_root/app/services/file_handler.py</name>
            <description>
                Manages file uploads and downloads.
                Imports: from flask import current_app; from werkzeug.utils import secure_filename; import os
                Functions:
                - save_file(file): Saves an uploaded file
                - get_file(filename): Retrieves a file for download
            </description>
        </file>
        <file>
            <name>/project_root/app/services/push_notifications.py</name>
            <description>
                Handles push notifications for real-time updates.
                Imports: import firebase_admin; from firebase_admin import messaging
                Functions:
                - send_notification(token, title, body): Sends a push notification
            </description>
        </file>
        <file>
            <name>/project_root/app/services/websocket.py</name>
            <description>
                Manages WebSocket connections for real-time communication.
                Imports: from flask_socketio import SocketIO, emit, join_room, leave_room
                Functions:
                - handle_connect(): Handles new WebSocket connections
                - handle_disconnect(): Handles WebSocket disconnections
                - handle_join_room(room): Handles joining a room
                - handle_leave_room(room): Handles leaving a room
                - handle_message(data): Handles incoming messages
            </description>
        </file>
        <file>
            <name>/project_root/app/utils/validators.py</name>
            <description>
                Input validation functions.
                Imports: import re
                Functions:
                - validate_email(email): Validates email format
                - validate_password(password): Validates password strength
                - validate_username(username): Validates username format
            </description>
        </file>
        <file>
            <name>/project_root/app/utils/helpers.py</name>
            <description>
                Helper functions used across the application.
                Imports: None
                Functions:
                - generate_unique_id(): Generates a unique identifier
                - format_timestamp(timestamp): Formats a timestamp for display
            </description>
        </file>
        <file>
            <name>/project_root/app/api/v1/routes.py</name>
            <description>
                Defines API endpoints.
                Imports: from flask import Blueprint, request, jsonify; from flask_restful import Api, Resource; from app.models import User, Message, Group, Channel; from .schemas import UserSchema, MessageSchema
                Classes:
                - UserAPI(Resource): Handles user-related API endpoints
                - MessageAPI(Resource): Handles message-related API endpoints
                - GroupAPI(Resource): Handles group-related API endpoints
                - ChannelAPI(Resource): Handles channel-related API endpoints
            </description>
        </file>
        <file>
            <name>/project_root/app/api/v1/schemas.py</name>
            <description>
                Defines serialization schemas for API responses.
                Imports: from marshmallow import Schema, fields
                Classes:
                - UserSchema(Schema): Schema for User model serialization
                - MessageSchema(Schema): Schema for Message model serialization
                - GroupSchema(Schema): Schema for Group model serialization
                - ChannelSchema(Schema): Schema for Channel model serialization
            </description>
        </file>
    </files>
    
    <logic>
        1. User registration and authentication
        2. Secure message sending and receiving
        3. Group and channel creation and management
        4. File upload, storage, and sharing
        5. Real-time updates via WebSockets
        6. Push notifications for offline users
        7. Voice and video call initiation and management
        8. Admin operations for platform management
        9. API endpoints for third-party integrations
        10. End-to-end encryption for all communications
    </logic>
</application_plan>

Remember, the application should start with a main module in the main.py file(main shouldn't take any arguments). Always return the full contents of the file
    