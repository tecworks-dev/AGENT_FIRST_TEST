
"""
Purpose: Handles documentation generation tasks for the AI Software Factory.

This service provides functionality to generate and update project documentation,
including generating comprehensive documentation for the entire project and
updating the README file with recent changes.
"""

from typing import List
import os
import traceback

class DocumentationService:
    def __init__(self):
        self.debug = True  # Set to True for debugging

    def generate_documentation(self, project_path: str) -> str:
        """
        Generates comprehensive documentation for the entire project.

        Args:
            project_path (str): The path to the project root directory.

        Returns:
            str: The generated documentation as a string.
        """
        try:
            if self.debug:
                print(f"Generating documentation for project at: {project_path}")

            documentation = []
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, project_path)
                        with open(file_path, 'r') as f:
                            content = f.read()
                        documentation.append(f"# {relative_path}\n\n```python\n{content}\n```\n")

            return "\n\n".join(documentation)
        except Exception as e:
            error_msg = f"Error generating documentation: {str(e)}"
            if self.debug:
                print(error_msg)
                print(traceback.format_exc())
            return error_msg

    def update_readme(self, project_path: str, changes: List[str]) -> bool:
        """
        Updates the README.md file with recent changes.

        Args:
            project_path (str): The path to the project root directory.
            changes (List[str]): A list of recent changes to add to the README.

        Returns:
            bool: True if the README was successfully updated, False otherwise.
        """
        try:
            readme_path = os.path.join(project_path, 'README.md')
            if self.debug:
                print(f"Updating README at: {readme_path}")

            if not os.path.exists(readme_path):
                with open(readme_path, 'w') as f:
                    f.write("# Project README\n\n")

            with open(readme_path, 'r+') as f:
                content = f.read()
                f.seek(0)
                f.write(content)
                f.write("\n## Recent Changes\n\n")
                for change in changes:
                    f.write(f"- {change}\n")
                f.truncate()

            return True
        except Exception as e:
            error_msg = f"Error updating README: {str(e)}"
            if self.debug:
                print(error_msg)
                print(traceback.format_exc())
            return False

# Example usage:
if __name__ == "__main__":
    doc_service = DocumentationService()
    project_path = "/path/to/your/project"
    
    # Generate documentation
    documentation = doc_service.generate_documentation(project_path)
    print(documentation)
    
    # Update README
    changes = [
        "Added new feature X",
        "Fixed bug in module Y",
        "Improved performance of function Z"
    ]
    success = doc_service.update_readme(project_path, changes)
    print(f"README updated successfully: {success}")
