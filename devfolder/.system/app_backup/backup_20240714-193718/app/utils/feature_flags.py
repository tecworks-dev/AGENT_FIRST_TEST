
"""
Purpose: Implements feature flag functionality for the application.
Description: This module provides a centralized way to manage feature flags,
allowing for easy enabling/disabling of features across the application.
"""

from typing import Dict, Any
import logging
import traceback

DEBUG = True

class FeatureFlags:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the FeatureFlags class with a configuration dictionary.

        Args:
            config (Dict[str, Any]): A dictionary containing feature flag configurations.
        """
        self.flags = config
        if DEBUG:
            print(f"Initialized FeatureFlags with config: {self.flags}")

    def is_enabled(self, feature_name: str) -> bool:
        """
        Checks if a feature is enabled.

        Args:
            feature_name (str): The name of the feature to check.

        Returns:
            bool: True if the feature is enabled, False otherwise.
        """
        try:
            enabled = self.flags.get(feature_name, False)
            if DEBUG:
                print(f"Checking feature '{feature_name}': {'enabled' if enabled else 'disabled'}")
            return enabled
        except Exception as e:
            logging.error(f"Error checking feature '{feature_name}': {str(e)}")
            logging.error(traceback.format_exc())
            return False

    def enable_feature(self, feature_name: str) -> None:
        """
        Enables a feature.

        Args:
            feature_name (str): The name of the feature to enable.
        """
        try:
            self.flags[feature_name] = True
            if DEBUG:
                print(f"Enabled feature: {feature_name}")
        except Exception as e:
            logging.error(f"Error enabling feature '{feature_name}': {str(e)}")
            logging.error(traceback.format_exc())

    def disable_feature(self, feature_name: str) -> None:
        """
        Disables a feature.

        Args:
            feature_name (str): The name of the feature to disable.
        """
        try:
            self.flags[feature_name] = False
            if DEBUG:
                print(f"Disabled feature: {feature_name}")
        except Exception as e:
            logging.error(f"Error disabling feature '{feature_name}': {str(e)}")
            logging.error(traceback.format_exc())

    def get_all_flags(self) -> Dict[str, bool]:
        """
        Returns the status of all feature flags.

        Returns:
            Dict[str, bool]: A dictionary containing all feature flags and their statuses.
        """
        try:
            if DEBUG:
                print(f"Returning all feature flags: {self.flags}")
            return self.flags.copy()
        except Exception as e:
            logging.error(f"Error getting all feature flags: {str(e)}")
            logging.error(traceback.format_exc())
            return {}

# Example usage
if __name__ == "__main__":
    config = {
        "new_ui": True,
        "advanced_search": False,
        "ai_recommendations": True
    }
    feature_flags = FeatureFlags(config)

    print(feature_flags.is_enabled("new_ui"))  # True
    print(feature_flags.is_enabled("advanced_search"))  # False

    feature_flags.enable_feature("advanced_search")
    print(feature_flags.is_enabled("advanced_search"))  # True

    feature_flags.disable_feature("ai_recommendations")
    print(feature_flags.is_enabled("ai_recommendations"))  # False

    print(feature_flags.get_all_flags())
    # {'new_ui': True, 'advanced_search': True, 'ai_recommendations': False}
