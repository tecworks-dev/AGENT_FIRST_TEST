
# app/utils/ai_prompt_templates.py
"""
This module stores templates for AI prompts used across the application.
It provides a centralized location for managing and accessing various prompt templates
for different AI-related tasks such as code generation, code review, and error fixing.
"""

import logging
from typing import Dict

class AIPromptTemplates:
    """
    A class that stores and manages templates for AI prompts used in various parts of the application.
    """

    def __init__(self):
        self.templates: Dict[str, str] = {
            "code_generation": "Generate Python code for the following task:\n{task_description}\nPlease provide clean, well-commented code that follows best practices.",
            "code_review": "Review the following code and provide feedback on its quality, efficiency, and adherence to best practices:\n\n{code}\n\nPlease provide specific suggestions for improvement if applicable.",
            "error_fixing": "The following code snippet has produced an error:\n\n{code_snippet}\n\nError message:\n{error_message}\n\nPlease analyze the error and suggest a fix for the code."
        }
        self.logger = logging.getLogger(__name__)

    def get_code_generation_prompt(self, task_description: str) -> str:
        """
        Generates a prompt for code generation based on the given task description.

        Args:
            task_description (str): A description of the coding task.

        Returns:
            str: The formatted prompt for code generation.
        """
        try:
            return self.templates["code_generation"].format(task_description=task_description)
        except KeyError:
            self.logger.error("Code generation template not found.")
            return ""
        except Exception as e:
            self.logger.error(f"Error generating code generation prompt: {str(e)}")
            return ""

    def get_code_review_prompt(self, code: str) -> str:
        """
        Generates a prompt for code review based on the given code.

        Args:
            code (str): The code to be reviewed.

        Returns:
            str: The formatted prompt for code review.
        """
        try:
            return self.templates["code_review"].format(code=code)
        except KeyError:
            self.logger.error("Code review template not found.")
            return ""
        except Exception as e:
            self.logger.error(f"Error generating code review prompt: {str(e)}")
            return ""

    def get_error_fixing_prompt(self, error_message: str, code_snippet: str) -> str:
        """
        Generates a prompt for error fixing based on the given error message and code snippet.

        Args:
            error_message (str): The error message to be addressed.
            code_snippet (str): The code snippet containing the error.

        Returns:
            str: The formatted prompt for error fixing.
        """
        try:
            return self.templates["error_fixing"].format(error_message=error_message, code_snippet=code_snippet)
        except KeyError:
            self.logger.error("Error fixing template not found.")
            return ""
        except Exception as e:
            self.logger.error(f"Error generating error fixing prompt: {str(e)}")
            return ""

# Debugging statements
if __name__ == "__main__":
    import traceback

    DEBUG = True

    if DEBUG:
        print("Debugging AIPromptTemplates class...")
        templates = AIPromptTemplates()

        try:
            print("\nTesting get_code_generation_prompt:")
            print(templates.get_code_generation_prompt("Create a function to calculate the factorial of a number"))

            print("\nTesting get_code_review_prompt:")
            print(templates.get_code_review_prompt("def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)"))

            print("\nTesting get_error_fixing_prompt:")
            print(templates.get_error_fixing_prompt("NameError: name 'factorial' is not defined", "result = factorial(5)"))

        except Exception as e:
            print(f"An error occurred during debugging: {str(e)}")
            print(traceback.format_exc())
