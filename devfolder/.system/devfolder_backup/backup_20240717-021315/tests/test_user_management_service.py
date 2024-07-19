
"""
Contains unit tests for the user management service.
"""

import unittest
from unittest.mock import MagicMock, patch
from app.services.user_management_service import UserManagementService
from app.models import User, Project

class TestUserManagementService(unittest.TestCase):

    def setUp(self):
        self.user_management_service = UserManagementService()

    @patch('app.models.User')
    def test_create_user(self, mock_user):
        # Arrange
        mock_user.return_value = MagicMock(id=1)
        username = "testuser"
        email = "testuser@example.com"
        password = "password123"

        # Act
        result = self.user_management_service.create_user(username, email, password)

        # Assert
        self.assertIsInstance(result, User)
        mock_user.assert_called_once_with(username=username, email=email)
        mock_user.return_value.set_password.assert_called_once_with(password)

    @patch('app.models.User.query')
    def test_update_user(self, mock_query):
        # Arrange
        mock_user = MagicMock(id=1)
        mock_query.get.return_value = mock_user
        user_id = 1
        new_email = "newemail@example.com"

        # Act
        result = self.user_management_service.update_user(user_id, email=new_email)

        # Assert
        self.assertEqual(result, mock_user)
        self.assertEqual(mock_user.email, new_email)

    @patch('app.models.User.query')
    def test_delete_user(self, mock_query):
        # Arrange
        mock_user = MagicMock(id=1)
        mock_query.get.return_value = mock_user
        user_id = 1

        # Act
        result = self.user_management_service.delete_user(user_id)

        # Assert
        self.assertTrue(result)
        mock_user.delete.assert_called_once()

    @patch('app.models.User.query')
    def test_get_user_projects(self, mock_query):
        # Arrange
        mock_user = MagicMock(id=1)
        mock_project1 = MagicMock(id=1, name="Project 1")
        mock_project2 = MagicMock(id=2, name="Project 2")
        mock_user.projects = [mock_project1, mock_project2]
        mock_query.get.return_value = mock_user
        user_id = 1

        # Act
        result = self.user_management_service.get_user_projects(user_id)

        # Assert
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Project)
        self.assertIsInstance(result[1], Project)
        self.assertEqual(result[0].name, "Project 1")
        self.assertEqual(result[1].name, "Project 2")

    @patch('app.models.User.query')
    def test_get_user_projects_no_user(self, mock_query):
        # Arrange
        mock_query.get.return_value = None
        user_id = 999  # Non-existent user

        # Act
        result = self.user_management_service.get_user_projects(user_id)

        # Assert
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
