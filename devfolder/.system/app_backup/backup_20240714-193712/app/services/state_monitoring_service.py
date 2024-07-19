
# app/services/state_monitoring_service.py
"""
Handles application state monitoring and project progress tracking.
"""

import traceback
from typing import Dict, Any
from app.models import Project, Task
from app import db

class StateMonitoringService:
    def __init__(self):
        pass

    def get_current_state(self, project_id: int) -> Dict[str, Any]:
        """
        Retrieves the current state of a project.

        Args:
            project_id (int): The ID of the project to get the state for.

        Returns:
            Dict[str, Any]: A dictionary containing the current state of the project.
        """
        try:
            project = Project.query.get(project_id)
            if not project:
                return {"error": "Project not found"}

            tasks = Task.query.filter_by(project_id=project_id).all()
            
            state = {
                "project_id": project.id,
                "project_name": project.name,
                "project_description": project.description,
                "tasks_total": len(tasks),
                "tasks_completed": sum(1 for task in tasks if task.status == "completed"),
                "tasks_in_progress": sum(1 for task in tasks if task.status == "in_progress"),
                "tasks_pending": sum(1 for task in tasks if task.status == "pending"),
            }

            if __debug__:
                print(f"Current state for project {project_id}: {state}")

            return state
        except Exception as e:
            error_msg = f"Error getting current state for project {project_id}: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return {"error": error_msg}

    def update_state(self, project_id: int, new_state: Dict[str, Any]) -> bool:
        """
        Updates the state of a project.

        Args:
            project_id (int): The ID of the project to update.
            new_state (Dict[str, Any]): A dictionary containing the new state information.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            project = Project.query.get(project_id)
            if not project:
                return False

            if "project_name" in new_state:
                project.name = new_state["project_name"]
            if "project_description" in new_state:
                project.description = new_state["project_description"]

            db.session.commit()

            if __debug__:
                print(f"Updated state for project {project_id}: {new_state}")

            return True
        except Exception as e:
            error_msg = f"Error updating state for project {project_id}: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return False

    def track_progress(self, project_id: int) -> float:
        """
        Calculates and returns the progress of a project.

        Args:
            project_id (int): The ID of the project to track progress for.

        Returns:
            float: The progress of the project as a percentage (0-100).
        """
        try:
            tasks = Task.query.filter_by(project_id=project_id).all()
            if not tasks:
                return 0.0

            total_tasks = len(tasks)
            completed_tasks = sum(1 for task in tasks if task.status == "completed")

            progress = (completed_tasks / total_tasks) * 100

            if __debug__:
                print(f"Progress for project {project_id}: {progress:.2f}%")

            return round(progress, 2)
        except Exception as e:
            error_msg = f"Error tracking progress for project {project_id}: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return 0.0

if __name__ == "__main__":
    # This block is for testing purposes only
    service = StateMonitoringService()
    test_project_id = 1  # Replace with a valid project ID for testing
    
    print("Testing get_current_state:")
    print(service.get_current_state(test_project_id))
    
    print("\nTesting update_state:")
    new_state = {"project_name": "Updated Project Name"}
    print(service.update_state(test_project_id, new_state))
    
    print("\nTesting track_progress:")
    print(service.track_progress(test_project_id))
