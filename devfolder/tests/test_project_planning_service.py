
import unittest
from unittest.mock import patch, MagicMock
import asyncio
from app.services.project_planning_service import ProjectPlanningService
from app.utils.api_utils import AsyncAnthropic

class TestProjectPlanningService(unittest.TestCase):
    def setUp(self):
        self.service = ProjectPlanningService()

    @patch('app.services.project_planning_service.AsyncAnthropic')
    def test_generate_project_plan(self, mock_anthropic):
        # Mock the AsyncAnthropic client
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        # Mock the response from the AI model
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='{"tasks": [{"name": "Task 1", "description": "Description 1"}]}')]
        mock_client.messages.create.return_value = asyncio.Future()
        mock_client.messages.create.return_value.set_result(mock_response)

        # Test the generate_project_plan method
        requirements = "Create a web application"
        result = asyncio.run(self.service.generate_project_plan(requirements))

        # Assert that the result is a dictionary
        self.assertIsInstance(result, dict)
        # Assert that the result contains a 'tasks' key
        self.assertIn('tasks', result)
        # Assert that the tasks list is not empty
        self.assertGreater(len(result['tasks']), 0)
        # Assert that the first task has the expected structure
        self.assertIn('name', result['tasks'][0])
        self.assertIn('description', result['tasks'][0])

    @patch('app.services.project_planning_service.AsyncAnthropic')
    def test_update_project_plan(self, mock_anthropic):
        # Mock the AsyncAnthropic client
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        # Mock the response from the AI model
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='{"tasks": [{"name": "Updated Task", "description": "Updated Description"}]}')]
        mock_client.messages.create.return_value = asyncio.Future()
        mock_client.messages.create.return_value.set_result(mock_response)

        # Test the update_project_plan method
        current_plan = {"tasks": [{"name": "Old Task", "description": "Old Description"}]}
        new_requirements = "Add user authentication"
        result = asyncio.run(self.service.update_project_plan(current_plan, new_requirements))

        # Assert that the result is a dictionary
        self.assertIsInstance(result, dict)
        # Assert that the result contains a 'tasks' key
        self.assertIn('tasks', result)
        # Assert that the tasks list is not empty
        self.assertGreater(len(result['tasks']), 0)
        # Assert that the first task has been updated
        self.assertEqual(result['tasks'][0]['name'], "Updated Task")
        self.assertEqual(result['tasks'][0]['description'], "Updated Description")

    def test_invalid_input(self):
        # Test with invalid input
        with self.assertRaises(ValueError):
            asyncio.run(self.service.generate_project_plan(""))

        with self.assertRaises(ValueError):
            asyncio.run(self.service.update_project_plan({}, ""))

    @patch('app.services.project_planning_service.AsyncAnthropic')
    def test_ai_service_error(self, mock_anthropic):
        # Mock the AsyncAnthropic client to raise an exception
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("AI service error")

        # Test that the service handles AI errors gracefully
        with self.assertRaises(Exception) as context:
            asyncio.run(self.service.generate_project_plan("Create a web application"))

        self.assertIn("AI service error", str(context.exception))

    def test_plan_structure(self):
        # Test that the generated plan has the correct structure
        plan = {
            "tasks": [
                {"name": "Task 1", "description": "Description 1"},
                {"name": "Task 2", "description": "Description 2"}
            ]
        }

        # Validate the plan structure
        self.validate_plan_structure(plan)

    def validate_plan_structure(self, plan):
        self.assertIsInstance(plan, dict)
        self.assertIn('tasks', plan)
        self.assertIsInstance(plan['tasks'], list)
        for task in plan['tasks']:
            self.assertIsInstance(task, dict)
            self.assertIn('name', task)
            self.assertIn('description', task)
            self.assertIsInstance(task['name'], str)
            self.assertIsInstance(task['description'], str)

if __name__ == '__main__':
    unittest.main()
