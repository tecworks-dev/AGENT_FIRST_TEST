Create a file named '/secure_messaging_platform/backend/services/encryption.py' with the following description: 
                Handles message encryption and decryption.
                Imports: cryptography.fernet
                Functions:
                - generate_key(): No arguments, returns bytes (encryption key).
                - encrypt_message(message: str, key: bytes): Returns bytes (encrypted message).
                - decrypt_message(encrypted_message: bytes, key: bytes): Returns str (decrypted message).
            

For python files include famework such as unittest


Here's the overall application plan which you should follow while writing the file:
<application_plan>
    <overview>
        The Secure Messaging Platform is a comprehensive web-based application inspired by Telegram's professional version. It's built using Flask for the backend and React.js for the frontend. The platform offers secure messaging with end-to-end encryption, group chats, file sharing, voice and video calling, advanced search, sticker support, user management, and an admin panel.
    </overview>
    <mechanics>
        - User registration and authentication using JWT
        - End-to-end encrypted messaging
        - Real-time updates using WebSockets
        - File upload and sharing
        - Group chat creation and management
        - Voice and video calling integration
        - Advanced search functionality
        - Sticker and emoji support
        - Admin panel for user and content management
    </mechanics>
    <components>
        - Flask backend
        - React.js frontend
        - PostgreSQL database
        - Redis for caching and real-time features
        - Celery for background tasks
    </components>
    <files>
        <file>
            <name>/secure_messaging_platform/main.py</name>
            <description>
                Entry point of the application. Initializes and runs the Flask app.
                Imports: from flask import Flask, from backend import create_app
                Functions:
                - main(): No arguments, returns None. Runs the Flask application.
            </description>
        </file>
        <file>
            <name>/secure_messaging_platform/backend/__init__.py</name>
            <description>
                Initializes the Flask application and registers blueprints.
                Imports: flask, .config, .extensions, .api
                Functions:
                - create_app(config_class=Config): Takes optional config_class, returns Flask app instance.
            </description>
        </file>
        <file>
            <name>/secure_messaging_platform/backend/config.py</name>
            <description>
                Defines configuration settings for the application.
                Imports: os
                Classes:
                - Config: Stores configuration variables as class attributes.
            </description>
        </file>
        <file>
            <name>/secure_messaging_platform/backend/extensions.py</name>
            <description>
                Initializes Flask extensions.
                Imports: flask_sqlalchemy, flask_migrate, flask_jwt_extended, flask_bcrypt, flask_redis, flask_celery
            </description>
        </file>
        <file>
            <name>/secure_messaging_platform/backend/api/auth.py</name>
            <description>
                Handles user authentication and authorization.
                Imports: flask, flask_jwt_extended, ..models.user, ..extensions
                Functions:
                - register(): POST, no arguments, returns JSON response.
                - login(): POST, no arguments, returns JSON response with access token.
                - logout(): POST, jwt_required, no arguments, returns JSON response.
            </description>
        </file>
        <file>
            <name>/secure_messaging_platform/backend/api/messages.py</name>
            <description>
                Handles message-related operations.
                Imports: flask, flask_jwt_extended, ..models.message, ..models.user, ..extensions, ..services.encryption
                Functions:
                - send_message(): POST, jwt_required, no arguments, returns JSON response.
                - receive_messages(): GET, jwt_required, no arguments, returns JSON response with messages.
            </description>
        </file>
        <file>
            <name>/secure_messaging_platform/backend/models/user.py</name>
            <description>
                Defines the User model.
                Imports: ..extensions
                Classes:
                - User: SQLAlchemy model with methods:
                  - set_password(password: str): Takes password string, returns None.
                  - check_password(password: str): Takes password string, returns bool.
            </description>
        </file>
        <file>
            <name>/secure_messaging_platform/backend/services/encryption.py</name>
            <description>
                Handles message encryption and decryption.
                Imports: cryptography.fernet
                Functions:
                - generate_key(): No arguments, returns bytes (encryption key).
                - encrypt_message(message: str, key: bytes): Returns bytes (encrypted message).
                - decrypt_message(encrypted_message: bytes, key: bytes): Returns str (decrypted message).
            </description>
        </file>
    </files>
    <logic>
        1. User registers or logs in through /api/auth endpoints
        2. Upon successful authentication, user receives a JWT
        3. User can then:
           - Send messages (encrypted) through /api/messages/send
           - Receive messages (decrypted) through /api/messages/receive
           - Create or join group chats
           - Upload and share files
           - Initiate voice or video calls
           - Search for messages or files
           - Use stickers and emojis in messages
        4. Admins can access additional endpoints for user and content management
        5. Background tasks (e.g., message delivery confirmation) are handled by Celery
        6. Redis is used for caching and managing real-time features
    </logic>
</application_plan>

Remember, the application should start with a main module in the main.py file(main shouldn't take any arguments). Always return the full contents of the file
    