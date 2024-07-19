
"""
app/utils/project_analyzer.py

This module provides functionality for analyzing project structure and providing insights.
It includes methods for analyzing project structure, identifying code smells, and suggesting refactoring.
"""

import os
import ast
from typing import Dict, Any, List
import traceback

DEBUG = True

class ProjectAnalyzer:
    def __init__(self):
        if DEBUG:
            print("ProjectAnalyzer initialized")

    def analyze_project_structure(self, project_path: str) -> Dict[str, Any]:
        """
        Analyzes the structure of a project given its path.

        Args:
            project_path (str): The path to the project directory.

        Returns:
            Dict[str, Any]: A dictionary containing information about the project structure.
        """
        try:
            if DEBUG:
                print(f"Analyzing project structure for: {project_path}")

            structure = {
                "files": [],
                "directories": [],
                "python_files": 0,
                "total_files": 0
            }

            for root, dirs, files in os.walk(project_path):
                rel_path = os.path.relpath(root, project_path)
                structure["directories"].append(rel_path)

                for file in files:
                    file_path = os.path.join(rel_path, file)
                    structure["files"].append(file_path)
                    structure["total_files"] += 1

                    if file.endswith(".py"):
                        structure["python_files"] += 1

            if DEBUG:
                print(f"Project structure analysis complete. Found {structure['total_files']} files.")

            return structure
        except Exception as e:
            if DEBUG:
                print(f"Error in analyze_project_structure: {str(e)}")
                print(traceback.format_exc())
            return {"error": str(e)}

    def identify_code_smells(self, project_path: str) -> List[Dict[str, str]]:
        """
        Identifies potential code smells in the project.

        Args:
            project_path (str): The path to the project directory.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing information about identified code smells.
        """
        try:
            if DEBUG:
                print(f"Identifying code smells for project: {project_path}")

            code_smells = []

            for root, _, files in os.walk(project_path):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        with open(file_path, "r") as f:
                            content = f.read()
                            tree = ast.parse(content)
                            
                            # Check for long functions
                            for node in ast.walk(tree):
                                if isinstance(node, ast.FunctionDef):
                                    if len(node.body) > 50:  # Arbitrary threshold for demonstration
                                        code_smells.append({
                                            "type": "Long Function",
                                            "file": file_path,
                                            "line": node.lineno,
                                            "message": f"Function '{node.name}' is too long ({len(node.body)} lines)"
                                        })

                            # Add more code smell checks here

            if DEBUG:
                print(f"Code smell analysis complete. Found {len(code_smells)} potential issues.")

            return code_smells
        except Exception as e:
            if DEBUG:
                print(f"Error in identify_code_smells: {str(e)}")
                print(traceback.format_exc())
            return [{"error": str(e)}]

    def suggest_refactoring(self, project_path: str) -> List[Dict[str, str]]:
        """
        Suggests refactoring based on the analysis of the project.

        Args:
            project_path (str): The path to the project directory.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing refactoring suggestions.
        """
        try:
            if DEBUG:
                print(f"Generating refactoring suggestions for project: {project_path}")

            suggestions = []
            code_smells = self.identify_code_smells(project_path)

            for smell in code_smells:
                if smell.get("type") == "Long Function":
                    suggestions.append({
                        "file": smell["file"],
                        "line": smell["line"],
                        "suggestion": f"Consider breaking down the function '{smell['message'].split(\"'\")[1]}' into smaller, more manageable functions."
                    })

            # Add more refactoring suggestions based on other analyses

            if DEBUG:
                print(f"Refactoring suggestion generation complete. Generated {len(suggestions)} suggestions.")

            return suggestions
        except Exception as e:
            if DEBUG:
                print(f"Error in suggest_refactoring: {str(e)}")
                print(traceback.format_exc())
            return [{"error": str(e)}]

if __name__ == "__main__":
    # This block allows for testing the ProjectAnalyzer class independently
    analyzer = ProjectAnalyzer()
    test_project_path = "./test_project"
    
    print("Analyzing project structure:")
    print(analyzer.analyze_project_structure(test_project_path))
    
    print("\nIdentifying code smells:")
    print(analyzer.identify_code_smells(test_project_path))
    
    print("\nSuggesting refactoring:")
    print(analyzer.suggest_refactoring(test_project_path))
