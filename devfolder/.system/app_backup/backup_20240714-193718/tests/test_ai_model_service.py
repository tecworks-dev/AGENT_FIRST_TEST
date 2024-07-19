
"""
Contains unit tests for the AI model service.
"""

import unittest
from unittest.mock import patch, MagicMock
import traceback
from app.services.ai_model_service import AIModelService

class TestAIModelService(unittest.TestCase):
    def setUp(self):
        self.ai_model_service = AIModelService()

    @patch('app.services.ai_model_service.AsyncAnthropic')
    def test_load_model(self, mock_anthropic):
        try:
            # Test successful model loading
            mock_anthropic.return_value.load_model.return_value = MagicMock()
            model = self.ai_model_service.load_model('test_model')
            self.assertIsNotNone(model)
            mock_anthropic.return_value.load_model.assert_called_once_with('test_model')

            # Test model loading failure
            mock_anthropic.return_value.load_model.side_effect = Exception("Model not found")
            with self.assertRaises(Exception):
                self.ai_model_service.load_model('nonexistent_model')

        except Exception as e:
            self.fail(f"Test failed: {str(e)}\n{traceback.format_exc()}")

    @patch('app.services.ai_model_service.AsyncAnthropic')
    def test_generate_response(self, mock_anthropic):
        try:
            mock_model = MagicMock()
            mock_anthropic.return_value.generate_response.return_value = "Generated response"

            response = self.ai_model_service.generate_response("Test prompt", mock_model)
            self.assertEqual(response, "Generated response")
            mock_anthropic.return_value.generate_response.assert_called_once_with("Test prompt", mock_model)

            # Test response generation failure
            mock_anthropic.return_value.generate_response.side_effect = Exception("Generation failed")
            with self.assertRaises(Exception):
                self.ai_model_service.generate_response("Test prompt", mock_model)

        except Exception as e:
            self.fail(f"Test failed: {str(e)}\n{traceback.format_exc()}")

    @patch('app.services.ai_model_service.AsyncAnthropic')
    def test_fine_tune_model(self, mock_anthropic):
        try:
            mock_model = MagicMock()
            mock_anthropic.return_value.fine_tune_model.return_value = MagicMock()

            training_data = [{"input": "Test input", "output": "Test output"}]
            fine_tuned_model = self.ai_model_service.fine_tune_model(mock_model, training_data)
            self.assertIsNotNone(fine_tuned_model)
            mock_anthropic.return_value.fine_tune_model.assert_called_once_with(mock_model, training_data)

            # Test fine-tuning failure
            mock_anthropic.return_value.fine_tune_model.side_effect = Exception("Fine-tuning failed")
            with self.assertRaises(Exception):
                self.ai_model_service.fine_tune_model(mock_model, training_data)

        except Exception as e:
            self.fail(f"Test failed: {str(e)}\n{traceback.format_exc()}")

def main():
    unittest.main()

if __name__ == '__main__':
    main()
