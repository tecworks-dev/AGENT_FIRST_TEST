Create a file named 'frontend/src/utils/api.js' with the following description: 
                API utility functions.
                Imports: axios
                Functions:
                - get(url: string, params: object): Makes a GET request
                - post(url: string, data: object): Makes a POST request
                - put(url: string, data: object): Makes a PUT request
                - delete(url: string): Makes a DELETE request
            

For python files include famework such as unittest


Here's the overall application plan which you should follow while writing the file:
<application_plan>
    <overview>
        A secure messaging platform using Flask and React.js, inspired by Telegram's professional version. The application features end-to-end encryption, user authentication, real-time communication, file sharing, and admin capabilities.
    </overview>
    <mechanics>
        - End-to-end encryption for messages
        - RESTful API for backend operations
        - WebSocket for real-time communication
        - User authentication and authorization
        - File upload and storage
        - Group chat functionality
        - Voice and video calling
        - Admin panel for user management
    </mechanics>
    <components>
        - Flask Backend
        - React.js Frontend
        - SQLAlchemy Database
        - WebSocket Server
        - Encryption Module
        - Authentication Module
        - File Storage System
        - Admin Panel
        - API Documentation (Swagger/OpenAPI)
    </components>
    <files>
        <file>
            <name>backend/main.py</name>
            <description>
                Entry point for the Flask application. Initializes the app, database, and WebSocket.
                Imports: flask, flask_socketio, config, routes, models, socket_events
                Functions:
                - create_app(): Creates and configures the Flask app
                - main(): Runs the application
            </description>
        </file>
        <file>
            <name>backend/config.py</name>
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
            <name>backend/routes/__init__.py</name>
            <description>
                Initializes routes package and combines all route blueprints.
                Imports: flask, .auth, .messages, .groups, .files, .admin
                Functions:
                - init_app(app): Registers all blueprints with the app
            </description>
        </file>
        <file>
            <name>backend/routes/auth.py</name>
            <description>
                Authentication routes (login, register, logout).
                Imports: flask, flask_jwt_extended, models, utils
                Functions:
                - register(): Handles user registration
                - login(): Handles user login
                - logout(): Handles user logout
                - refresh_token(): Refreshes JWT token
            </description>
        </file>
        <file>
            <name>backend/routes/messages.py</name>
            <description>
                Message-related routes (send, receive, edit, delete).
                Imports: flask, flask_jwt_extended, models, utils
                Functions:
                - send_message(recipient_id: int, content: str): Sends a message
                - get_messages(user_id: int): Retrieves messages for a user
                - edit_message(message_id: int, new_content: str): Edits a message
                - delete_message(message_id: int): Deletes a message
            </description>
        </file>
        <file>
            <name>backend/routes/groups.py</name>
            <description>
                Group-related routes (create, manage, invite).
                Imports: flask, flask_jwt_extended, models, utils
                Functions:
                - create_group(name: str, members: List[int]): Creates a new group
                - add_member(group_id: int, user_id: int): Adds a member to a group
                - remove_member(group_id: int, user_id: int): Removes a member from a group
                - get_group_messages(group_id: int): Retrieves messages for a group
            </description>
        </file>
        <file>
            <name>backend/routes/files.py</name>
            <description>
                File upload and management routes.
                Imports: flask, flask_jwt_extended, werkzeug.utils, models, utils
                Functions:
                - upload_file(): Handles file uploads
                - get_file(file_id: int): Retrieves a file
                - delete_file(file_id: int): Deletes a file
            </description>
        </file>
        <file>
            <name>backend/routes/admin.py</name>
            <description>
                Admin panel routes.
                Imports: flask, flask_jwt_extended, models, utils
                Functions:
                - get_all_users(): Retrieves all users
                - ban_user(user_id: int): Bans a user
                - unban_user(user_id: int): Unbans a user
                - get_system_stats(): Retrieves system statistics
            </description>
        </file>
        <file>
            <name>backend/models/__init__.py</name>
            <description>
                Initializes models package.
                Imports: .user, .message, .group
            </description>
        </file>
        <file>
            <name>backend/models/user.py</name>
            <description>
                User model.
                Imports: flask_sqlalchemy, database
                Classes:
                - User: Represents a user in the system
            </description>
        </file>
        <file>
            <name>backend/models/message.py</name>
            <description>
                Message model.
                Imports: flask_sqlalchemy, database
                Classes:
                - Message: Represents a message in the system
            </description>
        </file>
        <file>
            <name>backend/models/group.py</name>
            <description>
                Group model.
                Imports: flask_sqlalchemy, database
                Classes:
                - Group: Represents a group in the system
                - GroupMember: Represents a group membership
            </description>
        </file>
        <file>
            <name>backend/utils/__init__.py</name>
            <description>
                Initializes utils package.
                Imports: .encryption, .auth, .websocket
            </description>
        </file>
        <file>
            <name>backend/utils/encryption.py</name>
            <description>
                End-to-end encryption utilities.
                Imports: cryptography
                Functions:
                - encrypt_message(message: str, key: bytes) -> bytes: Encrypts a message
                - decrypt_message(encrypted: bytes, key: bytes) -> str: Decrypts a message
                - generate_key() -> bytes: Generates an encryption key
            </description>
        </file>
        <file>
            <name>backend/utils/auth.py</name>
            <description>
                Authentication utilities (JWT, 2FA).
                Imports: flask_jwt_extended, pyotp
                Functions:
                - generate_2fa_secret() -> str: Generates a 2FA secret
                - verify_2fa(secret: str, token: str) -> bool: Verifies a 2FA token
            </description>
        </file>
        <file>
            <name>backend/utils/websocket.py</name>
            <description>
                WebSocket utilities.
                Imports: flask_socketio
                Functions:
                - emit_message(user_id: int, message: dict): Emits a message to a user
                - emit_group_message(group_id: int, message: dict): Emits a message to a group
            </description>
        </file>
        <file>
            <name>backend/database.py</name>
            <description>
                Database configuration and connection.
                Imports: flask_sqlalchemy
                Variables:
                - db: SQLAlchemy instance
                Functions:
                - init_db(app): Initializes the database with the app
            </description>
        </file>
        <file>
            <name>backend/socket_events.py</name>
            <description>
                WebSocket event handlers.
                Imports: flask_socketio, models, utils
                Functions:
                - on_connect(): Handles client connection
                - on_disconnect(): Handles client disconnection
                - on_join_room(data): Handles joining a chat room
                - on_leave_room(data): Handles leaving a chat room
                - on_new_message(data): Handles new message events
            </description>
        </file>
        <file>
            <name>backend/api_docs.py</name>
            <description>
                OpenAPI/Swagger documentation generator.
                Imports: flask_restx
                Functions:
                - setup_api_docs(app): Sets up API documentation for the app
            </description>
        </file>
        <file>
            <name>frontend/src/index.js</name>
            <description>
                Entry point for React application.
                Imports: react, react-dom, App
            </description>
        </file>
        <file>
            <name>frontend/src/App.js</name>
            <description>
                Main React component.
                Imports: react, react-router-dom, components
                Components:
                - App: Main application component
            </description>
        </file>
        <file>
            <name>frontend/src/components/Auth/Login.js</name>
            <description>
                Login component.
                Imports: react, axios
                Components:
                - Login: Handles user login
            </description>
        </file>
        <file>
            <name>frontend/src/components/Auth/Register.js</name>
            <description>
                Registration component.
                Imports: react, axios
                Components:
                - Register: Handles user registration
            </description>
        </file>
        <file>
            <name>frontend/src/components/Chat/ChatInterface.js</name>
            <description>
                Main chat interface component.
                Imports: react, components (MessageList, ContactList)
                Components:
                - ChatInterface: Main chat UI
            </description>
        </file>
        <file>
            <name>frontend/src/components/Chat/MessageList.js</name>
            <description>
                Message list component.
                Imports: react, components (Message)
                Components:
                - MessageList: Displays a list of messages
            </description>
        </file>
        <file>
            <name>frontend/src/components/Chat/Message.js</name>
            <description>
                Individual message component.
                Imports: react
                Components:
                - Message: Displays a single message
            </description>
        </file>
        <file>
            <name>frontend/src/components/Chat/ContactList.js</name>
            <description>
                Contact list component.
                Imports: react
                Components:
                - ContactList: Displays a list of contacts
            </description>
        </file>
        <file>
            <name>frontend/src/components/Group/GroupChat.js</name>
            <description>
                Group chat component.
                Imports: react, components (MessageList)
                Components:
                - GroupChat: Handles group chat functionality
            </description>
        </file>
        <file>
            <name>frontend/src/components/Group/GroupManagement.js</name>
            <description>
                Group management component.
                Imports: react, axios
                Components:
                - GroupManagement: Manages group settings and members
            </description>
        </file>
        <file>
            <name>frontend/src/components/File/FileUpload.js</name>
            <description>
                File upload component.
                Imports: react, axios
                Components:
                - FileUpload: Handles file uploads
            </description>
        </file>
        <file>
            <name>frontend/src/components/Call/VoiceCall.js</name>
            <description>
                Voice call component.
                Imports: react, webrtc-adapter
                Components:
                - VoiceCall: Handles voice calls
            </description>
        </file>
        <file>
            <name>frontend/src/components/Call/VideoCall.js</name>
            <description>
                Video call component.
                Imports: react, webrtc-adapter
                Components:
                - VideoCall: Handles video calls
            </description>
        </file>
        <file>
            <name>frontend/src/components/Search/Search.js</name>
            <description>
                Advanced search component.
                Imports: react, axios
                Components:
                - Search: Provides advanced search functionality
            </description>
        </file>
        <file>
            <name>frontend/src/components/Profile/UserProfile.js</name>
            <description>
                User profile management component.
                Imports: react, axios
                Components:
                - UserProfile: Manages user profile settings
            </description>
        </file>
        <file>
            <name>frontend/src/utils/api.js</name>
            <description>
                API utility functions.
                Imports: axios
                Functions:
                - get(url: string, params: object): Makes a GET request
                - post(url: string, data: object): Makes a POST request
                - put(url: string, data: object): Makes a PUT request
                - delete(url: string): Makes a DELETE request
            </description>
        </file>
        <file>
            <name>frontend/src/utils/socket.js</name>
            <description>
                WebSocket utility functions.
                Imports: socket.io-client
                Functions:
                - connectSocket(): Connects to the WebSocket server
                - disconnectSocket(): Disconnects from the WebSocket server
                - onNewMessage(callback: function): Listens for new messages
            </description>
        </file>
        <file>
            <name>frontend/src/utils/encryption.js</name>
            <description>
                Client-side encryption utilities.
                Imports: crypto-js
                Functions:
                - encryptMessage(message: string, key: string): Encrypts a message
                - decryptMessage(encryptedMessage: string, key: string): Decrypts a message
            </description>
        </file>
    </files>
    <logic>
        1. User registers or logs in through the frontend
        2. Backend authenticates user and provides JWT token
        3. Frontend stores token and uses it for subsequent API calls
        4. User can:
           - Send/receive messages (encrypted end-to-end)
           - Create/join group chats
           - Upload/download files
           - Initiate voice/video calls
           - Search messages and contacts
           - Manage profile settings
        5. Real-time updates are handled via WebSocket connection
        6. Admin can manage users and view system stats through admin panel
        7. All API endpoints are documented using Swagger/OpenAPI
    </logic>
</application_plan>

Remember, the application should start with a main module in the main.py file(main shouldn't take any arguments). Always return the full contents of the file
    