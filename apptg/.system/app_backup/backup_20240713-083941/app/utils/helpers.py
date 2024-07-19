
# Purpose: Helper functions used across the application
# Description: This file contains utility functions that are used throughout the application
# to perform common tasks such as generating unique identifiers and formatting timestamps.

import uuid
from datetime import datetime
import traceback

DEBUG = True

def generate_unique_id():
    """
    Generates a unique identifier using UUID.

    Returns:
        str: A unique identifier string.
    """
    try:
        if DEBUG:
            print("Generating unique ID...")
        return str(uuid.uuid4())
    except Exception as e:
        print(f"Error generating unique ID: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        return None

def format_timestamp(timestamp):
    """
    Formats a timestamp for display.

    Args:
        timestamp (datetime): The timestamp to format.

    Returns:
        str: A formatted string representation of the timestamp.
    """
    try:
        if DEBUG:
            print(f"Formatting timestamp: {timestamp}")
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Error formatting timestamp: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        return None

# Additional helper functions can be added here as needed

if __name__ == "__main__":
    import unittest

    class TestHelperFunctions(unittest.TestCase):
        def test_generate_unique_id(self):
            id1 = generate_unique_id()
            id2 = generate_unique_id()
            self.assertIsNotNone(id1)
            self.assertIsNotNone(id2)
            self.assertNotEqual(id1, id2)

        def test_format_timestamp(self):
            test_timestamp = datetime(2023, 5, 1, 12, 30, 45)
            formatted = format_timestamp(test_timestamp)
            self.assertEqual(formatted, "2023-05-01 12:30:45")

    unittest.main()
