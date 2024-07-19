
"""
Handles project export and import functionality.

This module provides services for exporting project data to a portable format
and importing project data from previously exported files.
"""

from typing import Dict, Any
import json
from app.models import Project, Task, File
from app import db
import io
import zipfile


class ProjectExportService:
    def export_project(self, project_id: int) -> bytes:
        """
        Exports a project and all its associated data to a zip file.

        Args:
            project_id (int): The ID of the project to export.

        Returns:
            bytes: The exported project data as a zip file in bytes.

        Raises:
            ValueError: If the project with the given ID doesn't exist.
        """
        project = Project.query.get(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found.")

        project_data = {
            'project': project.to_dict(),
            'tasks': [task.to_dict() for task in Task.query.filter_by(project_id=project_id).all()],
            'files': [file.to_dict() for file in File.query.filter_by(project_id=project_id).all()]
        }

        # Create a zip file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add project data as JSON
            zip_file.writestr('project_data.json', json.dumps(project_data, indent=2))

            # Add file contents
            for file in File.query.filter_by(project_id=project_id).all():
                zip_file.writestr(f'files/{file.name}', file.content)

        zip_buffer.seek(0)
        return zip_buffer.getvalue()

    def import_project(self, project_data: bytes) -> int:
        """
        Imports a project from exported data.

        Args:
            project_data (bytes): The exported project data as a zip file in bytes.

        Returns:
            int: The ID of the newly imported project.

        Raises:
            ValueError: If the import data is invalid or corrupt.
        """
        try:
            zip_buffer = io.BytesIO(project_data)
            with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
                # Read project data JSON
                project_json = zip_file.read('project_data.json').decode('utf-8')
                project_data = json.loads(project_json)

                # Create new project
                new_project = Project(
                    name=project_data['project']['name'],
                    description=project_data['project']['description'],
                    user_id=project_data['project']['user_id']
                )
                db.session.add(new_project)
                db.session.flush()  # Get the new project ID

                # Import tasks
                for task_data in project_data['tasks']:
                    new_task = Task(
                        title=task_data['title'],
                        description=task_data['description'],
                        status=task_data['status'],
                        project_id=new_project.id
                    )
                    db.session.add(new_task)

                # Import files
                for file_data in project_data['files']:
                    file_content = zip_file.read(f"files/{file_data['name']}").decode('utf-8')
                    new_file = File(
                        name=file_data['name'],
                        content=file_content,
                        project_id=new_project.id
                    )
                    db.session.add(new_file)

                db.session.commit()
                return new_project.id

        except (json.JSONDecodeError, KeyError, zipfile.BadZipFile) as e:
            db.session.rollback()
            raise ValueError(f"Invalid or corrupt import data: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error during import: {str(e)}")

    def list_exportable_projects(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Lists all projects that a user can export.

        Args:
            user_id (int): The ID of the user.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing project information.
        """
        projects = Project.query.filter_by(user_id=user_id).all()
        return [{'id': project.id, 'name': project.name} for project in projects]

    def get_project_export_summary(self, project_id: int) -> Dict[str, Any]:
        """
        Generates a summary of what will be exported for a given project.

        Args:
            project_id (int): The ID of the project.

        Returns:
            Dict[str, Any]: A dictionary containing the export summary.

        Raises:
            ValueError: If the project with the given ID doesn't exist.
        """
        project = Project.query.get(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found.")

        tasks_count = Task.query.filter_by(project_id=project_id).count()
        files_count = File.query.filter_by(project_id=project_id).count()

        return {
            'project_name': project.name,
            'tasks_count': tasks_count,
            'files_count': files_count,
        }


# Debugging statements
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    try:
        service = ProjectExportService()
        
        # Example usage
        project_id = 1  # Assuming a project with ID 1 exists
        export_data = service.export_project(project_id)
        logger.debug(f"Exported project data size: {len(export_data)} bytes")

        imported_project_id = service.import_project(export_data)
        logger.debug(f"Imported project ID: {imported_project_id}")

        exportable_projects = service.list_exportable_projects(user_id=1)  # Assuming user with ID 1
        logger.debug(f"Exportable projects: {exportable_projects}")

        export_summary = service.get_project_export_summary(project_id)
        logger.debug(f"Export summary: {export_summary}")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
