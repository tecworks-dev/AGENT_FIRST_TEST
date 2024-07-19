
# Purpose: Generate AI prompts for various tasks
# Description: This module provides a class for generating AI prompts for code generation, testing, and refactoring.

import unittest
from typing import Dict, Any

class AIPromptGenerator:
    def __init__(self):
        self.code_prompt_template = "Generate Python code for the following task: {task}\n\nRequirements:\n{requirements}\n\nPlease provide clean, well-commented code that follows best practices."
        self.test_prompt_template = "Generate unit tests for the following Python code:\n\n{code}\n\nEnsure comprehensive test coverage and include edge cases."
        self.refactor_prompt_template = "Refactor the following Python code to address this issue: {issue}\n\nOriginal code:\n{code}\n\nPlease provide the refactored code with explanations for the changes made."

    def generate_code_prompt(self, task: str) -> str:
        """
        Generate a prompt for code generation.

        Args:
            task (str): Description of the coding task.

        Returns:
            str: Generated prompt for code generation.
        """
        requirements = "- Follow PEP 8 style guidelines\n- Include error handling\n- Use type hints"
        return self.code_prompt_template.format(task=task, requirements=requirements)

    def generate_test_prompt(self, code: str) -> str:
        """
        Generate a prompt for test creation.

        Args:
            code (str): The code to be tested.

        Returns:
            str: Generated prompt for test creation.
        """
        return self.test_prompt_template.format(code=code)

    def generate_refactor_prompt(self, code: str, issue: str) -> str:
        """
        Generate a prompt for code refactoring.

        Args:
            code (str): The code to be refactored.
            issue (str): The issue to be addressed in the refactoring.

        Returns:
            str: Generated prompt for code refactoring.
        """
        return self.refactor_prompt_template.format(code=code, issue=issue)


class TestAIPromptGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = AIPromptGenerator()

    def test_generate_code_prompt(self):
        task = "Create a function to calculate the factorial of a number"
        prompt = self.generator.generate_code_prompt(task)
        self.assertIn(task, prompt)
        self.assertIn("Requirements:", prompt)

    def test_generate_test_prompt(self):
        code = "def factorial(n):\n    return 1 if n == 0 else n * factorial(n - 1)"
        prompt = self.generator.generate_test_prompt(code)
        self.assertIn(code, prompt)
        self.assertIn("Generate unit tests", prompt)

    def test_generate_refactor_prompt(self):
        code = "def foo(x, y):\n    return x + y"
        issue = "Improve function naming and add type hints"
        prompt = self.generator.generate_refactor_prompt(code, issue)
        self.assertIn(code, prompt)
        self.assertIn(issue, prompt)


if __name__ == "__main__":
    unittest.main()
