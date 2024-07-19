
# Purpose: Implements test coverage analysis functionality.
# Description: This module provides a TestCoverageAnalyzer class to analyze test coverage for a given project.

import coverage
from typing import Dict, Any
import os
import traceback
from app.models import Project
from app.utils.logging_service import LoggingService

DEBUG = True

class TestCoverageAnalyzer:
    def __init__(self):
        self.logger = LoggingService()

    def analyze_coverage(self, project_id: int) -> Dict[str, Any]:
        """
        Analyzes test coverage for a given project.

        Args:
            project_id (int): The ID of the project to analyze.

        Returns:
            Dict[str, Any]: A dictionary containing coverage analysis results.
        """
        try:
            if DEBUG:
                print(f"Starting coverage analysis for project ID: {project_id}")

            project = Project.query.get(project_id)
            if not project:
                raise ValueError(f"Project with ID {project_id} not found")

            project_path = project.path  # Assuming Project model has a 'path' attribute

            cov = coverage.Coverage(source=[project_path])
            cov.start()

            # Run tests for the project
            self._run_project_tests(project_path)

            cov.stop()
            cov.save()

            report = cov.report(show_missing=True)
            
            # Get more detailed coverage data
            coverage_data = cov.get_data()
            files = coverage_data.measured_files()
            
            result = {
                "total_coverage": report,
                "file_coverage": {}
            }

            for file in files:
                file_coverage = coverage_data.line_counts(file)
                if file_coverage:
                    result["file_coverage"][file] = {
                        "total_lines": file_coverage[0],
                        "covered_lines": file_coverage[1],
                        "coverage_percentage": (file_coverage[1] / file_coverage[0]) * 100 if file_coverage[0] > 0 else 0
                    }

            if DEBUG:
                print(f"Coverage analysis completed for project ID: {project_id}")
                print(f"Coverage result: {result}")

            return result

        except Exception as e:
            error_msg = f"Error during coverage analysis for project ID {project_id}: {str(e)}"
            self.logger.log_error(error_msg, traceback.format_exc())
            if DEBUG:
                print(error_msg)
                print(traceback.format_exc())
            return {"error": error_msg}

    def _run_project_tests(self, project_path: str):
        """
        Runs tests for the project.

        Args:
            project_path (str): The path to the project directory.
        """
        import unittest

        if DEBUG:
            print(f"Running tests for project at path: {project_path}")

        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover(project_path, pattern="test_*.py")

        test_runner = unittest.TextTestRunner(verbosity=2)
        test_runner.run(test_suite)

if __name__ == "__main__":
    # This block is for testing purposes only
    analyzer = TestCoverageAnalyzer()
    result = analyzer.analyze_coverage(1)  # Assuming project with ID 1 exists
    print(result)
