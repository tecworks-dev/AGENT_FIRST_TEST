
"""
code_generator.py

This file is responsible for generating code files based on the project plan.
It contains the agent_write_file() function which uses the Anthropic API to generate Python code.
"""

import os
import traceback
from termcolor import colored
from api_utils import rate_limited_request
from file_utils import save_file_contents
import unittest

DEBUG = True

async def agent_write_file(file_name, file_description, project_plan):
    """
    Generate code for a specific file using the Anthropic API.

    Args:
    file_name (str): The name of the file to be generated.
    file_description (str): A description of the file's purpose and contents.
    project_plan (str): The overall project plan.

    Returns:
    str: The generated code for the file.
    """
    try:
        if DEBUG:
            print(f"Generating code for {file_name}...")

        prompt = f"""
        Create a file named '{file_name}' with the following description: 
        {file_description}

        For python files include framework such as unittest

        Here's the overall application plan which you should follow while writing the file:
        {project_plan}

        Remember, the application should start with a main module in the main.py file(main shouldn't take any arguments).
        Always return the full contents of the file
        """

        response = await rate_limited_request(prompt)
        
        if DEBUG:
            print(f"Code generated for {file_name}")

        # Extract code from the response
        code_start = response.find("