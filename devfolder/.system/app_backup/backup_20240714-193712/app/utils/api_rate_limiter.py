
"""
app/utils/api_rate_limiter.py

This module implements API rate limiting functionality to prevent excessive requests
and ensure fair usage of the API.

Classes:
- APIRateLimiter: Provides a decorator to limit the rate of API calls.
"""

import time
from functools import wraps
from typing import Callable, Dict
import traceback

DEBUG = True

class APIRateLimiter:
    def __init__(self, calls: int, period: int):
        """
        Initialize the APIRateLimiter.

        Args:
            calls (int): Number of allowed calls in the given period.
            period (int): Time period in seconds.
        """
        self.calls = calls
        self.period = period
        self.timestamps: Dict[Callable, list] = {}

    def limit(self, func: Callable) -> Callable:
        """
        Decorator to limit the rate of calls to the wrapped function.

        Args:
            func (Callable): The function to be rate-limited.

        Returns:
            Callable: The wrapped function with rate limiting applied.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            if func not in self.timestamps:
                self.timestamps[func] = []

            # Remove timestamps outside the current period
            self.timestamps[func] = [t for t in self.timestamps[func] if now - t <= self.period]

            if len(self.timestamps[func]) >= self.calls:
                if DEBUG:
                    print(f"Rate limit exceeded for {func.__name__}. Waiting...")
                time.sleep(self.period - (now - self.timestamps[func][0]))

            try:
                result = func(*args, **kwargs)
                self.timestamps[func].append(time.time())
                return result
            except Exception as e:
                if DEBUG:
                    print(f"Error in {func.__name__}: {str(e)}")
                    print(traceback.format_exc())
                raise

        return wrapper

# Example usage:
if __name__ == "__main__":
    limiter = APIRateLimiter(calls=5, period=10)

    @limiter.limit
    def example_api_call():
        print("API call executed")

    # Test the rate limiting
    for _ in range(10):
        example_api_call()
        time.sleep(1)
