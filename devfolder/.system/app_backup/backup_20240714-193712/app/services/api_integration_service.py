
"""
Manages integrations with external APIs.

This module provides functionality to add, remove, and list API integrations
for projects within the AI Software Factory application.
"""

from typing import List, Dict
from app.models import Project, APIIntegration
from app import db
import traceback

class APIIntegrationService:
    """
    Service class for managing API integrations.
    """

    def add_api_integration(self, project_id: int, api_name: str, api_key: str) -> bool:
        """
        Adds a new API integration to a project.

        Args:
            project_id (int): The ID of the project to add the integration to.
            api_name (str): The name of the API being integrated.
            api_key (str): The API key for authentication.

        Returns:
            bool: True if the integration was added successfully, False otherwise.
        """
        try:
            project = Project.query.get(project_id)
            if not project:
                raise ValueError(f"Project with ID {project_id} not found.")

            new_integration = APIIntegration(
                project_id=project_id,
                api_name=api_name,
                api_key=api_key
            )
            db.session.add(new_integration)
            db.session.commit()
            
            if __debug__:
                print(f"Added API integration: {api_name} for project {project_id}")
            
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error adding API integration: {str(e)}")
            traceback.print_exc()
            return False

    def remove_api_integration(self, project_id: int, api_name: str) -> bool:
        """
        Removes an API integration from a project.

        Args:
            project_id (int): The ID of the project to remove the integration from.
            api_name (str): The name of the API integration to remove.

        Returns:
            bool: True if the integration was removed successfully, False otherwise.
        """
        try:
            integration = APIIntegration.query.filter_by(
                project_id=project_id, api_name=api_name
            ).first()
            
            if not integration:
                raise ValueError(f"API integration {api_name} not found for project {project_id}.")

            db.session.delete(integration)
            db.session.commit()
            
            if __debug__:
                print(f"Removed API integration: {api_name} from project {project_id}")
            
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error removing API integration: {str(e)}")
            traceback.print_exc()
            return False

    def list_project_integrations(self, project_id: int) -> List[Dict[str, str]]:
        """
        Lists all API integrations for a given project.

        Args:
            project_id (int): The ID of the project to list integrations for.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing API integration details.
        """
        try:
            integrations = APIIntegration.query.filter_by(project_id=project_id).all()
            
            if __debug__:
                print(f"Listing API integrations for project {project_id}")
            
            return [
                {"api_name": integration.api_name, "api_key": integration.api_key}
                for integration in integrations
            ]
        except Exception as e:
            print(f"Error listing API integrations: {str(e)}")
            traceback.print_exc()
            return []

# Add any additional helper methods or functionality as needed

if __debug__:
    print("APIIntegrationService module loaded.")
