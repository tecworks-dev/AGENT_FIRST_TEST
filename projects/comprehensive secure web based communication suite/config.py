# config.py
"""
Purpose: Contains configuration settings for the secure communication suite application.
Description: This module provides a Config class to manage and retrieve configuration settings.
"""

import os
import json
import traceback
from typing import Any  # Add this import

DEBUG = True

class Config:
    """
    A class to manage configuration settings for the application.
    """

    def __init__(self):
        """
        Initialize the Config class by loading settings from a JSON file.
        """
        self.settings = {}
        self.config_file = 'config.json'
        self._load_config()

    def _load_config(self):
        """
        Load configuration settings from a JSON file.
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.settings = json.load(f)
            else:
                self._create_default_config()
        except Exception as e:
            if DEBUG:
                print(f"Debug: Error loading configuration: {str(e)}")
            print(f"Error: Unable to load configuration. Using default settings.")
            traceback.print_exc()
            self._create_default_config()

    def _create_default_config(self):
        """
        Create a default configuration if the config file doesn't exist.
        """
        self.settings = {
            'encryption_key': 'default_key',
            'server_host': 'localhost',
            'server_port': 8000,
            'debug_mode': True,
            'max_file_size': 10485760,  # 10 MB
            'allowed_file_types': ['.txt', '.pdf', '.jpg', '.png'],
            'max_message_length': 1000,
            'session_timeout': 3600,  # 1 hour
        }
        self._save_config()

    def _save_config(self):
        """
        Save the current configuration to the JSON file.
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            if DEBUG:
                print(f"Debug: Error saving configuration: {str(e)}")
            print(f"Error: Unable to save configuration.")
            traceback.print_exc()

    def get_setting(self, key: str) -> Any:
        """
        Retrieve a configuration setting by its key.

        Args:
            key (str): The key of the setting to retrieve.

        Returns:
            Any: The value of the requested setting, or None if not found.
        """
        try:
            return self.settings.get(key)
        except Exception as e:
            if DEBUG:
                print(f"Debug: Error retrieving setting '{key}': {str(e)}")
            print(f"Error: Unable to retrieve setting '{key}'.")
            traceback.print_exc()
            return None

    def set_setting(self, key: str, value: Any) -> bool:
        """
        Set a configuration setting.

        Args:
            key (str): The key of the setting to set.
            value (Any): The value to set for the given key.

        Returns:
            bool: True if the setting was successfully set, False otherwise.
        """
        try:
            self.settings[key] = value
            self._save_config()
            return True
        except Exception as e:
            if DEBUG:
                print(f"Debug: Error setting configuration '{key}': {str(e)}")
            print(f"Error: Unable to set configuration '{key}'.")
            traceback.print_exc()
            return False

if __name__ == "__main__":
    # For testing purposes
    config = Config()
    print("Current configuration:")
    print(json.dumps(config.settings, indent=4))

    # Test getting a setting
    print("\nTesting get_setting:")
    print(f"Server host: {config.get_setting('server_host')}")
    print(f"Non-existent setting: {config.get_setting('non_existent')}")

    # Test setting a new configuration
    print("\nTesting set_setting:")
    success = config.set_setting('new_setting', 'test_value')
    print(f"Set new setting: {'Success' if success else 'Failed'}")
    print(f"New setting value: {config.get_setting('new_setting')}")