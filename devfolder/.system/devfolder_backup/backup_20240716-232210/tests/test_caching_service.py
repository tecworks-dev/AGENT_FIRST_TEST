
"""
Contains unit tests for the caching service.
"""

import unittest
from unittest.mock import Mock, patch
import time
from app.services.caching_service import CachingService

class TestCachingService(unittest.TestCase):
    def setUp(self):
        self.caching_service = CachingService()

    def test_set_and_get(self):
        """Test basic set and get operations"""
        self.caching_service.set("test_key", "test_value", 60)
        self.assertEqual(self.caching_service.get("test_key"), "test_value")

    def test_get_nonexistent_key(self):
        """Test getting a non-existent key returns None"""
        self.assertIsNone(self.caching_service.get("nonexistent_key"))

    def test_delete(self):
        """Test deleting a cached item"""
        self.caching_service.set("delete_key", "delete_value", 60)
        self.caching_service.delete("delete_key")
        self.assertIsNone(self.caching_service.get("delete_key"))

    def test_cache_expiration(self):
        """Test cache expiration"""
        self.caching_service.set("expiring_key", "expiring_value", 1)
        time.sleep(1.1)  # Wait for slightly more than 1 second
        self.assertIsNone(self.caching_service.get("expiring_key"))

    def test_update_existing_key(self):
        """Test updating an existing key"""
        self.caching_service.set("update_key", "original_value", 60)
        self.caching_service.set("update_key", "updated_value", 60)
        self.assertEqual(self.caching_service.get("update_key"), "updated_value")

    def test_set_with_zero_expiration(self):
        """Test setting a key with zero expiration time"""
        self.caching_service.set("zero_expiry", "zero_value", 0)
        self.assertIsNone(self.caching_service.get("zero_expiry"))

    def test_set_with_negative_expiration(self):
        """Test setting a key with negative expiration time"""
        with self.assertRaises(ValueError):
            self.caching_service.set("negative_expiry", "negative_value", -1)

    @patch('app.services.caching_service.time.time')
    def test_cache_cleanup(self, mock_time):
        """Test cache cleanup of expired items"""
        mock_time.return_value = 1000  # Set a fixed current time
        self.caching_service.set("expired_key", "expired_value", 10)
        self.caching_service.set("valid_key", "valid_value", 30)
        
        mock_time.return_value = 1020  # Advance time by 20 seconds
        self.caching_service._cleanup_expired()
        
        self.assertIsNone(self.caching_service.get("expired_key"))
        self.assertEqual(self.caching_service.get("valid_key"), "valid_value")

    def test_cache_max_size(self):
        """Test cache respects max size limit"""
        original_max_size = self.caching_service.max_size
        self.caching_service.max_size = 3
        
        self.caching_service.set("key1", "value1", 60)
        self.caching_service.set("key2", "value2", 60)
        self.caching_service.set("key3", "value3", 60)
        self.caching_service.set("key4", "value4", 60)
        
        self.assertEqual(len(self.caching_service.cache), 3)
        self.assertIsNone(self.caching_service.get("key1"))  # Oldest key should be removed
        
        self.caching_service.max_size = original_max_size  # Restore original max size

    @patch('app.services.caching_service.logging')
    def test_logging_on_error(self, mock_logging):
        """Test that errors are logged"""
        with patch.object(self.caching_service, 'get', side_effect=Exception("Test error")):
            self.caching_service.get("error_key")
            mock_logging.error.assert_called_once_with("Error in caching service: Test error")

if __name__ == '__main__':
    unittest.main()
