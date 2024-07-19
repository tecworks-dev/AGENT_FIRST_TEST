
# Purpose: Implements caching mechanisms for improved performance.
# Description: This file contains the CachingService class which provides methods for getting, setting, and deleting cached items.

from typing import Any
import traceback
from redis import Redis
from datetime import timedelta

class CachingService:
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379, db: int = 0):
        """
        Initialize the CachingService with a Redis connection.
        
        :param redis_host: Redis server host
        :param redis_port: Redis server port
        :param db: Redis database number
        """
        self.redis = Redis(host=redis_host, port=redis_port, db=db)

    def get(self, key: str) -> Any:
        """
        Retrieve a value from the cache.
        
        :param key: The key to retrieve
        :return: The value associated with the key, or None if not found
        """
        try:
            value = self.redis.get(key)
            if value:
                return eval(value.decode('utf-8'))  # Deserialize the stored value
            return None
        except Exception as e:
            if __debug__:
                print(f"Error retrieving key '{key}' from cache: {str(e)}")
                traceback.print_exc()
            return None

    def set(self, key: str, value: Any, expiration: int) -> None:
        """
        Set a value in the cache with an expiration time.
        
        :param key: The key to set
        :param value: The value to store
        :param expiration: Expiration time in seconds
        """
        try:
            serialized_value = str(value)  # Simple serialization
            self.redis.setex(key, timedelta(seconds=expiration), serialized_value)
            if __debug__:
                print(f"Successfully set key '{key}' in cache with expiration {expiration} seconds")
        except Exception as e:
            if __debug__:
                print(f"Error setting key '{key}' in cache: {str(e)}")
                traceback.print_exc()

    def delete(self, key: str) -> None:
        """
        Delete a value from the cache.
        
        :param key: The key to delete
        """
        try:
            self.redis.delete(key)
            if __debug__:
                print(f"Successfully deleted key '{key}' from cache")
        except Exception as e:
            if __debug__:
                print(f"Error deleting key '{key}' from cache: {str(e)}")
                traceback.print_exc()

if __name__ == "__main__":
    # Example usage
    cache = CachingService()
    cache.set("example_key", "example_value", 3600)  # Cache for 1 hour
    value = cache.get("example_key")
    print(f"Retrieved value: {value}")
    cache.delete("example_key")
