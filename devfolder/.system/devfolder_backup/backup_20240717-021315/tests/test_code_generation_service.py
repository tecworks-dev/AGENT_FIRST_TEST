
# tests/test_code_generation_service.py
"""
Contains unit tests for the code generation service.
"""

import unittest
from unittest.mock import Mock, patch
from app.services.code_generation_service import CodeGenerationService
from app.utils.api_utils import AsyncAnthropic
import asyncio

class TestCodeGenerationService(unittest.TestCase):
    def setUp(self):
        self.code_gen_service = CodeGenerationService()

    @patch('app.services.code_generation_service.AsyncAnthropic')
    def test_generate_code(self, mock_anthropic):
        # Mock the AI response
        mock_response = Mock()
        mock_response.content = [Mock(text="def example_function():\n    return 'Hello, World!'")]
        mock_anthropic.return_value.messages.create.return_value = mock_response

        # Test input
        specifications = {
            "language": "python",
            "task": "Create a simple function that returns 'Hello, World!'"
        }

        # Run the test
        result = asyncio.run(self.code_gen_service.generate_code(specifications))

        # Assertions
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], tuple)
        self.assertEqual(len(result[0]), 2)
        self.assertEqual(result[0][0], "example_function.py")
        self.assertEqual(result[0][1], "def example_function():\n    return 'Hello, World!'")

        # Verify that the AI was called with the correct prompt
        mock_anthropic.return_value.messages.create.assert_called_once()
        call_args = mock_anthropic.return_value.messages.create.call_args
        self.assertIn("Create a simple function that returns 'Hello, World!'", str(call_args))
        self.assertIn("python", str(call_args))

    @patch('app.services.code_generation_service.AsyncAnthropic')
    def test_refactor_code(self, mock_anthropic):
        # Mock the AI response
        mock_response = Mock()
        mock_response.content = [Mock(text="def improved_function():\n    return 'Hello, Improved World!'")]
        mock_anthropic.return_value.messages.create.return_value = mock_response

        # Test input
        code = "def old_function():\n    print('Hello, Old World!')"
        refactor_instructions = "Improve the function to return the greeting instead of printing it."

        # Run the test
        result = asyncio.run(self.code_gen_service.refactor_code(code, refactor_instructions))

        # Assertions
        self.assertIsInstance(result, str)
        self.assertEqual(result, "def improved_function():\n    return 'Hello, Improved World!'")

        # Verify that the AI was called with the correct prompt
        mock_anthropic.return_value.messages.create.assert_called_once()
        call_args = mock_anthropic.return_value.messages.create.call_args
        self.assertIn(code, str(call_args))
        self.assertIn(refactor_instructions, str(call_args))

    def test_invalid_specifications(self):
        # Test input
        invalid_specifications = {
            "invalid_key": "This should not work"
        }

        # Run the test and check for raised exception
        with self.assertRaises(ValueError):
            asyncio.run(self.code_gen_service.generate_code(invalid_specifications))

    @patch('app.services.code_generation_service.AsyncAnthropic')
    def test_ai_service_error(self, mock_anthropic):
        # Mock the AI to raise an exception
        mock_anthropic.return_value.messages.create.side_effect = Exception("AI service error")

        # Test input
        specifications = {
            "language": "python",
            "task": "Create a function that will cause an error"
        }

        # Run the test and check for raised exception
        with self.assertRaises(Exception) as context:
            asyncio.run(self.code_gen_service.generate_code(specifications))

        self.assertIn("AI service error", str(context.exception))

if __name__ == '__main__':
    unittest.main()
