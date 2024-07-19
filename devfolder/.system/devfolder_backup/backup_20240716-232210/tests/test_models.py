
# Purpose: Contains unit tests for database models.
# Description: This file includes test cases for User, Project, Task, and File models,
# as well as relationship tests and model method tests.

import pytest
from app.models import User, Project, Task, File
from app import db

@pytest.fixture
def user(app):
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()

@pytest.fixture
def project(app, user):
    with app.app_context():
        project = Project(name='Test Project', description='A test project', user_id=user.id)
        db.session.add(project)
        db.session.commit()
        yield project
        db.session.delete(project)
        db.session.commit()

@pytest.fixture
def task(app, project):
    with app.app_context():
        task = Task(title='Test Task', description='A test task', project_id=project.id)
        db.session.add(task)
        db.session.commit()
        yield task
        db.session.delete(task)
        db.session.commit()

@pytest.fixture
def file(app, project):
    with app.app_context():
        file = File(name='test_file.py', content='print("Hello, World!")', project_id=project.id)
        db.session.add(file)
        db.session.commit()
        yield file
        db.session.delete(file)
        db.session.commit()

def test_user_model(user):
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.check_password('password123')
    assert not user.check_password('wrongpassword')

def test_project_model(project, user):
    assert project.name == 'Test Project'
    assert project.description == 'A test project'
    assert project.user_id == user.id

def test_task_model(task, project):
    assert task.title == 'Test Task'
    assert task.description == 'A test task'
    assert task.project_id == project.id
    assert task.status == 'pending'

def test_file_model(file, project):
    assert file.name == 'test_file.py'
    assert file.content == 'print("Hello, World!")'
    assert file.project_id == project.id
    assert file.version == 1

def test_user_project_relationship(user, project):
    assert project in user.projects
    assert user == project.user

def test_project_task_relationship(project, task):
    assert task in project.tasks
    assert project == task.project

def test_project_file_relationship(project, file):
    assert file in project.files
    assert project == file.project

def test_user_to_dict(user):
    user_dict = user.to_dict()
    assert user_dict['username'] == 'testuser'
    assert user_dict['email'] == 'test@example.com'
    assert 'id' in user_dict
    assert 'password_hash' not in user_dict

def test_project_to_dict(project):
    project_dict = project.to_dict()
    assert project_dict['name'] == 'Test Project'
    assert project_dict['description'] == 'A test project'
    assert 'id' in project_dict
    assert 'user_id' in project_dict

def test_task_to_dict(task):
    task_dict = task.to_dict()
    assert task_dict['title'] == 'Test Task'
    assert task_dict['description'] == 'A test task'
    assert task_dict['status'] == 'pending'
    assert 'id' in task_dict
    assert 'project_id' in task_dict

def test_file_to_dict(file):
    file_dict = file.to_dict()
    assert file_dict['name'] == 'test_file.py'
    assert file_dict['content'] == 'print("Hello, World!")'
    assert file_dict['version'] == 1
    assert 'id' in file_dict
    assert 'project_id' in file_dict

if __name__ == '__main__':
    pytest.main()
