
# planner.py
"""
Handles the project planning phase. Contains plan_project() function.
This module is responsible for generating a project plan based on user input using AI assistance.
"""

import asyncio
import re
from termcolor import colored
from api_utils import rate_limited_request
from file_utils import save_file_contents
import traceback

DEBUG = True

async def plan_project(user_input):
    """
    Generate a project plan based on user input using AI assistance.
    
    Args:
    user_input (str): The user's description of the desired project.
    
    Returns:
    str: The generated project plan.
    """
    try:
        if DEBUG:
            print(colored("DEBUG: Starting project planning...", "yellow"))

        # Prepare the prompt for the AI
        prompt = f"""
        Based on the following user input, create a detailed project plan:

        User Input: {user_input}

        The project plan should include:
        1. An overview of the project
        2. A list of main features
        3. A suggested file structure with brief descriptions of each file's purpose
        4. Any potential challenges or considerations

        Please format the response in a clear, structured manner.
        """

        # Make the API request
        response = await rate_limited_request(prompt)

        # Extract the project plan from the response
        project_plan = response.completion.text.strip()

        # Save the project plan to a file
        await save_file_contents("project_plan.txt", project_plan)

        if DEBUG:
            print(colored("DEBUG: Project plan generated and saved.", "yellow"))

        return project_plan

    except Exception as e:
        print(colored(f"Error in plan_project: {str(e)}", "red"))
        if DEBUG:
            print(colored("Traceback:", "red"))
            print(colored(traceback.format_exc(), "red"))
        return None

async def validate_plan(project_plan):
    """
    Validate the generated project plan to ensure it meets the required format and content.
    
    Args:
    project_plan (str): The generated project plan.
    
    Returns:
    bool: True if the plan is valid, False otherwise.
    """
    try:
        if DEBUG:
            print(colored("DEBUG: Validating project plan...", "yellow"))

        # Check for required sections
        required_sections = ["overview", "main features", "file structure", "challenges"]
        for section in required_sections:
            if section not in project_plan.lower():
                print(colored(f"Error: Project plan is missing the '{section}' section.", "red"))
                return False

        # Check for file structure format
        file_structure = re.search(r"file structure:(.*?)(?:\n\n|\Z)", project_plan, re.DOTALL | re.IGNORECASE)
        if not file_structure:
            print(colored("Error: File structure section is not properly formatted.", "red"))
            return False

        if DEBUG:
            print(colored("DEBUG: Project plan validation completed.", "yellow"))

        return True

    except Exception as e:
        print(colored(f"Error in validate_plan: {str(e)}", "red"))
        if DEBUG:
            print(colored("Traceback:", "red"))
            print(colored(traceback.format_exc(), "red"))
        return False

# Add more helper functions as needed

if __name__ == "__main__":
    # This block allows you to test the module independently
    test_input = "Create a simple to-do list application with a command-line interface."
    asyncio.run(plan_project(test_input))

# Unit tests
import unittest

class TestPlanner(unittest.TestCase):
    def test_plan_project(self):
        test_input = "Create a simple to-do list application with a command-line interface."
        plan = asyncio.run(plan_project(test_input))
        self.assertIsNotNone(plan)
        self.assertIn("overview", plan.lower())
        self.assertIn("main features", plan.lower())
        self.assertIn("file structure", plan.lower())

    def test_validate_plan(self):
        valid_plan = """
        Overview: This is a test plan.
        Main Features: Feature 1, Feature 2
        File Structure: main.py, utils.py
        Challenges: Challenge 1, Challenge 2
        """
        self.assertTrue(asyncio.run(validate_plan(valid_plan)))

        invalid_plan = "This is an invalid plan without proper sections."
        self.assertFalse(asyncio.run(validate_plan(invalid_plan)))

if __name__ == "__main__":
    unittest.main()
