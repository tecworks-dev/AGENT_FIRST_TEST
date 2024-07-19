
# app/services/collaboration_service.py
"""
Handles collaboration features for team projects.
This module provides functionality for inviting users to projects,
assigning tasks, and retrieving project activity.
"""

import logging
from typing import Dict, Any, List
from app.models import User, Project, Task
from app import db
import traceback

class CollaborationService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def invite_user(self, project_id: int, user_email: str) -> bool:
        """
        Invites a user to a project.

        Args:
            project_id (int): The ID of the project.
            user_email (str): The email of the user to invite.

        Returns:
            bool: True if the invitation was successful, False otherwise.
        """
        try:
            project = Project.query.get(project_id)
            if not project:
                self.logger.error(f"Project with ID {project_id} not found")
                return False

            user = User.query.filter_by(email=user_email).first()
            if not user:
                self.logger.error(f"User with email {user_email} not found")
                return False

            if user in project.users:
                self.logger.info(f"User {user_email} is already a member of project {project_id}")
                return True

            project.users.append(user)
            db.session.commit()
            self.logger.info(f"User {user_email} invited to project {project_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error inviting user to project: {str(e)}")
            self.logger.error(traceback.format_exc())
            db.session.rollback()
            return False

    def assign_task(self, task_id: int, user_id: int) -> bool:
        """
        Assigns a task to a user.

        Args:
            task_id (int): The ID of the task to assign.
            user_id (int): The ID of the user to assign the task to.

        Returns:
            bool: True if the task was assigned successfully, False otherwise.
        """
        try:
            task = Task.query.get(task_id)
            if not task:
                self.logger.error(f"Task with ID {task_id} not found")
                return False

            user = User.query.get(user_id)
            if not user:
                self.logger.error(f"User with ID {user_id} not found")
                return False

            task.assigned_to = user_id
            db.session.commit()
            self.logger.info(f"Task {task_id} assigned to user {user_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error assigning task: {str(e)}")
            self.logger.error(traceback.format_exc())
            db.session.rollback()
            return False

    def get_project_activity(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Retrieves recent activity for a project.

        Args:
            project_id (int): The ID of the project.

        Returns:
            List[Dict[str, Any]]: A list of recent activities for the project.
        """
        try:
            project = Project.query.get(project_id)
            if not project:
                self.logger.error(f"Project with ID {project_id} not found")
                return []

            activities = []

            # Get recent task updates
            recent_tasks = Task.query.filter_by(project_id=project_id).order_by(Task.updated_at.desc()).limit(10).all()
            for task in recent_tasks:
                activities.append({
                    'type': 'task_update',
                    'task_id': task.id,
                    'task_title': task.title,
                    'status': task.status,
                    'updated_at': task.updated_at
                })

            # Get recent user invitations (assuming we had a ProjectUser join table)
            # This is a placeholder and should be adjusted based on your actual data model
            recent_invitations = db.session.query(User).join(Project.users).filter(Project.id == project_id).order_by(User.created_at.desc()).limit(5).all()
            for user in recent_invitations:
                activities.append({
                    'type': 'user_invited',
                    'user_id': user.id,
                    'user_email': user.email,
                    'invited_at': user.created_at
                })

            # Sort activities by date
            activities.sort(key=lambda x: x.get('updated_at') or x.get('invited_at'), reverse=True)

            return activities

        except Exception as e:
            self.logger.error(f"Error retrieving project activity: {str(e)}")
            self.logger.error(traceback.format_exc())
            return []

if __name__ == "__main__":
    # This block is for testing purposes only
    collaboration_service = CollaborationService()
    
    # Test inviting a user
    invite_result = collaboration_service.invite_user(1, "test@example.com")
    print(f"Invite result: {invite_result}")
    
    # Test assigning a task
    assign_result = collaboration_service.assign_task(1, 1)
    print(f"Assign result: {assign_result}")
    
    # Test getting project activity
    activity = collaboration_service.get_project_activity(1)
    print(f"Project activity: {activity}")
