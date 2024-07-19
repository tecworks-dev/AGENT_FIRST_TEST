
"""
Contains tests for the application routes.

This file includes test cases for different HTTP endpoints, authentication tests,
and response validation tests for the Flask application.
"""

import pytest
from flask import url_for
from app.models import User, Project, Task
from app import create_app, db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def auth_client(client):
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    client.post(url_for('auth.login'), data={'email': 'test@example.com', 'password': 'password123'})
    return client

def test_home_page(client):
    response = client.get(url_for('main.index'))
    assert response.status_code == 200
    assert b"AI Software Factory" in response.data

def test_login_page(client):
    response = client.get(url_for('auth.login'))
    assert response.status_code == 200
    assert b"Login" in response.data

def test_register_page(client):
    response = client.get(url_for('auth.register'))
    assert response.status_code == 200
    assert b"Register" in response.data

def test_create_project(auth_client):
    response = auth_client.post(url_for('main.create_project'), data={
        'name': 'Test Project',
        'description': 'This is a test project'
    })
    assert response.status_code == 302  # Redirect after successful creation
    project = Project.query.filter_by(name='Test Project').first()
    assert project is not None

def test_create_task(auth_client):
    project = Project(name='Test Project', description='Test Description', user_id=1)
    db.session.add(project)
    db.session.commit()

    response = auth_client.post(url_for('main.create_task', project_id=project.id), data={
        'title': 'Test Task',
        'description': 'This is a test task'
    })
    assert response.status_code == 302  # Redirect after successful creation
    task = Task.query.filter_by(title='Test Task').first()
    assert task is not None

def test_update_task_status(auth_client):
    project = Project(name='Test Project', description='Test Description', user_id=1)
    db.session.add(project)
    task = Task(title='Test Task', description='Test Description', project_id=project.id)
    db.session.add(task)
    db.session.commit()

    response = auth_client.post(url_for('main.update_task', task_id=task.id), data={
        'status': 'completed'
    })
    assert response.status_code == 200
    updated_task = Task.query.get(task.id)
    assert updated_task.status == 'completed'

def test_unauthorized_access(client):
    response = client.get(url_for('main.user_profile', user_id=1))
    assert response.status_code == 302  # Redirect to login page
    assert url_for('auth.login') in response.location

def test_404_error(client):
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
    assert b"Page Not Found" in response.data

def test_csrf_protection(client):
    response = client.post(url_for('auth.login'), data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400  # Bad Request due to missing CSRF token

def test_api_rate_limiting(client):
    for _ in range(100):
        response = client.get(url_for('main.index'))
    assert response.status_code == 429  # Too Many Requests

if __name__ == '__main__':
    pytest.main()
