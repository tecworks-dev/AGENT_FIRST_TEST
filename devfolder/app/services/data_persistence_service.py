
"""
Handles data persistence operations for the AI Software Factory application.

This service provides methods to save and load project states, as well as backup projects.
It interacts with the database to persist and retrieve project-related data.
"""

from typing import Dict, Any
from app.models import Project, db
import json
import os
import datetime
import traceback

class DataPersistenceService:
    def save_project_state(self, project_id: int, state: Dict[str, Any]) -> bool:
        """
        Save the current state of a project to the database.

        Args:
            project_id (int): The ID of the project to save.
            state (Dict[str, Any]): The current state of the project to be saved.

        Returns:
            bool: True if the save operation was successful, False otherwise.
        """
        try:
            project = Project.query.get(project_id)
            if not project:
                raise ValueError(f"Project with id {project_id} not found")

            project.state = json.dumps(state)
            project.updated_at = datetime.datetime.utcnow()
            db.session.commit()

            if __debug__:
                print(f"Project state saved successfully for project_id: {project_id}")

            return True
        except Exception as e:
            if __debug__:
                print(f"Error saving project state for project_id {project_id}: {str(e)}")
                traceback.print_exc()
            return False

    def load_project_state(self, project_id: int) -> Dict[str, Any]:
        """
        Load the current state of a project from the database.

        Args:
            project_id (int): The ID of the project to load.

        Returns:
            Dict[str, Any]: The loaded project state, or an empty dict if not found.
        """
        try:
            project = Project.query.get(project_id)
            if not project:
                raise ValueError(f"Project with id {project_id} not found")

            state = json.loads(project.state) if project.state else {}

            if __debug__:
                print(f"Project state loaded successfully for project_id: {project_id}")

            return state
        except Exception as e:
            if __debug__:
                print(f"Error loading project state for project_id {project_id}: {str(e)}")
                traceback.print_exc()
            return {}

    def backup_project(self, project_id: int) -> str:
        """
        Create a backup of the project's current state.

        Args:
            project_id (int): The ID of the project to backup.

        Returns:
            str: The path to the created backup file, or an empty string if backup failed.
        """
        try:
            project = Project.query.get(project_id)
            if not project:
                raise ValueError(f"Project with id {project_id} not found")

            state = self.load_project_state(project_id)
            
            backup_dir = os.path.join(os.getcwd(), 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"project_{project_id}_backup_{timestamp}.json"
            backup_path = os.path.join(backup_dir, backup_filename)

            with open(backup_path, 'w') as backup_file:
                json.dump(state, backup_file, indent=2)

            if __debug__:
                print(f"Project backup created successfully for project_id: {project_id}")

            return backup_path
        except Exception as e:
            if __debug__:
                print(f"Error creating backup for project_id {project_id}: {str(e)}")
                traceback.print_exc()
            return ""

# Additional helper methods can be added here as needed

if __debug__:
    print("DataPersistenceService module loaded")
