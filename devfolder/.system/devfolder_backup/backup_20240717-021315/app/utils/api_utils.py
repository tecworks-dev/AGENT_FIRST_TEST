
"""
Utility functions for API interactions.

This module provides utilities for managing API requests, including rate limiting
and error handling for interactions with external APIs, particularly the Anthropic API.
"""

import time
import asyncio
from collections import deque
from functools import wraps
from typing import Any, Callable
from anthropic import AsyncAnthropic, RateLimitError, APIError

import logging
import traceback

# Set up logging
logger = logging.getLogger(__name__)

# Debug flag
DEBUG = True

class APIRateLimiter:
    """
    Implements a rate limiter for API requests.
    """
    def __init__(self, rate_limit: int, time_window: int):
        """
        Initialize the rate limiter.

        :param rate_limit: Maximum number of requests allowed in the time window
        :param time_window: Time window in seconds
        """
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.request_times = deque()

    async def wait(self) -> None:
        """
        Wait if necessary to comply with the rate limit.
        """
        current_time = time.time()
        
        # Remove old request times
        while self.request_times and current_time - self.request_times[0] > self.time_window:
            self.request_times.popleft()
        
        if len(self.request_times) >= self.rate_limit:
            sleep_time = self.time_window - (current_time - self.request_times[0])
            if sleep_time > 0:
                if DEBUG:
                    logger.debug(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds.")
                await asyncio.sleep(sleep_time)
        
        self.request_times.append(time.time())

def rate_limited_request(func: Callable) -> Callable:
    """
    Decorator for rate-limiting API requests.

    :param func: The function to be rate-limited
    :return: Wrapped function
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        retries = 3
        while retries > 0:
            try:
                return await func(*args, **kwargs)
            except RateLimitError:
                if DEBUG:
                    logger.warning(f"Rate limit exceeded. Retrying in 5 seconds. Retries left: {retries}")
                await asyncio.sleep(5)
                retries -= 1
            except APIError as e:
                logger.error(f"API Error occurred: {str(e)}")
                if DEBUG:
                    logger.error(traceback.format_exc())
                raise
        raise Exception("Max retries exceeded for rate-limited request")
    return wrapper

class AnthropicAPI:
    """
    Wrapper class for Anthropic API interactions.
    """
    def __init__(self, api_key: str, rate_limit: int = 10, time_window: int = 60):
        """
        Initialize the Anthropic API wrapper.

        :param api_key: Anthropic API key
        :param rate_limit: Maximum number of requests allowed in the time window
        :param time_window: Time window in seconds
        """
        self.client = AsyncAnthropic(api_key=api_key)
        self.rate_limiter = APIRateLimiter(rate_limit, time_window)

    @rate_limited_request
    async def generate_text(self, prompt: str, max_tokens: int = 100) -> str:
        """
        Generate text using the Anthropic API.

        :param prompt: Input prompt for text generation
        :param max_tokens: Maximum number of tokens to generate
        :return: Generated text
        """
        await self.rate_limiter.wait()
        try:
            response = await self.client.completions.create(
                model="claude-2",
                prompt=prompt,
                max_tokens_to_sample=max_tokens
            )
            return response.completion
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            if DEBUG:
                logger.error(traceback.format_exc())
            raise

# Example usage
async def example_usage():
    api = AnthropicAPI("your-api-key-here")
    try:
        result = await api.generate_text("Hello, world!")
        print(result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(example_usage())
