
# api_utils.py
"""
Utility functions for API interactions.
This module provides a rate-limited request function to interact with the Anthropic API.
"""

import time
import asyncio
from anthropic import AsyncAnthropic, RateLimitError, APIError
import traceback
from constants import DEBUG

# Initialize the AsyncAnthropic client
client = AsyncAnthropic()

async def rate_limited_request(prompt, max_retries=3, base_delay=1):
    """
    Performs a rate-limited request to the Anthropic API.

    Args:
        prompt (str): The prompt to send to the API.
        max_retries (int): Maximum number of retries in case of rate limit errors.
        base_delay (int): Base delay between retries in seconds.

    Returns:
        str: The response from the API.

    Raises:
        Exception: If the request fails after all retries.
    """
    for attempt in range(max_retries):
        try:
            if DEBUG:
                print(f"Sending API request (attempt {attempt + 1}/{max_retries})...")

            response = await client.completions.create(
                prompt=prompt,
                max_tokens_to_sample=1000,
                model="claude-v1"
            )

            if DEBUG:
                print("API request successful.")

            return response.completion

        except RateLimitError as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                if DEBUG:
                    print(f"Rate limit reached. Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                if DEBUG:
                    print("Max retries reached. Unable to complete the request.")
                raise

        except APIError as e:
            if DEBUG:
                print(f"API Error occurred: {str(e)}")
                print(traceback.format_exc())
            raise

        except Exception as e:
            if DEBUG:
                print(f"Unexpected error occurred: {str(e)}")
                print(traceback.format_exc())
            raise

    raise Exception("Failed to complete the API request after multiple retries.")

# Unit tests
import unittest
from unittest.mock import patch, MagicMock

class TestApiUtils(unittest.TestCase):

    @patch('api_utils.AsyncAnthropic')
    async def test_rate_limited_request_success(self, mock_anthropic):
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_response = MagicMock()
        mock_response.completion = "Test response"
        mock_client.completions.create.return_value = mock_response

        result = await rate_limited_request("Test prompt")
        self.assertEqual(result, "Test response")

    @patch('api_utils.AsyncAnthropic')
    @patch('api_utils.asyncio.sleep')
    async def test_rate_limited_request_rate_limit_retry(self, mock_sleep, mock_anthropic):
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.completions.create.side_effect = [
            RateLimitError("Rate limit exceeded"),
            MagicMock(completion="Test response after retry")
        ]

        result = await rate_limited_request("Test prompt")
        self.assertEqual(result, "Test response after retry")
        mock_sleep.assert_called_once()

    @patch('api_utils.AsyncAnthropic')
    async def test_rate_limited_request_api_error(self, mock_anthropic):
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.completions.create.side_effect = APIError("API Error")

        with self.assertRaises(APIError):
            await rate_limited_request("Test prompt")

if __name__ == '__main__':
    unittest.main()
