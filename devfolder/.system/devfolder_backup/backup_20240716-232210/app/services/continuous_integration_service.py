
# app/services/continuous_integration_service.py
# Purpose: Handles continuous integration tasks.
# Description: This service provides methods to run CI pipelines and analyze results.

from typing import Dict, Any, List
import logging
import traceback
from app.utils.api_utils import AsyncAnthropic
from app.models import Project
from app.services.version_control_service import VersionControlService
from app.services.testing_service import TestingService
from app.services.code_quality_service import CodeQualityService

class ContinuousIntegrationService:
    def __init__(self):
        self.version_control = VersionControlService()
        self.testing_service = TestingService()
        self.code_quality_service = CodeQualityService()
        self.anthropic = AsyncAnthropic()

    async def run_ci_pipeline(self, project_id: int) -> Dict[str, Any]:
        """
        Runs the continuous integration pipeline for a given project.

        Args:
            project_id (int): The ID of the project to run the CI pipeline for.

        Returns:
            Dict[str, Any]: A dictionary containing the results of the CI pipeline.
        """
        try:
            project = Project.query.get(project_id)
            if not project:
                raise ValueError(f"Project with ID {project_id} not found.")

            ci_results = {
                "project_id": project_id,
                "status": "started",
                "steps": []
            }

            # Step 1: Pull latest changes
            ci_results["steps"].append(await self.version_control.pull_latest_changes(project_id))

            # Step 2: Run tests
            test_results = await self.testing_service.run_tests(project_id)
            ci_results["steps"].append({"name": "Run Tests", "result": test_results})

            # Step 3: Code quality analysis
            quality_results = await self.code_quality_service.analyze_code_quality(project_id)
            ci_results["steps"].append({"name": "Code Quality Analysis", "result": quality_results})

            # Step 4: Build project (if applicable)
            # This step would depend on the type of project and build process

            ci_results["status"] = "completed"
            return ci_results

        except Exception as e:
            logging.error(f"Error in CI pipeline for project {project_id}: {str(e)}")
            ci_results["status"] = "failed"
            ci_results["error"] = str(e)
            if __debug__:
                print(f"CI Pipeline Error: {traceback.format_exc()}")
            return ci_results

    async def analyze_ci_results(self, ci_results: Dict[str, Any]) -> List[str]:
        """
        Analyzes the results of a CI pipeline run and provides insights.

        Args:
            ci_results (Dict[str, Any]): The results of a CI pipeline run.

        Returns:
            List[str]: A list of insights and recommendations based on the CI results.
        """
        try:
            insights = []

            if ci_results["status"] == "failed":
                insights.append(f"CI pipeline failed. Error: {ci_results.get('error', 'Unknown error')}")
                return insights

            for step in ci_results["steps"]:
                if step["name"] == "Run Tests":
                    test_insights = self._analyze_test_results(step["result"])
                    insights.extend(test_insights)
                elif step["name"] == "Code Quality Analysis":
                    quality_insights = self._analyze_quality_results(step["result"])
                    insights.extend(quality_insights)

            # Use AI to generate additional insights
            ai_prompt = f"Analyze the following CI results and provide 3 key insights or recommendations:\n{ci_results}"
            ai_response = await self.anthropic.generate_text(ai_prompt, max_tokens=150)
            ai_insights = ai_response.strip().split("\n")
            insights.extend(ai_insights)

            return insights

        except Exception as e:
            logging.error(f"Error analyzing CI results: {str(e)}")
            if __debug__:
                print(f"CI Results Analysis Error: {traceback.format_exc()}")
            return ["Error occurred while analyzing CI results."]

    def _analyze_test_results(self, test_results: Dict[str, Any]) -> List[str]:
        """Helper method to analyze test results"""
        insights = []
        if test_results["total_tests"] > 0:
            pass_rate = (test_results["passed_tests"] / test_results["total_tests"]) * 100
            insights.append(f"Test pass rate: {pass_rate:.2f}%")
            if pass_rate < 90:
                insights.append("Consider improving test coverage and fixing failing tests.")
        return insights

    def _analyze_quality_results(self, quality_results: Dict[str, Any]) -> List[str]:
        """Helper method to analyze code quality results"""
        insights = []
        if quality_results["code_smells"] > 10:
            insights.append(f"High number of code smells detected: {quality_results['code_smells']}. Consider refactoring.")
        if quality_results["maintainability_index"] < 65:
            insights.append("Low maintainability index. Code might be difficult to maintain.")
        return insights

if __name__ == "__main__":
    # This block is for testing purposes only
    import asyncio
    from app import create_app, db

    app = create_app()
    with app.app_context():
        ci_service = ContinuousIntegrationService()
        test_project_id = 1  # Assuming a project with ID 1 exists

        async def test_ci_pipeline():
            results = await ci_service.run_ci_pipeline(test_project_id)
            print("CI Pipeline Results:", results)
            insights = await ci_service.analyze_ci_results(results)
            print("CI Insights:", insights)

        asyncio.run(test_ci_pipeline())
