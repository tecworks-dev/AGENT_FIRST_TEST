
# app/services/deployment_service.py

"""
Handles deployment tasks for the AI Software Factory application.

This module provides a DeploymentService class that manages the deployment
of projects to different environments and allows for rollback to previous versions.
"""

import os
import shutil
import subprocess
import logging
from typing import Dict, Any
from datetime import datetime
from app.models import Project, Deployment
from app.utils.error_handler import handle_error
from app.services.version_control_service import VersionControlService

class DeploymentService:
    def __init__(self):
        self.vcs = VersionControlService()
        self.logger = logging.getLogger(__name__)

    def deploy_to_environment(self, project_path: str, environment: str) -> bool:
        """
        Deploy the project to the specified environment.

        Args:
            project_path (str): The path to the project to be deployed.
            environment (str): The target environment (e.g., 'production', 'staging').

        Returns:
            bool: True if deployment was successful, False otherwise.
        """
        try:
            # Validate input
            if not os.path.exists(project_path):
                raise ValueError(f"Project path does not exist: {project_path}")
            if environment not in ['production', 'staging', 'development']:
                raise ValueError(f"Invalid environment: {environment}")

            # Get the current version from version control
            current_version = self.vcs.get_current_version(project_path)

            # Perform deployment steps
            deployment_successful = self._perform_deployment(project_path, environment, current_version)

            if deployment_successful:
                # Update deployment record in the database
                self._update_deployment_record(project_path, environment, current_version)
                self.logger.info(f"Deployment to {environment} successful. Version: {current_version}")
                return True
            else:
                self.logger.error(f"Deployment to {environment} failed. Version: {current_version}")
                return False

        except Exception as e:
            handle_error(e, f"Error during deployment to {environment}")
            return False

    def rollback_deployment(self, project_path: str, environment: str, version: str) -> bool:
        """
        Rollback the deployment to a specific version.

        Args:
            project_path (str): The path to the project.
            environment (str): The environment to rollback.
            version (str): The version to rollback to.

        Returns:
            bool: True if rollback was successful, False otherwise.
        """
        try:
            # Validate input
            if not os.path.exists(project_path):
                raise ValueError(f"Project path does not exist: {project_path}")
            if environment not in ['production', 'staging', 'development']:
                raise ValueError(f"Invalid environment: {environment}")

            # Check if the version exists
            if not self.vcs.version_exists(project_path, version):
                raise ValueError(f"Version does not exist: {version}")

            # Perform rollback steps
            rollback_successful = self._perform_rollback(project_path, environment, version)

            if rollback_successful:
                # Update deployment record in the database
                self._update_deployment_record(project_path, environment, version, is_rollback=True)
                self.logger.info(f"Rollback to version {version} in {environment} successful.")
                return True
            else:
                self.logger.error(f"Rollback to version {version} in {environment} failed.")
                return False

        except Exception as e:
            handle_error(e, f"Error during rollback to version {version} in {environment}")
            return False

    def _perform_deployment(self, project_path: str, environment: str, version: str) -> bool:
        """
        Perform the actual deployment steps.

        This method should be extended with actual deployment logic, such as:
        - Copying files to the deployment server
        - Updating configurations
        - Restarting services
        """
        try:
            # Simulated deployment steps
            deployment_dir = f"/var/www/{environment}/{os.path.basename(project_path)}"
            os.makedirs(deployment_dir, exist_ok=True)
            shutil.copytree(project_path, deployment_dir, dirs_exist_ok=True)

            # Run any necessary deployment scripts
            subprocess.run(["./deploy.sh", environment], cwd=deployment_dir, check=True)

            return True
        except Exception as e:
            self.logger.error(f"Deployment failed: {str(e)}")
            return False

    def _perform_rollback(self, project_path: str, environment: str, version: str) -> bool:
        """
        Perform the actual rollback steps.

        This method should be extended with actual rollback logic, such as:
        - Restoring files from the specified version
        - Updating configurations to match the old version
        - Restarting services
        """
        try:
            # Simulated rollback steps
            deployment_dir = f"/var/www/{environment}/{os.path.basename(project_path)}"
            backup_dir = f"{deployment_dir}_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}"

            # Backup current version
            shutil.copytree(deployment_dir, backup_dir)

            # Checkout the specified version
            self.vcs.checkout_version(project_path, version)

            # Copy the old version to the deployment directory
            shutil.copytree(project_path, deployment_dir, dirs_exist_ok=True)

            # Run any necessary rollback scripts
            subprocess.run(["./rollback.sh", environment, version], cwd=deployment_dir, check=True)

            return True
        except Exception as e:
            self.logger.error(f"Rollback failed: {str(e)}")
            return False

    def _update_deployment_record(self, project_path: str, environment: str, version: str, is_rollback: bool = False) -> None:
        """
        Update the deployment record in the database.
        """
        project = Project.query.filter_by(path=project_path).first()
        if project:
            deployment = Deployment(
                project_id=project.id,
                environment=environment,
                version=version,
                status='completed',
                is_rollback=is_rollback
            )
            db.session.add(deployment)
            db.session.commit()

if __name__ == "__main__":
    # This block is for testing purposes only
    deployment_service = DeploymentService()
    
    # Test deployment
    test_project_path = "/path/to/test/project"
    test_environment = "staging"
    
    if deployment_service.deploy_to_environment(test_project_path, test_environment):
        print(f"Deployment to {test_environment} successful")
    else:
        print(f"Deployment to {test_environment} failed")
    
    # Test rollback
    test_version = "v1.0.0"
    if deployment_service.rollback_deployment(test_project_path, test_environment, test_version):
        print(f"Rollback to version {test_version} successful")
    else:
        print(f"Rollback to version {test_version} failed")
