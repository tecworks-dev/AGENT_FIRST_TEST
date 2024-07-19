
"""
Contains unit tests for the data persistence service.
This file tests the functionality of saving and loading project states,
as well as project backup functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
import json
from app.services.data_persistence_service import DataPersistenceService
from app.models import Project

class TestDataPersistenceService(unittest.TestCase):
    def setUp(self):
        self.service = DataPersistenceService()
        self.mock_project = MagicMock(spec=Project)
        self.mock_project.id = 1
        self.mock_project.name = "Test Project"
        self.mock_project.to_dict.return_value = {
            "id": 1,
            "name": "Test Project",
            "description": "A test project",
            "user_id": 1
        }

    @patch('app.services.data_persistence_service.db.session')
    def test_save_project_state(self, mock_db_session):
        state = {"tasks": [{"id": 1, "title": "Task 1"}]}
        result = self.service.save_project_state(self.mock_project.id, state)
        
        self.assertTrue(result)
        mock_db_session.commit.assert_called_once()

    @patch('app.services.data_persistence_service.Project')
    def test_load_project_state(self, mock_project):
        mock_project.query.get.return_value = self.mock_project
        self.mock_project.state = json.dumps({"tasks": [{"id": 1, "title": "Task 1"}]})
        
        result = self.service.load_project_state(self.mock_project.id)
        
        self.assertEqual(result, {"tasks": [{"id": 1, "title": "Task 1"}]})

    @patch('app.services.data_persistence_service.os')
    @patch('app.services.data_persistence_service.json')
    def test_backup_project(self, mock_json, mock_os):
        mock_os.path.exists.return_value = True
        mock_os.makedirs = MagicMock()
        mock_open = mock_os.open
        
        with patch('builtins.open', mock_open):
            result = self.service.backup_project(self.mock_project.id)
        
        self.assertTrue(result.endswith('.json'))
        mock_json.dump.assert_called_once()

    @patch('app.services.data_persistence_service.Project')
    @patch('app.services.data_persistence_service.os')
    def test_restore_project_from_backup(self, mock_os, mock_project):
        mock_project.query.get.return_value = self.mock_project
        mock_os.path.exists.return_value = True
        mock_open = mock_os.open
        
        backup_data = {
            "id": 1,
            "name": "Test Project",
            "description": "A test project",
            "user_id": 1,
            "state": {"tasks": [{"id": 1, "title": "Task 1"}]}
        }
        
        with patch('builtins.open', mock_open):
            with patch('json.load', return_value=backup_data):
                result = self.service.restore_project_from_backup(self.mock_project.id, "backup.json")
        
        self.assertTrue(result)
        self.mock_project.name = "Test Project"
        self.mock_project.description = "A test project"
        self.mock_project.state = json.dumps({"tasks": [{"id": 1, "title": "Task 1"}]})

    def test_load_project_state_not_found(self):
        with patch('app.services.data_persistence_service.Project') as mock_project:
            mock_project.query.get.return_value = None
            result = self.service.load_project_state(999)
            self.assertIsNone(result)

    @patch('app.services.data_persistence_service.os')
    def test_backup_project_directory_creation(self, mock_os):
        mock_os.path.exists.return_value = False
        mock_os.makedirs = MagicMock()
        
        with patch('builtins.open', MagicMock()):
            self.service.backup_project(self.mock_project.id)
        
        mock_os.makedirs.assert_called_once()

    @patch('app.services.data_persistence_service.Project')
    @patch('app.services.data_persistence_service.os')
    def test_restore_project_from_backup_file_not_found(self, mock_os, mock_project):
        mock_os.path.exists.return_value = False
        
        result = self.service.restore_project_from_backup(self.mock_project.id, "nonexistent_backup.json")
        
        self.assertFalse(result)

    @patch('app.services.data_persistence_service.db.session')
    def test_save_project_state_database_error(self, mock_db_session):
        mock_db_session.commit.side_effect = Exception("Database error")
        
        state = {"tasks": [{"id": 1, "title": "Task 1"}]}
        result = self.service.save_project_state(self.mock_project.id, state)
        
        self.assertFalse(result)
        mock_db_session.rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()
