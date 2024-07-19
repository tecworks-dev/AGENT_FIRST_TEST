
"""
This module handles push notifications for real-time updates in the application.
It uses Firebase Cloud Messaging (FCM) to send notifications to clients.
"""

import firebase_admin
from firebase_admin import messaging
import traceback
import logging

# Initialize Firebase Admin SDK
try:
    firebase_admin.initialize_app()
except ValueError:
    # App already initialized
    pass

# Set up logging
logger = logging.getLogger(__name__)

# Debug flag
DEBUG = True

def send_notification(token, title, body):
    """
    Sends a push notification to a specific device using FCM.

    Args:
    token (str): The FCM registration token of the target device.
    title (str): The title of the notification.
    body (str): The body text of the notification.

    Returns:
    bool: True if the notification was sent successfully, False otherwise.
    """
    try:
        if DEBUG:
            print(f"Attempting to send notification - Token: {token}, Title: {title}, Body: {body}")

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )

        response = messaging.send(message)

        if DEBUG:
            print(f"Successfully sent message: {response}")

        return True

    except Exception as e:
        logger.error(f"Error sending push notification: {str(e)}")
        if DEBUG:
            print(f"Error sending push notification: {str(e)}")
            print(traceback.format_exc())
        return False

def send_multicast_notification(tokens, title, body):
    """
    Sends a push notification to multiple devices using FCM.

    Args:
    tokens (list): A list of FCM registration tokens of the target devices.
    title (str): The title of the notification.
    body (str): The body text of the notification.

    Returns:
    dict: A dictionary containing the number of successful and failed messages.
    """
    try:
        if DEBUG:
            print(f"Attempting to send multicast notification - Tokens: {tokens}, Title: {title}, Body: {body}")

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            tokens=tokens,
        )

        response = messaging.send_multicast(message)

        if DEBUG:
            print(f"Multicast message sent. Success: {response.success_count}, Failure: {response.failure_count}")

        return {
            "success_count": response.success_count,
            "failure_count": response.failure_count
        }

    except Exception as e:
        logger.error(f"Error sending multicast push notification: {str(e)}")
        if DEBUG:
            print(f"Error sending multicast push notification: {str(e)}")
            print(traceback.format_exc())
        return {
            "success_count": 0,
            "failure_count": len(tokens)
        }

# Unit tests
import unittest

class TestPushNotifications(unittest.TestCase):
    def test_send_notification(self):
        # Mock FCM token (replace with a valid token for actual testing)
        token = "mock_fcm_token"
        result = send_notification(token, "Test Title", "Test Body")
        self.assertTrue(result)

    def test_send_multicast_notification(self):
        # Mock FCM tokens (replace with valid tokens for actual testing)
        tokens = ["mock_token1", "mock_token2", "mock_token3"]
        result = send_multicast_notification(tokens, "Test Multicast", "Test Body")
        self.assertIsInstance(result, dict)
        self.assertIn("success_count", result)
        self.assertIn("failure_count", result)

if __name__ == "__main__":
    unittest.main()
