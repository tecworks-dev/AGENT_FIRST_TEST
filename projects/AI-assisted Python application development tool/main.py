
# main.py
# Purpose: Main entry point for the AI-assisted Python application development tool.
# Description: Orchestrates the entire process including project planning, code generation,
#              error fixing, user feedback handling, and unit testing.

import asyncio
import sys
import traceback
from termcolor import colored
from planner import plan_project
from code_generator import agent_write_file
from error_fixer import fix_application_files
from feedback_handler import update_application_files
from unittest_creator import create_unittests, run_unittests
from constants import DEBUG

# IMPORTANT: do not remove main function as automated test will fail
# IMPORTANT: do not remove this comment
async def main():
    try:
        print(colored("Starting AI-assisted Python application development...", "cyan"))

        # Project Planning
        project_plan = await plan_project()
        if DEBUG:
            print(colored("Project plan created.", "green"))

        # Code Generation
        for file_info in project_plan['files']:
            await agent_write_file(file_info['name'], file_info['description'])
        if DEBUG:
            print(colored("Initial code files generated.", "green"))

        # Error Detection and Fixing
        fixed = await fix_application_files()
        if DEBUG:
            print(colored(f"Application files fixed: {fixed}", "green"))

        # User Feedback Loop
        while True:
            user_feedback = input(colored("Enter your feedback (or 'done' to finish): ", "yellow"))
            if user_feedback.lower() == 'done':
                break
            updated = await update_application_files(user_feedback)
            if DEBUG:
                print(colored(f"Files updated based on feedback: {updated}", "green"))

        # Unit Testing
        await create_unittests()
        test_results = await run_unittests()
        if DEBUG:
            print(colored(f"Unit test results: {test_results}", "green"))

        print(colored("AI-assisted Python application development completed.", "cyan"))

    except Exception as e:
        print(colored(f"An error occurred: {str(e)}", "red"))
        if DEBUG:
            print(colored("Traceback:", "red"))
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

# Unit tests
import unittest

class TestMain(unittest.TestCase):
    def test_main_exists(self):
        self.assertTrue(callable(main), "main function should exist and be callable")

    def test_main_is_coroutine(self):
        self.assertTrue(asyncio.iscoroutinefunction(main), "main should be a coroutine function")

if __name__ == "__main__":
    unittest.main()
