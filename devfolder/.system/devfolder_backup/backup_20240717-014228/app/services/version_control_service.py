
# app/services/version_control_service.py
"""
Handles version control operations.

This module provides a service for managing version control operations
within the AI Software Factory application. It uses the 'git' package
to interact with Git repositories.
"""

from typing import Dict, Any
import git
import os
import traceback

DEBUG = True

class VersionControlService:
    def __init__(self):
        self.repo = None

    def init_repository(self, project_path: str) -> bool:
        """
        Initialize a new Git repository for the project.

        Args:
            project_path (str): The path to the project directory.

        Returns:
            bool: True if the repository was successfully initialized, False otherwise.
        """
        try:
            if not os.path.exists(project_path):
                os.makedirs(project_path)
            
            self.repo = git.Repo.init(project_path)
            if DEBUG:
                print(f"Initialized Git repository at {project_path}")
            return True
        except Exception as e:
            if DEBUG:
                print(f"Error initializing Git repository: {str(e)}")
                print(traceback.format_exc())
            return False

    def commit_changes(self, project_path: str, commit_message: str) -> bool:
        """
        Commit changes to the Git repository.

        Args:
            project_path (str): The path to the project directory.
            commit_message (str): The commit message.

        Returns:
            bool: True if the changes were successfully committed, False otherwise.
        """
        try:
            if self.repo is None:
                self.repo = git.Repo(project_path)
            
            # Add all changes
            self.repo.git.add(A=True)
            
            # Commit changes
            self.repo.index.commit(commit_message)
            
            if DEBUG:
                print(f"Committed changes with message: {commit_message}")
            return True
        except Exception as e:
            if DEBUG:
                print(f"Error committing changes: {str(e)}")
                print(traceback.format_exc())
            return False

    def create_branch(self, project_path: str, branch_name: str) -> bool:
        """
        Create a new branch in the Git repository.

        Args:
            project_path (str): The path to the project directory.
            branch_name (str): The name of the new branch.

        Returns:
            bool: True if the branch was successfully created, False otherwise.
        """
        try:
            if self.repo is None:
                self.repo = git.Repo(project_path)
            
            # Create and checkout the new branch
            new_branch = self.repo.create_head(branch_name)
            new_branch.checkout()
            
            if DEBUG:
                print(f"Created and checked out new branch: {branch_name}")
            return True
        except Exception as e:
            if DEBUG:
                print(f"Error creating branch: {str(e)}")
                print(traceback.format_exc())
            return False

    def list_branches(self, project_path: str) -> List[str]:
        """
        List all branches in the Git repository.

        Args:
            project_path (str): The path to the project directory.

        Returns:
            List[str]: A list of branch names.
        """
        try:
            if self.repo is None:
                self.repo = git.Repo(project_path)
            
            branches = [branch.name for branch in self.repo.branches]
            
            if DEBUG:
                print(f"Branches in repository: {', '.join(branches)}")
            return branches
        except Exception as e:
            if DEBUG:
                print(f"Error listing branches: {str(e)}")
                print(traceback.format_exc())
            return []

    def get_current_branch(self, project_path: str) -> str:
        """
        Get the name of the current branch.

        Args:
            project_path (str): The path to the project directory.

        Returns:
            str: The name of the current branch.
        """
        try:
            if self.repo is None:
                self.repo = git.Repo(project_path)
            
            current_branch = self.repo.active_branch.name
            
            if DEBUG:
                print(f"Current branch: {current_branch}")
            return current_branch
        except Exception as e:
            if DEBUG:
                print(f"Error getting current branch: {str(e)}")
                print(traceback.format_exc())
            return ""

    def switch_branch(self, project_path: str, branch_name: str) -> bool:
        """
        Switch to a different branch.

        Args:
            project_path (str): The path to the project directory.
            branch_name (str): The name of the branch to switch to.

        Returns:
            bool: True if successfully switched to the branch, False otherwise.
        """
        try:
            if self.repo is None:
                self.repo = git.Repo(project_path)
            
            self.repo.git.checkout(branch_name)
            
            if DEBUG:
                print(f"Switched to branch: {branch_name}")
            return True
        except Exception as e:
            if DEBUG:
                print(f"Error switching branch: {str(e)}")
                print(traceback.format_exc())
            return False

if __name__ == "__main__":
    # Example usage
    vcs = VersionControlService()
    project_path = "./example_project"
    
    # Initialize repository
    vcs.init_repository(project_path)
    
    # Commit changes
    vcs.commit_changes(project_path, "Initial commit")
    
    # Create a new branch
    vcs.create_branch(project_path, "feature-branch")
    
    # List branches
    branches = vcs.list_branches(project_path)
    print(f"Branches: {branches}")
    
    # Get current branch
    current_branch = vcs.get_current_branch(project_path)
    print(f"Current branch: {current_branch}")
    
    # Switch branch
    vcs.switch_branch(project_path, "master")
