Create a file named 'code_generator.py' with the following description: 
                Responsible for generating code files based on the project plan. Contains agent_write_file() function. Imports: os, colored (from termcolor), rate_limited_request function, save_file_contents function.
            

For python files include famework such as unittest


Here's the overall application plan which you should follow while writing the file:
<application_plan>
    <overview>
        This is an AI-assisted Python application development tool. It uses the Anthropic API to generate, modify, and fix Python code based on user input and feedback. The application supports creating new projects, planning application structure, writing code files, running the application, fixing errors, and iteratively improving the codebase through user feedback.
    </overview>
    <mechanics>
        1. Project Planning: Uses AI to plan the application structure based on user input.
        2. Code Generation: Generates Python code files based on the planned structure.
        3. Error Detection and Fixing: Runs the application, detects errors, and attempts to fix them using AI.
        4. User Feedback Loop: Allows users to provide feedback and updates the application accordingly.
        5. Unit Testing: Creates and runs unit tests to ensure application functionality.
        6. File Management: Handles file operations, including reading, writing, and backing up files.
        7. Rate Limiting: Manages API request rates to prevent exceeding limits.
    </mechanics>
    <files>
        <file>
            <name>main.py</name>
            <description>
                Main entry point for the application. Contains the main() function that orchestrates the entire process. Imports: asyncio, sys, colored (from termcolor), create_application function.
            </description>
        </file>
        <file>
            <name>planner.py</name>
            <description>
                Handles the project planning phase. Contains plan_project() function. Imports: asyncio, re, colored (from termcolor), rate_limited_request function, save_file_contents function.
            </description>
        </file>
        <file>
            <name>code_generator.py</name>
            <description>
                Responsible for generating code files based on the project plan. Contains agent_write_file() function. Imports: os, colored (from termcolor), rate_limited_request function, save_file_contents function.
            </description>
        </file>
        <file>
            <name>error_fixer.py</name>
            <description>
                Handles error detection and fixing. Contains fix_application_files() function. Imports: re, colored (from termcolor), rate_limited_request function, get_project_files_contents function, save_file_contents function.
            </description>
        </file>
        <file>
            <name>feedback_handler.py</name>
            <description>
                Manages the user feedback loop and updates files accordingly. Contains update_application_files() function. Imports: os, colored (from termcolor), rate_limited_request function, select_relevant_files function, save_file_contents function.
            </description>
        </file>
        <file>
            <name>unittest_creator.py</name>
            <description>
                Creates and runs unit tests for the application. Contains create_unittests() and run_unittests() functions. Imports: subprocess, colored (from termcolor), rate_limited_request function, get_project_files_contents function, save_file_contents function.
            </description>
        </file>
        <file>
            <name>file_utils.py</name>
            <description>
                Utility functions for file operations. Contains get_file_contents(), save_file_contents(), update_backup_folder() functions. Imports: os, aiofiles, shutil, colored (from termcolor).
            </description>
        </file>
        <file>
            <name>api_utils.py</name>
            <description>
                Utility functions for API interactions. Contains rate_limited_request() function. Imports: time, asyncio, AsyncAnthropic, RateLimitError, APIError from anthropic.
            </description>
        </file>
        <file>
            <name>constants.py</name>
            <description>
                Stores constant values used throughout the application. No functions, only variable definitions. No imports.
            </description>
        </file>
        <file>
            <name>requirements.txt</name>
            <description>
                Lists all the Python package dependencies required for the application. No code, only package names and versions.
            </description>
        </file>
    </files>
</application_plan>

Remember, the application should start with a main module in the main.py file(main shouldn't take any arguments). Always return the full contents of the file
    