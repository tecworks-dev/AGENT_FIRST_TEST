"""
Configuration settings for the application.

This module provides functions to load and retrieve configuration settings
for the secure messaging platform.
"""

import json
import os
import traceback

DEBUG = True

def load_config(config_file: str) -> dict:
    """
    Loads configuration from a file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: A dictionary containing the configuration settings.
    """
    try:
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file not found: {config_file}")

        with open(config_file, 'r') as file:
            config = json.load(file)
        
        if DEBUG:
            print(f"Configuration loaded successfully from {config_file}")
        
        return config
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in configuration file: {str(e)}")
        if DEBUG:
            print(traceback.format_exc())
        return {}
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        if DEBUG:
            print(traceback.format_exc())
        return {}

def get_config_value(key: str, default=None) -> any:
    """
    Retrieves a configuration value.

    Args:
        key (str): The key of the configuration value to retrieve.
        default: The default value to return if the key is not found.

    Returns:
        any: The value associated with the given key, or the default value if not found.
    """
    config = load_config("config.json")  # Assuming a default config file name
    try:
        value = config.get(key, default)
        if DEBUG:
            print(f"Retrieved configuration value for key '{key}': {value}")
        return value
    except Exception as e:
        print(f"Error retrieving configuration value for key '{key}': {str(e)}")
        if DEBUG:
            print(traceback.format_exc())
        return default

if DEBUG:
    print("Config module loaded successfully")