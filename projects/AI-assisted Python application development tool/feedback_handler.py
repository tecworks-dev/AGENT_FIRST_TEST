
# feedback_handler.py
"""
Manages the user feedback loop and updates files accordingly.
This module handles user feedback and updates the application files based on that feedback.
"""

import os
import traceback
from termcolor import colored
from api_utils import rate_limited_request
from file_utils import select_relevant_files, save_file_contents
import constants

DEBUG = True

async def update_application_files(feedback, project_files):
    """
    Updates application files based on user feedback.

    Args:
    feedback (str): User feedback on the current state of the application.
    project_files (dict): Dictionary containing file names and their contents.

    Returns:
    dict: Updated project files.
    """
    try:
        if DEBUG:
            print(colored("Updating application files based on user feedback...", "cyan"))

        # Select relevant files for update based on feedback
        relevant_files = select_relevant_files(feedback, project_files)

        for file_name, file_content in relevant_files.items():
            if DEBUG:
                print(colored(f"Updating file: {file_name}", "yellow"))

            prompt = f"""
            You are a Python and Web Full Stack expert Developer. Your task is to update the following file based on user feedback:

            File name: {file_name}
            Current content:
            {file_content}

            User feedback:
            {feedback}

            Please provide the updated content for this file, addressing the user's feedback.
            Return only the updated file content, without any additional explanations.
            """

            updated_content = await rate_limited_request(prompt)

            # Save the updated content
            save_file_contents(file_name, updated_content)
            project_files[file_name] = updated_content

        if DEBUG:
            print(colored("Application files updated successfully.", "green"))

        return project_files

    except Exception as e:
        print(colored(f"Error in update_application_files: {str(e)}", "red"))
        if DEBUG:
            traceback.print_exc()
        return project_files

# Unit tests
import unittest
from unittest.mock import patch, AsyncMock

class TestFeedbackHandler(unittest.TestCase):
    @patch('feedback_handler.rate_limited_request')
    @patch('feedback_handler.select_relevant_files')
    @patch('feedback_handler.save_file_contents')
    async def test_update_application_files(self, mock_save, mock_select, mock_request):
        # Mock dependencies
        mock_select.return_value = {'test.py': 'original content'}
        mock_request.return_value = 'updated content'

        # Test data
        feedback = "Please update test.py"
        project_files = {'test.py': 'original content', 'other.py': 'content'}

        # Run the function
        updated_files = await update_application_files(feedback, project_files)

        # Assertions
        mock_select.assert_called_once_with(feedback, project_files)
        mock_request.assert_called_once()
        mock_save.assert_called_once_with('test.py', 'updated content')
        self.assertEqual(updated_files['test.py'], 'updated content')
        self.assertEqual(updated_files['other.py'], 'content')

if __name__ == '__main__':
    unittest.main()
