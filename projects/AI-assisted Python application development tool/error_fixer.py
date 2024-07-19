
# error_fixer.py
"""
This module handles error detection and fixing for the AI-assisted Python application development tool.
It contains functions to analyze application errors and generate fixes using AI assistance.
"""

import re
import traceback
from termcolor import colored
from api_utils import rate_limited_request
from file_utils import get_project_files_contents, save_file_contents
import unittest

DEBUG = True

async def fix_application_files(error_message, project_files):
    """
    Analyzes the error message and attempts to fix the relevant project files.

    Args:
    error_message (str): The error message to be analyzed and fixed.
    project_files (dict): A dictionary containing the project file names and their contents.

    Returns:
    dict: Updated project files with fixes applied.
    """
    if DEBUG:
        print(colored(f"Debugging: Attempting to fix error: {error_message}", "yellow"))

    try:
        # Extract relevant information from the error message
        file_name, line_number, error_type = parse_error_message(error_message)

        if not file_name or not line_number or not error_type:
            raise ValueError("Unable to parse error message")

        # Get the content of the file with the error
        file_content = project_files.get(file_name)
        if not file_content:
            raise ValueError(f"File {file_name} not found in project files")

        # Generate a fix for the error using AI
        fix = await generate_fix(file_name, file_content, line_number, error_type, error_message)

        # Apply the fix to the file content
        updated_content = apply_fix(file_content, fix, line_number)

        # Update the project files dictionary with the fixed content
        project_files[file_name] = updated_content

        if DEBUG:
            print(colored(f"Debugging: Fix applied to {file_name}", "green"))

        return project_files

    except Exception as e:
        print(colored(f"Error in fix_application_files: {str(e)}", "red"))
        if DEBUG:
            traceback.print_exc()
        return project_files

def parse_error_message(error_message):
    """
    Parses the error message to extract relevant information.

    Args:
    error_message (str): The error message to be parsed.

    Returns:
    tuple: (file_name, line_number, error_type)
    """
    # Example regex pattern, adjust based on your error message format
    pattern = r"File \"(.+)\", line (\d+).+(?:(\w+Error):)?"
    match = re.search(pattern, error_message)
    
    if match:
        return match.group(1), int(match.group(2)), match.group(3)
    return None, None, None

async def generate_fix(file_name, file_content, line_number, error_type, error_message):
    """
    Generates a fix for the error using AI assistance.

    Args:
    file_name (str): Name of the file containing the error.
    file_content (str): Content of the file containing the error.
    line_number (int): Line number where the error occurred.
    error_type (str): Type of the error.
    error_message (str): Full error message.

    Returns:
    str: Suggested fix for the error.
    """
    prompt = f"""
    Given the following error in the file '{file_name}' at line {line_number}:
    Error Type: {error_type}
    Error Message: {error_message}

    Please provide a fix for this error. Here's the relevant part of the file:

    {file_content}

    Suggest a correction that resolves the error.
    """

    response = await rate_limited_request(prompt)
    return response.completion

def apply_fix(file_content, fix, line_number):
    """
    Applies the generated fix to the file content.

    Args:
    file_content (str): Original content of the file.
    fix (str): The fix to be applied.
    line_number (int): Line number where the fix should be applied.

    Returns:
    str: Updated file content with the fix applied.
    """
    lines = file_content.split('\n')
    lines[line_number - 1] = fix.strip()
    return '\n'.join(lines)

class TestErrorFixer(unittest.TestCase):
    def test_parse_error_message(self):
        error_message = 'File "test.py", line 10, in <module>\n    TypeError: unsupported operand type(s) for +: "int" and "str"'
        file_name, line_number, error_type = parse_error_message(error_message)
        self.assertEqual(file_name, "test.py")
        self.assertEqual(line_number, 10)
        self.assertEqual(error_type, "TypeError")

    def test_apply_fix(self):
        file_content = "line1\nline2\nline3\nline4"
        fix = "fixed line"
        line_number = 3
        expected_result = "line1\nline2\nfixed line\nline4"
        result = apply_fix(file_content, fix, line_number)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
