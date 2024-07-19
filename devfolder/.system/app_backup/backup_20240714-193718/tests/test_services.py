
"""
Contains unit tests for various service classes.
"""

import pytest
from unittest.mock import Mock, patch
from app.services import (
    AIService, ProjectManager, TaskManager, FileManager,
    WebBrowsingService, StateMonitoringService
)

# AIService Tests
def test_ai_service_generate_text():
    ai_service = AIService()
    with patch('app.services.AsyncAnthropic.messages.create') as mock_create:
        mock_create.return_value.content = [Mock(text="Generated text")]
        result = ai_service.generate_text("Test prompt", 100)
        assert result == "Generated text"
        mock_create.assert_called_once()

def test_ai_service_analyze_code():
    ai_service = AIService()
    with patch('app.services.AsyncAnthropic.messages.create') as mock_create:
        mock_create.return_value.content = [Mock(text='{"complexity": 5, "suggestions": ["Refactor function X"]}')]
        result = ai_service.analyze_code("def test(): pass")
        assert isinstance(result, dict)
        assert "complexity" in result
        assert "suggestions" in result

# ProjectManager Tests
@pytest.fixture
def project_manager():
    return ProjectManager()

def test_project_manager_create_project(project_manager):
    with patch('app.models.Project') as MockProject:
        MockProject.return_value.id = 1
        project = project_manager.create_project("Test Project", "Description", 1)
        assert project.id == 1
        assert project.name == "Test Project"

def test_project_manager_update_project(project_manager):
    with patch('app.models.Project.query') as mock_query:
        mock_project = Mock()
        mock_query.get.return_value = mock_project
        updated_project = project_manager.update_project(1, name="Updated Project")
        assert updated_project.name == "Updated Project"

# TaskManager Tests
@pytest.fixture
def task_manager():
    return TaskManager()

def test_task_manager_create_task(task_manager):
    with patch('app.models.Task') as MockTask:
        MockTask.return_value.id = 1
        task = task_manager.create_task("Test Task", "Description", 1)
        assert task.id == 1
        assert task.title == "Test Task"

def test_task_manager_update_task(task_manager):
    with patch('app.models.Task.query') as mock_query:
        mock_task = Mock()
        mock_query.get.return_value = mock_task
        updated_task = task_manager.update_task(1, status="completed")
        assert updated_task.status == "completed"

# FileManager Tests
@pytest.fixture
def file_manager():
    return FileManager()

def test_file_manager_create_file(file_manager):
    with patch('app.models.File') as MockFile:
        MockFile.return_value.id = 1
        file = file_manager.create_file("test.py", "print('Hello')", 1)
        assert file.id == 1
        assert file.name == "test.py"

def test_file_manager_update_file(file_manager):
    with patch('app.models.File.query') as mock_query:
        mock_file = Mock()
        mock_query.get.return_value = mock_file
        updated_file = file_manager.update_file(1, content="print('Updated')")
        assert updated_file.content == "print('Updated')"

# WebBrowsingService Tests
@pytest.fixture
def web_browsing_service():
    return WebBrowsingService()

def test_web_browsing_service_search(web_browsing_service):
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = "<html><body>Test Result</body></html>"
        results = web_browsing_service.search("test query")
        assert isinstance(results, list)
        assert len(results) > 0

def test_web_browsing_service_extract_content(web_browsing_service):
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = "<html><body><p>Extracted content</p></body></html>"
        content = web_browsing_service.extract_content("http://test.com")
        assert "Extracted content" in content

# StateMonitoringService Tests
@pytest.fixture
def state_monitoring_service():
    return StateMonitoringService()

def test_state_monitoring_service_get_current_state(state_monitoring_service):
    with patch('app.models.Project.query') as mock_query:
        mock_project = Mock()
        mock_project.tasks = [Mock(status="completed"), Mock(status="pending")]
        mock_query.get.return_value = mock_project
        state = state_monitoring_service.get_current_state(1)
        assert isinstance(state, dict)
        assert "total_tasks" in state
        assert "completed_tasks" in state

def test_state_monitoring_service_update_state(state_monitoring_service):
    with patch('app.models.Project.query') as mock_query:
        mock_project = Mock()
        mock_query.get.return_value = mock_project
        result = state_monitoring_service.update_state(1, {"status": "in_progress"})
        assert result is True
        assert mock_project.status == "in_progress"

if __name__ == "__main__":
    pytest.main()
