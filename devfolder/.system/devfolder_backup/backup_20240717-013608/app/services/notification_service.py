
# app/services/notification_service.py
"""
Manages user notifications and alerts.

This service handles the creation, retrieval, and management of user notifications
within the AI Software Factory application.
"""

from typing import List, Dict, Any
from app.models import User, db
from datetime import datetime
import logging

class NotificationService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def send_notification(self, user_id: int, message: str) -> bool:
        """
        Sends a notification to a specific user.

        Args:
            user_id (int): The ID of the user to receive the notification.
            message (str): The content of the notification.

        Returns:
            bool: True if the notification was sent successfully, False otherwise.
        """
        try:
            user = User.query.get(user_id)
            if not user:
                self.logger.warning(f"User with ID {user_id} not found.")
                return False

            notification = Notification(user_id=user_id, message=message)
            db.session.add(notification)
            db.session.commit()

            self.logger.info(f"Notification sent to user {user_id}: {message}")
            return True
        except Exception as e:
            self.logger.error(f"Error sending notification: {str(e)}")
            db.session.rollback()
            return False

    def get_user_notifications(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Retrieves all notifications for a specific user.

        Args:
            user_id (int): The ID of the user whose notifications to retrieve.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing notification details.
        """
        try:
            user = User.query.get(user_id)
            if not user:
                self.logger.warning(f"User with ID {user_id} not found.")
                return []

            notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
            return [notification.to_dict() for notification in notifications]
        except Exception as e:
            self.logger.error(f"Error retrieving notifications: {str(e)}")
            return []

    def mark_notification_as_read(self, notification_id: int) -> bool:
        """
        Marks a specific notification as read.

        Args:
            notification_id (int): The ID of the notification to mark as read.

        Returns:
            bool: True if the notification was marked as read successfully, False otherwise.
        """
        try:
            notification = Notification.query.get(notification_id)
            if not notification:
                self.logger.warning(f"Notification with ID {notification_id} not found.")
                return False

            notification.read = True
            notification.read_at = datetime.utcnow()
            db.session.commit()

            self.logger.info(f"Notification {notification_id} marked as read.")
            return True
        except Exception as e:
            self.logger.error(f"Error marking notification as read: {str(e)}")
            db.session.rollback()
            return False

    def delete_notification(self, notification_id: int) -> bool:
        """
        Deletes a specific notification.

        Args:
            notification_id (int): The ID of the notification to delete.

        Returns:
            bool: True if the notification was deleted successfully, False otherwise.
        """
        try:
            notification = Notification.query.get(notification_id)
            if not notification:
                self.logger.warning(f"Notification with ID {notification_id} not found.")
                return False

            db.session.delete(notification)
            db.session.commit()

            self.logger.info(f"Notification {notification_id} deleted.")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting notification: {str(e)}")
            db.session.rollback()
            return False

class Notification(db.Model):
    """
    Represents a notification in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the notification to a dictionary representation.

        Returns:
            Dict[str, Any]: A dictionary containing the notification details.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'read': self.read,
            'created_at': self.created_at.isoformat(),
            'read_at': self.read_at.isoformat() if self.read_at else None
        }

# Debugging statements
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.debug("NotificationService module loaded.")
