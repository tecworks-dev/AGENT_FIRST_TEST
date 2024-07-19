
# app/services/dependency_management_service.py

"""
This module handles dependency management tasks for the AI Software Factory.
It provides functionality to analyze, update, and resolve conflicts in project dependencies.
"""

import os
import json
import subprocess
from typing import Dict, List
import traceback

import pkg_resources
from packaging import version

class DependencyManagementService:
    def __init__(self):
        self.debug = True  # Set to True by default for debugging

    def analyze_dependencies(self, project_path: str) -> Dict[str, str]:
        """
        Analyzes the dependencies of a project and returns a dictionary of package names and versions.

        Args:
            project_path (str): The path to the project directory.

        Returns:
            Dict[str, str]: A dictionary of package names and their versions.
        """
        try:
            if self.debug:
                print(f"Analyzing dependencies for project at: {project_path}")

            requirements_file = os.path.join(project_path, 'requirements.txt')
            if not os.path.exists(requirements_file):
                raise FileNotFoundError(f"requirements.txt not found in {project_path}")

            dependencies = {}
            with open(requirements_file, 'r') as f:
                for line in f:
                    if '==' in line:
                        package, version = line.strip().split('==')
                        dependencies[package] = version

            if self.debug:
                print(f"Dependencies found: {dependencies}")

            return dependencies
        except Exception as e:
            print(f"Error analyzing dependencies: {str(e)}")
            if self.debug:
                traceback.print_exc()
            return {}

    def update_dependencies(self, project_path: str) -> Dict[str, str]:
        """
        Updates the dependencies of a project to their latest versions.

        Args:
            project_path (str): The path to the project directory.

        Returns:
            Dict[str, str]: A dictionary of updated package names and their new versions.
        """
        try:
            if self.debug:
                print(f"Updating dependencies for project at: {project_path}")

            current_deps = self.analyze_dependencies(project_path)
            updated_deps = {}

            for package, current_version in current_deps.items():
                latest_version = self._get_latest_version(package)
                if latest_version != current_version:
                    updated_deps[package] = latest_version

            if updated_deps:
                self._update_requirements_file(project_path, updated_deps)

            if self.debug:
                print(f"Updated dependencies: {updated_deps}")

            return updated_deps
        except Exception as e:
            print(f"Error updating dependencies: {str(e)}")
            if self.debug:
                traceback.print_exc()
            return {}

    def resolve_conflicts(self, project_path: str, conflicts: List[str]) -> bool:
        """
        Attempts to resolve conflicts between dependencies.

        Args:
            project_path (str): The path to the project directory.
            conflicts (List[str]): A list of conflicting package names.

        Returns:
            bool: True if conflicts were resolved successfully, False otherwise.
        """
        try:
            if self.debug:
                print(f"Resolving conflicts for project at: {project_path}")
                print(f"Conflicts to resolve: {conflicts}")

            current_deps = self.analyze_dependencies(project_path)
            resolved_deps = {}

            for package in conflicts:
                if package in current_deps:
                    latest_compatible_version = self._find_compatible_version(package, current_deps)
                    if latest_compatible_version:
                        resolved_deps[package] = latest_compatible_version

            if resolved_deps:
                self._update_requirements_file(project_path, resolved_deps)
                if self.debug:
                    print(f"Resolved dependencies: {resolved_deps}")
                return True
            else:
                if self.debug:
                    print("Unable to resolve conflicts automatically.")
                return False
        except Exception as e:
            print(f"Error resolving conflicts: {str(e)}")
            if self.debug:
                traceback.print_exc()
            return False

    def _get_latest_version(self, package: str) -> str:
        """
        Gets the latest version of a package from PyPI.

        Args:
            package (str): The name of the package.

        Returns:
            str: The latest version of the package.
        """
        try:
            cmd = f"pip index versions {package}"
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            versions = result.stdout.strip().split('\n')[1:]  # Skip the header
            return versions[0].split()[0]  # Return the first (latest) version
        except subprocess.CalledProcessError:
            return ""

    def _find_compatible_version(self, package: str, current_deps: Dict[str, str]) -> str:
        """
        Finds a compatible version of a package that doesn't conflict with other dependencies.

        Args:
            package (str): The name of the package.
            current_deps (Dict[str, str]): The current dependencies of the project.

        Returns:
            str: A compatible version of the package, or an empty string if not found.
        """
        try:
            cmd = f"pip index versions {package}"
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            versions = result.stdout.strip().split('\n')[1:]  # Skip the header

            for ver in versions:
                version_str = ver.split()[0]
                if self._is_compatible(package, version_str, current_deps):
                    return version_str
            return ""
        except subprocess.CalledProcessError:
            return ""

    def _is_compatible(self, package: str, version_str: str, current_deps: Dict[str, str]) -> bool:
        """
        Checks if a specific version of a package is compatible with the current dependencies.

        Args:
            package (str): The name of the package.
            version_str (str): The version to check.
            current_deps (Dict[str, str]): The current dependencies of the project.

        Returns:
            bool: True if the version is compatible, False otherwise.
        """
        try:
            dist = pkg_resources.get_distribution(f"{package}=={version_str}")
            for dep in dist.requires():
                if dep.key in current_deps:
                    if not version.parse(current_deps[dep.key]) in dep.specifier:
                        return False
            return True
        except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
            return False

    def _update_requirements_file(self, project_path: str, updated_deps: Dict[str, str]) -> None:
        """
        Updates the requirements.txt file with new package versions.

        Args:
            project_path (str): The path to the project directory.
            updated_deps (Dict[str, str]): A dictionary of package names and their new versions.
        """
        requirements_file = os.path.join(project_path, 'requirements.txt')
        with open(requirements_file, 'r') as f:
            lines = f.readlines()

        with open(requirements_file, 'w') as f:
            for line in lines:
                package = line.split('==')[0]
                if package in updated_deps:
                    f.write(f"{package}=={updated_deps[package]}\n")
                else:
                    f.write(line)

        if self.debug:
            print(f"Updated requirements.txt with new versions: {updated_deps}")

if __name__ == "__main__":
    # This block allows for testing the service independently
    service = DependencyManagementService()
    project_path = "/path/to/your/project"
    
    print("Analyzing dependencies...")
    deps = service.analyze_dependencies(project_path)
    print(f"Current dependencies: {deps}")
    
    print("\nUpdating dependencies...")
    updated = service.update_dependencies(project_path)
    print(f"Updated dependencies: {updated}")
    
    print("\nResolving conflicts...")
    conflicts = ["package1", "package2"]  # Example conflicts
    resolved = service.resolve_conflicts(project_path, conflicts)
    print(f"Conflicts resolved: {resolved}")
