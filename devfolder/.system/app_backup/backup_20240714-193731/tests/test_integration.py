
# tests/test_integration.py

"""
Contains integration tests for the AI Software Factory application.
This file includes end-to-end test cases, API integration tests, and database integration tests.
"""

import unittest
import json
from flask import url_for
from app import create_app, db
from app.models import User, Project, Task, File
from app.services import AIService, ProjectManager, TaskManager, FileManager
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def register_user(self, username, email, password):
        return self.client.post('/auth/register', data={
            'username': username,
            'email': email,
            'password': password,
            'password2': password
        }, follow_redirects=True)

    def login_user(self, email, password):
        return self.client.post('/auth/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

    def test_user_registration_and_login(self):
        # Test user registration
        response = self.register_user('testuser', 'test@example.com', 'password123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)

        # Test user login
        response = self.login_user('test@example.com', 'password123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, testuser!', response.data)

    def test_project_creation_and_retrieval(self):
        # Register and login a user
        self.register_user('testuser', 'test@example.com', 'password123')
        self.login_user('test@example.com', 'password123')

        # Create a new project
        response = self.client.post('/projects/create', data={
            'name': 'Test Project',
            'description': 'This is a test project'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Project created successfully', response.data)

        # Retrieve the project
        response = self.client.get('/projects')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Project', response.data)
        self.assertIn(b'This is a test project', response.data)

    def test_task_creation_and_update(self):
        # Register, login, and create a project
        self.register_user('testuser', 'test@example.com', 'password123')
        self.login_user('test@example.com', 'password123')
        self.client.post('/projects/create', data={
            'name': 'Test Project',
            'description': 'This is a test project'
        })

        # Get the project ID
        project = Project.query.filter_by(name='Test Project').first()

        # Create a new task
        response = self.client.post(f'/projects/{project.id}/tasks/create', data={
            'title': 'Test Task',
            'description': 'This is a test task'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task created successfully', response.data)

        # Update the task status
        task = Task.query.filter_by(title='Test Task').first()
        response = self.client.post(f'/tasks/{task.id}/update', data={
            'status': 'in_progress'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task updated successfully', response.data)

        # Verify the task status
        updated_task = Task.query.get(task.id)
        self.assertEqual(updated_task.status, 'in_progress')

    def test_ai_service_integration(self):
        # Register, login, and create a project
        self.register_user('testuser', 'test@example.com', 'password123')
        self.login_user('test@example.com', 'password123')
        self.client.post('/projects/create', data={
            'name': 'AI Test Project',
            'description': 'Testing AI integration'
        })

        project = Project.query.filter_by(name='AI Test Project').first()

        # Test AI-assisted code generation
        response = self.client.post(f'/projects/{project.id}/generate_code', data={
            'prompt': 'Create a Python function to calculate the factorial of a number'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Code generated successfully', response.data)

        # Verify that a file was created
        file = File.query.filter_by(project_id=project.id).first()
        self.assertIsNotNone(file)
        self.assertIn('factorial', file.content.lower())

    def test_web_browsing_service(self):
        # Register and login a user
        self.register_user('testuser', 'test@example.com', 'password123')
        self.login_user('test@example.com', 'password123')

        # Test web browsing for research
        response = self.client.post('/web_browse', data={
            'query': 'Python best practices'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Web browsing results', response.data)

    def test_database_integration(self):
        # Test creating a user directly in the database
        user = User(username='dbuser', email='dbuser@example.com')
        user.set_password('dbpassword')
        db.session.add(user)
        db.session.commit()

        # Verify the user was created
        fetched_user = User.query.filter_by(username='dbuser').first()
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user.email, 'dbuser@example.com')

        # Test creating a project for the user
        project = Project(name='DB Test Project', description='Testing database integration', user_id=user.id)
        db.session.add(project)
        db.session.commit()

        # Verify the project was created and associated with the user
        fetched_project = Project.query.filter_by(name='DB Test Project').first()
        self.assertIsNotNone(fetched_project)
        self.assertEqual(fetched_project.user_id, user.id)

    def test_api_integration(self):
        # Register and login a user
        self.register_user('apiuser', 'apiuser@example.com', 'apipassword')
        response = self.login_user('apiuser@example.com', 'apipassword')

        # Extract the API token from the response
        api_token = json.loads(response.data)['api_token']

        # Test creating a project via API
        response = self.client.post('/api/projects', 
                                    headers={'Authorization': f'Bearer {api_token}'},
                                    json={'name': 'API Test Project', 'description': 'Testing API integration'})
        self.assertEqual(response.status_code, 201)
        project_id = json.loads(response.data)['id']

        # Test retrieving the project via API
        response = self.client.get(f'/api/projects/{project_id}',
                                   headers={'Authorization': f'Bearer {api_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['name'], 'API Test Project')

        # Test creating a task via API
        response = self.client.post(f'/api/projects/{project_id}/tasks',
                                    headers={'Authorization': f'Bearer {api_token}'},
                                    json={'title': 'API Test Task', 'description': 'Testing task creation via API'})
        self.assertEqual(response.status_code, 201)
        task_id = json.loads(response.data)['id']

        # Test updating the task status via API
        response = self.client.patch(f'/api/tasks/{task_id}',
                                     headers={'Authorization': f'Bearer {api_token}'},
                                     json={'status': 'completed'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['status'], 'completed')

if __name__ == '__main__':
    unittest.main()
