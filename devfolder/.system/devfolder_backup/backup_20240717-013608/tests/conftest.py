
"""
Defines fixtures and configuration for pytest.

This file contains fixtures and configuration settings for pytest,
including test database setup, application context creation, and
mock object definitions.
"""

import pytest
from app import create_app, db
from app.models import User, Project, Task
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture(scope='module')
def test_app():
    """Create and configure a test Flask app."""
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def test_client(test_app):
    """Create a test client for the app."""
    return test_app.test_client()

@pytest.fixture(scope='module')
def init_database(test_app):
    """Initialize the test database with sample data."""
    with test_app.app_context():
        # Create test users
        user1 = User(username='testuser1', email='testuser1@example.com')
        user1.set_password('testpassword1')
        user2 = User(username='testuser2', email='testuser2@example.com')
        user2.set_password('testpassword2')
        db.session.add_all([user1, user2])

        # Create test projects
        project1 = Project(name='Test Project 1', description='A test project', user_id=user1.id)
        project2 = Project(name='Test Project 2', description='Another test project', user_id=user2.id)
        db.session.add_all([project1, project2])

        # Create test tasks
        task1 = Task(title='Test Task 1', description='A test task', project_id=project1.id, assigned_to=user1.id)
        task2 = Task(title='Test Task 2', description='Another test task', project_id=project2.id, assigned_to=user2.id)
        db.session.add_all([task1, task2])

        db.session.commit()

        yield db  # this is where the testing happens

        db.drop_all()

@pytest.fixture(scope='function')
def mock_ai_service():
    """Mock AI service for testing."""
    class MockAIService:
        def generate_text(self, prompt, max_tokens):
            return "Mock AI generated text"

        def analyze_code(self, code):
            return {"complexity": "low", "suggestions": ["Mock suggestion"]}

    return MockAIService()

@pytest.fixture(scope='function')
def mock_web_browsing_service():
    """Mock web browsing service for testing."""
    class MockWebBrowsingService:
        def search(self, query):
            return [{"title": "Mock result", "url": "http://mock.com", "snippet": "Mock snippet"}]

        def extract_content(self, url):
            return "Mock extracted content"

        def summarize(self, content):
            return "Mock summary"

    return MockWebBrowsingService()

@pytest.fixture(scope='function')
def mock_state_monitoring_service():
    """Mock state monitoring service for testing."""
    class MockStateMonitoringService:
        def get_current_state(self, project_id):
            return {"status": "in_progress", "completion": 50}

        def update_state(self, project_id, new_state):
            return True

        def track_progress(self, project_id):
            return 0.5

    return MockStateMonitoringService()

# Add more fixtures as needed for other services or components

if __name__ == '__main__':
    pytest.main([__file__])
