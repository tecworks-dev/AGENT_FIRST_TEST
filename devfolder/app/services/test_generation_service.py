
# Purpose: Handles test generation tasks.
# Description: This service is responsible for generating unit tests and integration tests
# for the application, utilizing AI assistance through the Anthropic API.

from typing import Dict, Any
from app.utils.api_utils import AsyncAnthropic
import os
import traceback

class TestGenerationService:
    def __init__(self):
        self.anthropic = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def generate_unit_tests(self, code: str, function_name: str) -> str:
        """
        Generate unit tests for a given function using AI assistance.

        Args:
            code (str): The source code containing the function to be tested.
            function_name (str): The name of the function to generate tests for.

        Returns:
            str: Generated unit tests as a string.
        """
        try:
            prompt = f"""
            Please generate comprehensive unit tests for the following Python function:

            {code}

            Focus on testing the function named '{function_name}'.
            Include tests for various input scenarios, edge cases, and potential errors.
            Use pytest for writing the tests.
            """

            response = await self.anthropic.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            generated_tests = response.content[0].text
            
            if os.environ.get("DEBUG") == "True":
                print(f"Generated unit tests for {function_name}:\n{generated_tests}")

            return generated_tests

        except Exception as e:
            error_message = f"Error generating unit tests: {str(e)}"
            print(error_message)
            traceback.print_exc()
            return error_message

    async def generate_integration_tests(self, project_structure: Dict[str, Any]) -> str:
        """
        Generate integration tests for the project based on its structure.

        Args:
            project_structure (Dict[str, Any]): A dictionary representing the project structure.

        Returns:
            str: Generated integration tests as a string.
        """
        try:
            prompt = f"""
            Please generate comprehensive integration tests for the following project structure:

            {project_structure}

            Focus on testing the interactions between different components and modules.
            Include tests for various scenarios, including potential edge cases and error conditions.
            Use pytest for writing the tests.
            """

            response = await self.anthropic.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )

            generated_tests = response.content[0].text
            
            if os.environ.get("DEBUG") == "True":
                print(f"Generated integration tests:\n{generated_tests}")

            return generated_tests

        except Exception as e:
            error_message = f"Error generating integration tests: {str(e)}"
            print(error_message)
            traceback.print_exc()
            return error_message

# Example usage:
# async def main():
#     test_service = TestGenerationService()
#     unit_tests = await test_service.generate_unit_tests("def add(a, b):\n    return a + b", "add")
#     print(unit_tests)
#
#     project_structure = {
#         "app": {
#             "models": ["user.py", "project.py"],
#             "services": ["auth_service.py", "project_service.py"],
#             "routes": ["auth_routes.py", "project_routes.py"]
#         }
#     }
#     integration_tests = await test_service.generate_integration_tests(project_structure)
#     print(integration_tests)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
