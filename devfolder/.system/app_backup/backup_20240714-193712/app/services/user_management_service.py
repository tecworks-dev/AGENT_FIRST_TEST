
# Purpose: Handles user-related operations.
# Description: This service provides methods for creating, updating, deleting users,
# and retrieving user projects.

from typing import List
from app.models import User, Project
from app import db
import logging
import traceback

class UserManagementService:
    def create_user(self, username: str, email: str, password: str) -> User:
        """
        Create a new user.

        Args:
            username (str): The username for the new user.
            email (str): The email address for the new user.
            password (str): The password for the new user.

        Returns:
            User: The newly created user object.

        Raises:
            ValueError: If the username or email already exists.
        """
        try:
            if User.query.filter_by(username=username).first():
                raise ValueError("Username already exists")
            if User.query.filter_by(email=email).first():
                raise ValueError("Email already exists")
            
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            logging.info(f"User created: {username}")
            return new_user
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating user: {str(e)}")
            logging.debug(traceback.format_exc())
            raise

    def update_user(self, user_id: int, **kwargs) -> User:
        """
        Update user information.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments for updating user attributes.

        Returns:
            User: The updated user object.

        Raises:
            ValueError: If the user is not found.
        """
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            db.session.commit()
            logging.info(f"User updated: {user.username}")
            return user
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating user: {str(e)}")
            logging.debug(traceback.format_exc())
            raise

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if the user was successfully deleted, False otherwise.

        Raises:
            ValueError: If the user is not found.
        """
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            db.session.delete(user)
            db.session.commit()
            logging.info(f"User deleted: {user.username}")
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting user: {str(e)}")
            logging.debug(traceback.format_exc())
            raise

    def get_user_projects(self, user_id: int) -> List[Project]:
        """
        Retrieve all projects associated with a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            List[Project]: A list of Project objects associated with the user.

        Raises:
            ValueError: If the user is not found.
        """
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            projects = Project.query.filter_by(user_id=user_id).all()
            logging.info(f"Retrieved {len(projects)} projects for user: {user.username}")
            return projects
        except Exception as e:
            logging.error(f"Error retrieving user projects: {str(e)}")
            logging.debug(traceback.format_exc())
            raise

# Debugging statements
if __name__ == "__main__":
    import os
    if os.environ.get("DEBUG") == "True":
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("UserManagementService debugging is enabled")
    else:
        logging.basicConfig(level=logging.INFO)
