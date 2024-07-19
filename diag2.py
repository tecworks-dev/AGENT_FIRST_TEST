import unittest
import json
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.message import Message
from app.models.media import Media
from io import BytesIO
from app import create_app, socketio, db
from flask_sqlalchemy import SQLAlchemy
from config import Config

class FlaskRoutesTest(unittest.TestCase):
    def setUp(self):
        # self.app = create_app('testing')
        db.init_app(app)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user
        self.test_user = User(username='testuser', password_hash='testpass')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_routes(self):
        routes = [
            ('/login', 'POST', {'username': 'testuser', 'password': 'testpass'}),
            ('/register', 'POST', {'username': 'newuser', 'password': 'newpass'}),
            ('/logout', 'POST', {}),
            ('/messages', 'GET', {}),
            ('/messages', 'POST', {'receiver_id': 1, 'content': 'Test message'}),
            ('/messages/1', 'GET', {}),
            ('/messages/1', 'PUT', {'content': 'Updated message'}),
            ('/messages/1', 'DELETE', {}),
            ('/media', 'POST', {'file': (BytesIO(b'test file content'), 'test.txt')}),
            ('/media/1', 'GET', {}),
            ('/media/1', 'DELETE', {}),
            ('/search', 'GET', {'query': 'test'}),
        ]

        unexpected_responses = []

        for route, method, data in routes:
            if method == 'GET':
                response = self.client.get(route, query_string=data)
            elif method == 'POST':
                response = self.client.post(route, data=data)
            elif method == 'PUT':
                response = self.client.put(route, data=data)
            elif method == 'DELETE':
                response = self.client.delete(route)

            if response.status_code not in [200, 201, 204]:
                unexpected_responses.append({
                    'route': route,
                    'method': method,
                    'data': data,
                    'response': response.get_data(as_text=True),
                    'status_code': response.status_code
                })

        self.report_unexpected_responses(unexpected_responses)

    def report_unexpected_responses(self, unexpected_responses):
        if unexpected_responses:
            print("\nUnexpected Responses:")
            for resp in unexpected_responses:
                print(f"""<route name="{resp['route']} {resp['method']}">
  <data>{json.dumps(resp['data'])}</data>
  <response>{resp['response']}</response>
  <httpcode>{resp['status_code']}</httpcode>
</route>
""")
        else:
            print("All routes responded as expected.")

if __name__ == '__main__':
    unittest.main()