
# unittest_creator.py
# Purpose: Creates and runs unit tests for the application
# Description: Contains functions to create and run unit tests for the AI-assisted Python application development tool

import subprocess
import unittest
import importlib
import traceback
from termcolor import colored
from api_utils import rate_limited_request
from file_utils import get_project_files_contents, save_file_contents

DEBUG = True

async def create_unittests():
    """
    Creates unit tests for the application based on the existing code files.
    """
    try:
        if DEBUG:
            print(colored("Creating unit tests...", "cyan"))

        # Get the contents of all project files
        project_files = await get_project_files_contents()

        # Generate unit tests using AI
        prompt = f"Create unit tests for the following Python application files:\n\n{project_files}\n\nProvide the unit tests in a single Python file with appropriate test cases for each module."
        
        response = await rate_limited_request(prompt)

        # Save the generated unit tests
        await save_file_contents("tests.py", response)

        if DEBUG:
            print(colored("Unit tests created successfully.", "green"))

    except Exception as e:
        print(colored(f"Error creating unit tests: {str(e)}", "red"))
        if DEBUG:
            traceback.print_exc()

async def run_unittests():
    """
    Runs the created unit tests and reports the results.
    """
    try:
        if DEBUG:
            print(colored("Running unit tests...", "cyan"))

        # Run the unit tests using subprocess
        result = subprocess.run(["python", "-m", "unittest", "tests.py"], capture_output=True, text=True)

        if result.returncode == 0:
            print(colored("All unit tests passed successfully.", "green"))
        else:
            print(colored("Some unit tests failed. Details:", "yellow"))
            print(result.stdout)
            print(result.stderr)

        # Return test results for further processing if needed
        return result.returncode == 0, result.stdout, result.stderr

    except Exception as e:
        print(colored(f"Error running unit tests: {str(e)}", "red"))
        if DEBUG:
            traceback.print_exc()
        return False, "", str(e)

if __name__ == "__main__":
    import asyncio
    
    async def main():
        await create_unittests()
        await run_unittests()

    asyncio.run(main())
