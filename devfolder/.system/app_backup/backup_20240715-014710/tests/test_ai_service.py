
"""
Contains unit tests for the AI service.

This module includes test cases for various AI service methods, mock API responses,
and edge case handling tests to ensure the robustness of the AI service.
"""

import unittest
from unittest.mock import patch, MagicMock
import traceback
from app.services.ai_service import AIService
from app.utils.custom_exceptions import AIServiceException

class TestAIService(unittest.TestCase):
    def setUp(self):
        self.ai_service = AIService()

    @patch('app.services.ai_service.AsyncAnthropic')
    def test_generate_text(self, mock_anthropic):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Generated text")]
        mock_anthropic.return_value.messages.create.return_value = mock_response

        result = self.ai_service.generate_text("Test prompt", 100)
        self.assertEqual(result, "Generated text")

        if __debug__:
            print("Debug: test_generate_text passed")

    @patch('app.services.ai_service.AsyncAnthropic')
    def test_generate_text_error(self, mock_anthropic):
        mock_anthropic.return_value.messages.create.side_effect = Exception("API Error")

        with self.assertRaises(AIServiceException):
            self.ai_service.generate_text("Test prompt", 100)

        if __debug__:
            print("Debug: test_generate_text_error passed")

    @patch('app.services.ai_service.AsyncAnthropic')
    def test_analyze_code(self, mock_anthropic):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='{"complexity": 5, "suggestions": ["Refactor function X"]}')]
        mock_anthropic.return_value.messages.create.return_value = mock_response

        result = self.ai_service.analyze_code("def test(): pass")
        self.assertIsInstance(result, dict)
        self.assertIn("complexity", result)
        self.assertIn("suggestions", result)

        if __debug__:
            print("Debug: test_analyze_code passed")

    @patch('app.services.ai_service.AsyncAnthropic')
    def test_analyze_code_invalid_response(self, mock_anthropic):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='Invalid JSON')]
        mock_anthropic.return_value.messages.create.return_value = mock_response

        with self.assertRaises(AIServiceException):
            self.ai_service.analyze_code("def test(): pass")

        if __debug__:
            print("Debug: test_analyze_code_invalid_response passed")

    @patch('app.services.ai_service.AsyncAnthropic')
    def test_generate_unit_tests(self, mock_anthropic):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="def test_function(): assert True")]
        mock_anthropic.return_value.messages.create.return_value = mock_response

        result = self.ai_service.generate_unit_tests("def function(): return True")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

        if __debug__:
            print("Debug: test_generate_unit_tests passed")

    @patch('app.services.ai_service.AsyncAnthropic')
    def test_optimize_code(self, mock_anthropic):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="def optimized_function(): return True")]
        mock_anthropic.return_value.messages.create.return_value = mock_response

        result = self.ai_service.optimize_code("def function(): return True")
        self.assertIsInstance(result, str)
        self.assertIn("optimized_function", result)

        if __debug__:
            print("Debug: test_optimize_code passed")

    def test_invalid_max_tokens(self):
        with self.assertRaises(ValueError):
            self.ai_service.generate_text("Test prompt", -1)

        if __debug__:
            print("Debug: test_invalid_max_tokens passed")

    @patch('app.services.ai_service.AsyncAnthropic')
    def test_rate_limit_handling(self, mock_anthropic):
        mock_anthropic.return_value.messages.create.side_effect = [
            Exception("Rate limit exceeded"),
            MagicMock(content=[MagicMock(text="Generated text after retry")])
        ]

        result = self.ai_service.generate_text("Test prompt", 100)
        self.assertEqual(result, "Generated text after retry")

        if __debug__:
            print("Debug: test_rate_limit_handling passed")

def main():
    try:
        unittest.main()
    except Exception as e:
        print(f"An error occurred while running the tests: {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
