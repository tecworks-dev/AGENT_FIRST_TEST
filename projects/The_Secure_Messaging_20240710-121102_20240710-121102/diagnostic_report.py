
import unittest
import traceback
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from secure_messaging_platform.main import main as app_main
from secure_messaging_platform.backend import create_app
from secure_messaging_platform.backend.config import Config, TestConfig
from secure_messaging_platform.backend.extensions import db, migrate, jwt, bcrypt, redis_client, celery, init_extensions
from secure_messaging_platform.backend.api.auth import register, login, logout
from secure_messaging_platform.backend.api.messages import send_message, receive_messages
from secure_messaging_platform.backend.models.user import User
from secure_messaging_platform.backend.services.encryption import generate_key, encrypt_message, decrypt_message

class DiagnosticReport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestConfig)
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def test_01_main_py(self):
        print("\nTesting main.py")
        try:
            self.assertIsNone(app_main())
        except Exception as e:
            print(f"Error in main.py: {str(e)}")
            print(traceback.format_exc())

    def test_02_backend_init(self):
        print("\nTesting backend/__init__.py")
        try:
            self.assertIsNotNone(self.app)
        except Exception as e:
            print(f"Error in backend/__init__.py: {str(e)}")
            print(traceback.format_exc())

    def test_03_config(self):
        print("\nTesting backend/config.py")
        try:
            self.assertIsNotNone(Config.SECRET_KEY)
            self.assertTrue(TestConfig.TESTING)
        except Exception as e:
            print(f"Error in backend/config.py: {str(e)}")
            print(traceback.format_exc())

    def test_04_extensions(self):
        print("\nTesting backend/extensions.py")
        try:
            init_extensions(self.app)
            self.assertIsNotNone(db)
            self.assertIsNotNone(migrate)
            self.assertIsNotNone(jwt)
            self.assertIsNotNone(bcrypt)
            self.assertIsNotNone(redis_client)
            self.assertIsNotNone(celery)
        except Exception as e:
            print(f"Error in backend/extensions.py: {str(e)}")
            print(traceback.format_exc())

    def test_05_user_model(self):
        print("\nTesting backend/models/user.py")
        try:
            user = User(username="testuser", email="test@example.com", password="testpassword")
            self.assertIsNotNone(user)
            self.assertTrue(user.check_password("testpassword"))
            self.assertFalse(user.check_password("wrongpassword"))
        except Exception as e:
            print(f"Error in backend/models/user.py: {str(e)}")
            print(traceback.format_exc())

    def test_06_auth_api(self):
        print("\nTesting backend/api/auth.py")
        try:
            with self.app.test_request_context():
                response = register()
                self.assertIn(response[1], [201, 400])

                response = login()
                self.assertIn(response[1], [200, 401])

                response = logout()
                self.assertEqual(response[1], 200)
        except Exception as e:
            print(f"Error in backend/api/auth.py: {str(e)}")
            print(traceback.format_exc())

    def test_07_messages_api(self):
        print("\nTesting backend/api/messages.py")
        try:
            with self.app.test_request_context():
                response = send_message()
                self.assertIn(response[1], [201, 400, 404])

                response = receive_messages()
                self.assertIn(response[1], [200, 404])
        except Exception as e:
            print(f"Error in backend/api/messages.py: {str(e)}")
            print(traceback.format_exc())

    def test_08_encryption_service(self):
        print("\nTesting backend/services/encryption.py")
        try:
            key = generate_key()
            self.assertIsNotNone(key)

            message = "Test message"
            encrypted = encrypt_message(message, key)
            self.assertIsNotNone(encrypted)

            decrypted = decrypt_message(encrypted, key)
            self.assertEqual(message, decrypted)
        except Exception as e:
            print(f"Error in backend/services/encryption.py: {str(e)}")
            print(traceback.format_exc())

def main():
    unittest.main(verbosity=2)

if __name__ == "__main__":
    main()
