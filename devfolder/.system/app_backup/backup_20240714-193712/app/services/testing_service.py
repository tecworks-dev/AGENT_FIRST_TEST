
# app/services/testing_service.py
"""
Handles AI-driven test generation and execution.
This service provides methods to generate unit tests for given code
and run those tests, returning the results.
"""

from typing import Dict, Any
import unittest
import io
import sys
import traceback
import ast
from app.utils.api_utils import AsyncAnthropic
import os

class TestingService:
    def __init__(self):
        self.anthropic = AsyncAnthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    async def generate_tests(self, code: str) -> str:
        """
        Generates unit tests for the given code using AI.

        Args:
            code (str): The source code to generate tests for.

        Returns:
            str: The generated unit test code.
        """
        prompt = f"""
        Generate comprehensive unit tests for the following Python code:

        {code}

        Please include tests for both normal cases and edge cases. Use unittest framework.
        """

        response = await self.anthropic.completions.create(
            prompt=prompt,
            max_tokens_to_sample=1000,
            model="claude-2"
        )
        
        return response.completion

    async def run_tests(self, code: str, tests: str) -> Dict[str, Any]:
        """
        Runs the generated tests against the given code.

        Args:
            code (str): The source code to test.
            tests (str): The unit test code to run.

        Returns:
            Dict[str, Any]: A dictionary containing test results and any errors.
        """
        # Combine code and tests
        full_code = f"{code}\n\n{tests}"

        # Create a new module
        module = ast.parse(full_code)

        # Compile the module
        compiled_code = compile(module, filename="<ast>", mode="exec")

        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        test_results = {
            "success": False,
            "output": "",
            "error": None
        }

        try:
            # Execute the code
            exec(compiled_code, globals())

            # Run the tests
            test_suite = unittest.defaultTestLoader.loadTestsFromName("__main__")
            test_runner = unittest.TextTestRunner(stream=sys.stdout)
            test_result = test_runner.run(test_suite)

            test_results["success"] = test_result.wasSuccessful()
            test_results["output"] = sys.stdout.getvalue()

        except Exception as e:
            test_results["error"] = str(e)
            test_results["output"] = traceback.format_exc()

        finally:
            # Restore stdout
            sys.stdout = old_stdout

        return test_results

    def debug_log(self, message: str) -> None:
        """
        Logs debug messages if DEBUG is set to True.

        Args:
            message (str): The debug message to log.
        """
        if os.getenv('DEBUG', 'False').lower() == 'true':
            print(f"DEBUG: {message}")

# Example usage (not part of the class):
# async def main():
#     testing_service = TestingService()
#     code = "def add(a, b): return a + b"
#     tests = await testing_service.generate_tests(code)
#     results = await testing_service.run_tests(code, tests)
#     print(results)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
