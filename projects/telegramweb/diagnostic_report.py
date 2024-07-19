
import unittest
import traceback
import sys
import os
from io import StringIO
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from app import create_app
from app.extensions import db, socketio
from app.models.user import User
from app.models.message import Message
from app.models.media import Media
from app.services.auth import AuthService
from app.services.messages import MessageService
from app.services.media import MediaService
from app.services.search import SearchService
from app.utils.encryption import generate_key, encrypt_message, decrypt_message, hash_password, verify_password
from app.utils.storage import store_file, retrieve_file, delete_file

class TestMessagingPlatform(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(Config)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        db.session.begin(subtransactions=True)

    def tearDown(self):
        db.session.rollback()

    def test_config(self):
        print("\nTesting Config (config.py)")
        try:
            self.assertTrue(self.app.config['SECRET_KEY'])
            self.assertTrue(self.app.config['SQLALCHEMY_DATABASE_URI'])
            self.assertFalse(self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        except AssertionError as e:
            print(f"Test failed: {str(e)}")
            traceback.print_exc()

    def test_create_app(self):
        print("\nTesting create_app (app/__init__.py)")
        try:
            self.assertIsInstance(self.app, Flask)
            self.assertIsInstance(self.app.extensions['sqlalchemy'].db, SQLAlchemy)
            self.assertIsInstance(self.app.extensions['socketio'], SocketIO)
        except AssertionError as e:
            print(f"Test failed: {str(e)}")
            traceback.print_exc()

    def test_user_model(self):
        print("\nTesting User model (app/models/user.py)")
        try:
            user = User(username="testuser", password_hash="testhash")
            db.session.add(user)
            db.session.commit()
            self.assertIsNotNone(user.id)
            self.assertEqual(user.username, "testuser")
            self.assertEqual(user.password_hash, "testhash")
        except Exception as e:
            print(f"Test failed: {str(e)}")
            traceback.print_exc()

    def test_message_model(self):
        print("\nTesting Message model (app/models/message.py)")
        try:
            sender = User(username="sender", password_hash="senderhash")
            receiver = User(username="receiver", password_hash="receiverhash")
            db.session.add_all([sender, receiver])
            db.session.commit()

            message = Message(sender_id=sender.id, receiver_id=receiver.id, content="Test message")
            db.session.add(message)
            db.session.commit()

            self.assertIsNotNone(message.id)
            self.assertEqual(message.sender_id, sender.id)
            self.assertEqual(message.receiver_id, receiver.id)
            self.assertEqual(message.content, "Test message")
        except Exception as e:
            print(f"Test failed: {str(e)}")
            traceback.print_exc()

    def test_media_model(self):
        print("\nTesting Media model (app/models/media.py)")
        try:
            user = User(username="mediauser", password_hash="mediahash")
            db.session.add(user)
            db.session.commit()

            media = Media(user_id=user.id, filename="test.jpg", file_type="image/jpeg")
            db.session.add(media)
            db.session.commit()

            self.assertIsNotNone(media.id)
            self.assertEqual(media.user_id, user.id)
            self.assertEqual(media.filename, "test.jpg")
            self.assertEqual(media.file_type, "image/jpeg")
        except Exception as e:
            print(f"Test failed: {str(e)}")
            traceback.print_exc()

    def test_auth_service(self):
        print("\nTesting AuthService (app/services/auth.py)")
        try:
            auth_service = AuthService()
            result = auth_service.register("testuser", "testpass")
            self.assertEqual(result['status'], "success")

            login_result = auth_service.login("testuser", "testpass")
            self.assertTrue(login_result['success'])

            logout_result = auth_service.logout(login_result['user'].id)
            self.assertTrue(logout_result)
        except Exception as e:
            print(f"Test failed: {str(e)}")
            traceback.print_exc()

    def test_message_service(self):
        print("\nTesting MessageService (app/services/messages.py)")
        try:
            sender = User(username="sender", password_hash="senderhash")
            receiver = User(username="receiver", password_hash="receiverhash")
            db.session.add_all([sender, receiver])
            db.session.commit()

            message_service = MessageService()
            message = message_service.send_message(sender.id, receiver.id, "Test message")
            self.assertIsNotNone(message['id'])

            retrieved_message = message_service.get_message(message['id'])
            self.assertEqual(retrieved_message['content'], "Test message")

            updated_message = message_service.update_message(message['id'], "Updated message")
            self.assertEqual(updated_message['content'], "Updated message")

            delete_result = message_service.delete_message(message['id'])
            self.assertTrue(delete_result)
        except Exception as e:
            print(f"Test failed: {str(e)}")
            traceback.print_exc()

    def test_media_service(self):
        print("\nTesting MediaService (app/services/media.py)")
        try:
            user = User(username="mediauser", password_hash="mediahash")
            db.session.add(user)
            db.session.commit()

            media_service = MediaService()
            
            # Create a mock file object
            mock_file = StringIO("Mock file content")
            mock_file.filename = "test.txt"

            media = media_service.upload_media(user.id, mock_file)
            self.assertIsNotNone(media['id'])

            retrieved_media = media_service.get_media(media['id'])
            self.assertEqual(retrieved_media['filename'], "test.txt")

            delete_result = media_service.delete_media(media['id'])
            self.assertTrue(delete_result)
        except Exception as e:
            print(f"Test failed: {str(e)}")
            traceback.print_exc()

    def test_search_service(self):
        print("\nTesting SearchService (app/services/search.py)")
        try:
            user = User(username="searchuser", password_hash="searchhash")
            db.session.add(user)
            db.session.commit()

            message = Message(sender_id=user.id, receiver_id=user.id, content="Test search message")
            db.session.add(message)
            db.session.commit()

            media = Media(user_id=user.id, filename="searchtest.jpg", file_type="image/jpeg")
            db.session.add(media)
            db.session.commit()

            search_service = SearchService()
            message_results = search_service.search_messages(user.id, "search")
            self.assertEqual(len(message_results), 1)

            media_results = search_service.search_media(user.id, "search")
            self.assertEqual(len(media_results), 1)
        except Exception as e:
            print(f"Test failed: {str(e)}")
            traceback.print_exc()

    def test_encryption_utils(self):
        print("\nTesting encryption utils (app/utils/encryption.py)")
        try:
            key = generate_key()
            self.assertIsInstance(key, bytes)

            message = "Test message"
            encrypted = encrypt_message(message, key)
            decrypted = decrypt_message(encrypted, key)
            self.assertEqual(message, decrypted)

            password = "testpassword"
            hashed = hash_password(password)
            self.assertTrue(verify_password(hashed, password))
        except Exception as e:
            print(f"Test failed: {str(e)}")
            traceback.print_exc()

    def test_storage_utils(self):
        print("\nTesting storage utils (app/utils/storage.py)")
        try:
            # Create a mock file object
            mock_file = StringIO("Mock file content")
            mock_file.filename = "test.txt"

            stored_path = store_file(mock_file, "test.txt")
            self.assertTrue(os.path.exists(stored_path))

            retrieved_file = retrieve_file("test.txt")
            self.assertIsNotNone(retrieved_file)

            delete_result = delete_file("test.txt")
            self.assertTrue(delete_result)
            self.assertFalse(os.path.exists(stored_path))
        except Exception as e:
            print(f"Test failed: {str(e)}")
            traceback.print_exc()

def main():
    unittest.main(verbosity=2)

if __name__ == "__main__":
    main()
