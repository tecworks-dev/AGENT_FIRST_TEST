import asyncio
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from typing import List, Dict, Tuple, Optional, Any
import subprocess
import unittest
import logging
import shutil
from dataclasses import dataclass
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio
import yaml
import html
import git
import pylint.lint

import aiofiles
import aiohttp
from anthropic import AsyncAnthropic, RateLimitError, APIError
from termcolor import colored

# Import custom modules
from file_selector import FileTreeSelector
from requirements_manager import RequirementsManager

@dataclass
class Config:
    dev_folder: str = os.getenv('DEV_FOLDER', 'app')
    backup_folder: str = os.getenv('BACKUP_FOLDER', 'app_backup')
    logs_folder: str = os.getenv('LOGS_FOLDER', 'app/logs')
    request_limit: int = int(os.getenv('REQUEST_LIMIT', '145'))
    time_window: int = int(os.getenv('TIME_WINDOW', '60'))
    max_retries: int = int(os.getenv('MAX_RETRIES', '20'))
    base_delay: int = int(os.getenv('BASE_DELAY', '60'))
    max_fix_attempts: int = int(os.getenv('MAX_FIX_ATTEMPTS', '5'))

    @classmethod
    def from_file(cls, filename: str) -> 'Config':
        with open(filename, 'r') as f:
            config_dict = yaml.safe_load(f)
        return cls(**config_dict)

class Plugin:
    def hook_method(self, *args: Any, **kwargs: Any) -> None:
        pass

class AIAssistedDevTool:
    """
    A tool for AI-assisted Python application development.
    
    This class provides functionality for creating, updating, fixing, and managing
    Python applications with the assistance of AI.
    """

    def __init__(self, config: Config, anthropic_client: AsyncAnthropic, 
                 file_selector: FileTreeSelector, requirements_manager: RequirementsManager,
                 logger: logging.Logger):
        """
        Initialize the AIAssistedDevTool.

        Args:
            config (Config): Configuration settings for the tool.
            anthropic_client (AsyncAnthropic): Client for interacting with the Anthropic API.
            file_selector (FileTreeSelector): Tool for selecting files in the project.
            requirements_manager (RequirementsManager): Tool for managing project requirements.
            logger (logging.Logger): Logger for the tool.
        """
        self.config = config
        self.anthropic_client = anthropic_client
        self.file_selector = file_selector
        self.requirements_manager = requirements_manager
        self.logger = logger
        self.request_counter = 0
        self.request_timestamps: List[float] = []
        self.plugins: List[Plugin] = []

    def register_plugin(self, plugin: Plugin) -> None:
        """Register a plugin with the tool."""
        self.plugins.append(plugin)

    def run_plugins(self, hook_name: str, *args: Any, **kwargs: Any) -> None:
        """Run all registered plugins for a given hook."""
        for plugin in self.plugins:
            if hasattr(plugin, hook_name):
                getattr(plugin, hook_name)(*args, **kwargs)

    async def with_error_recovery(self, operation: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Execute an operation with error recovery.

        Args:
            operation: The async operation to execute.
            *args: Positional arguments for the operation.
            **kwargs: Keyword arguments for the operation.

        Returns:
            The result of the operation if successful.

        Raises:
            Exception: If the operation fails after max retries.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return await operation(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error during {operation.__name__}: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

    async def run(self) -> None:
        """Main loop for the AI Assisted Dev Tool."""
        self.logger.info("Starting AI Assisted Dev Tool")
        print(colored("Welcome to AI Assisted Dev Tool!", "cyan"))
        while True:
            action = await self.get_validated_input(
                "Choose an action (create/update/fix/run/test/backup/restore/structure/quit): ",
                "action",
                default="create"
            )
            try:
                if action == "quit":
                    break
                elif action == "create":
                    await self.with_error_recovery(self.create_application)
                elif action == "update":
                    await self.with_error_recovery(self.update_application)
                elif action == "fix":
                    await self.with_error_recovery(self.fix_application)
                elif action == "run":
                    await self.with_error_recovery(self.run_and_improve_application)
                elif action == "test":
                    await self.with_error_recovery(self.run_unit_tests)
                elif action == "backup":
                    await self.with_error_recovery(self.backup_project)
                elif action == "restore":
                    await self.with_error_recovery(self.restore_backup)
                elif action == "structure":
                    await self.with_error_recovery(self.show_project_structure)
                self.run_plugins('after_action', action)
            except Exception as e:
                self.logger.error(f"An error occurred: {str(e)}", exc_info=True)
                print(colored(f"An error occurred: {str(e)}", "red"))
                print("Traceback:")
                traceback.print_exc()
                user_choice = await self.get_validated_input("Do you want to continue? (yes/no): ", "yes_no", default="yes")
                if user_choice.lower() != "yes":
                    break

        self.logger.info("AI Assisted Dev Tool session ended")
        print(colored("Thank you for using AI Assisted Dev Tool. Goodbye!", "cyan"))

    async def create_application(self) -> None:
        """Create a new application based on user input."""
        self.logger.info("Starting application creation process")
        user_input = await self.get_user_input("Describe the Python application you want to create: ")
        plan = await self.iterative_planning(user_input)
        await self.save_application_plan(plan)
        await self.create_application_files(plan)
        await self.update_requirements()
        self.commit_changes("Initial application creation")
        self.logger.info("Application creation process completed")

    async def iterative_planning(self, initial_input: str, max_iterations: int = 3) -> str:
        """
        Iteratively refine the application plan based on user feedback.

        Args:
            initial_input (str): The initial description of the application.
            max_iterations (int): Maximum number of refinement iterations.

        Returns:
            str: The final application plan.
        """
        self.logger.info(f"Starting iterative planning with max {max_iterations} iterations")
        current_plan = await self.generate_application_plan(initial_input)
        
        for iteration in tqdm(range(max_iterations), desc="Planning Iterations"):
            print(colored(f"\nIteration {iteration + 1}/{max_iterations}", "cyan"))
            print(colored("Current Application Plan:", "yellow"))
            print(current_plan)
            
            user_approval = await self.get_validated_input("Do you approve this plan? (yes/no/refine): ", "yes_no_refine", default="yes")
            
            if user_approval.lower() == 'yes':
                self.logger.info("User approved the application plan")
                return current_plan
            elif user_approval.lower() == 'no':
                user_feedback = await self.get_user_input("Please provide feedback for improvement: ")
                current_plan = await self.refine_application_plan(current_plan, user_feedback)
            else:  # refine
                current_plan = await self.refine_application_plan(current_plan)
        
        self.logger.info("Iterative planning completed")
        return current_plan

    async def generate_application_plan(self, user_input: str) -> str:
        """
        Generate an initial application plan based on user input.

        Args:
            user_input (str): The user's description of the desired application.

        Returns:
            str: The generated application plan in XML format.
        """
        self.logger.info("Generating initial application plan")
        system_message = """You are an expert Python application designer. Create a detailed application plan based on the user's input.
Your response should be in the following XML format:
<application_plan>
    <overview>Overall application description</overview>
    <mechanics>Key application mechanics</mechanics>
    <files>
        <file>
            <name>filename.ext</name>
            <description>File purpose and contents</description>
        </file>
        <!-- Repeat <file> element for each file -->
    </files>
</application_plan>"""
        response = await self.rate_limited_request(
            model="claude-3-5-sonnet-20240620",
            system=system_message,
            messages=[{"role": "user", "content": user_input}],
            max_tokens=4000
        )
        return self.extract_xml_plan(response.content[0].text)

    async def refine_application_plan(self, current_plan: str, user_feedback: str = "") -> str:
        """
        Refine the application plan based on user feedback or AI analysis.

        Args:
            current_plan (str): The current application plan.
            user_feedback (str, optional): User feedback for refinement.

        Returns:
            str: The refined application plan.
        """
        self.logger.info("Refining application plan")
        system_message = """You are an expert Python application designer. Refine the given application plan based on the provided feedback (if any) or your own analysis for improvement.
Your response should be in the following XML format:
<application_plan>
    <overview>Overall application description</overview>
    <mechanics>Key application mechanics</mechanics>
    <files>
        <file>
            <name>filename.ext</name>
            <description>File purpose and contents</description>
        </file>
        <!-- Repeat <file> element for each file -->
    </files>
</application_plan>"""
        
        prompt = f"Refine the following application plan:\n\n{current_plan}\n\n"
        if user_feedback:
            prompt += f"Consider this feedback: {user_feedback}\n"
        prompt += "If no specific feedback is provided, analyze the plan for potential improvements in structure, completeness, or clarity."

        response = await self.rate_limited_request(
            model="claude-3-5-sonnet-20240620",
            system=system_message,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        return self.extract_xml_plan(response.content[0].text)

    async def update_application(self) -> None:
        """Update the application based on user feedback."""
        self.logger.info("Starting application update process")
        feedback = await self.get_user_feedback()
        files_to_update = await self.select_files_for_update(feedback)
        await self.update_files(files_to_update, feedback)
        await self.update_requirements()
        await self.run_tests()
        self.commit_changes("Application update")
        self.logger.info("Application update process completed")

    async def get_user_feedback(self) -> str:
        """Get feedback from the user for application update."""
        return await self.get_user_input("Provide feedback for application update: ")

    async def select_files_for_update(self, feedback: str) -> List[str]:
        """Select files for updating based on user feedback."""
        selection_method = await self.get_validated_input("Choose file selection method (model/manual): ", "file_selection", default="model")
        return await self.select_files(selection_method, feedback)

    async def update_files(self, files: List[str], feedback: str) -> None:
        """Update the specified files based on user feedback."""
        plan = await self.load_application_plan()
        update_tasks = [self.update_file(file, feedback, plan) for file in files]
        await tqdm_asyncio.gather(*update_tasks, desc="Updating Files")

    async def update_file(self, file: str, feedback: str, plan: str) -> None:
        """Update a single file based on user feedback and the application plan."""
        content = await self.get_file_contents(file)
        updated_content = await self.update_file_content(file, content, feedback, plan)
        await self.save_file(file, updated_content)
        await self.create_test_file(file)

    async def fix_application(self) -> None:
        """Attempt to fix the application if errors are detected."""
        self.logger.info("Starting application fix process")
        for attempt in tqdm(range(self.config.max_fix_attempts), desc="Fix Attempts"):
            error_message = await self.run_application()
            if not error_message:
                self.logger.info(f"Application fixed successfully after {attempt + 1} attempts")
                print(colored(f"Application fixed successfully after {attempt + 1} attempts!", "green"))
                await self.run_unit_tests()
                self.commit_changes("Application fix")
                return
            
            print(colored(f"Fix attempt {attempt + 1}/{self.config.max_fix_attempts}", "yellow"))
            await self.fix_application_files(error_message)
            await self.update_requirements()
        
        self.logger.warning(f"Failed to fix the application after {self.config.max_fix_attempts} attempts")
        print(colored(f"Failed to fix the application after {self.config.max_fix_attempts} attempts.", "red"))
        user_choice = await self.get_validated_input("Do you want to try manual fixing? (yes/no): ", "yes_no", default="yes")
        if user_choice.lower() == "yes":
            await self.manual_fix()

    async def fix_application_files(self, error_message: str) -> None:
        """
        Fix application files based on the error message.

        Args:
            error_message (str): The error message to guide the fixing process.
        """
        self.logger.info("Fixing application files")
        files_to_fix = self.extract_error_files(error_message)
        plan = await self.load_application_plan()
        
        for file in files_to_fix:
            try:
                content = await self.get_file_contents(file)
                fixed_content = await self.fix_file_content(file, content, error_message, plan)
                await self.save_file(file, fixed_content)
                self.logger.info(f"Fixed file: {file}")
            except FileNotFoundError:
                self.logger.error(f"File not found: {file}")
                print(colored(f"Error: File {file} not found. Skipping.", "red"))
            except Exception as e:
                self.logger.error(f"Error fixing file {file}: {str(e)}", exc_info=True)
                print(colored(f"Error fixing file {file}: {str(e)}", "red"))

    async def manual_fix(self) -> None:
        """Allow manual fixing of the application by the user."""
        self.logger.info("Starting manual fix process")
        while True:
            error_message = await self.run_application()
            if not error_message:
                self.logger.info("Application fixed successfully through manual process")
                print(colored("Application fixed successfully!", "green"))
                self.commit_changes("Manual application fix")
                return
            
            print(colored("Current error:", "red"))
            print(error_message)
            
            file_to_edit = await self.get_user_input("Enter the file name to edit (or 'quit' to stop): ")
            if file_to_edit.lower() == 'quit':
                break
            
            await self.edit_file(file_to_edit)
            await self.update_requirements()

    async def edit_file(self, file_name: str) -> None:
        """
        Allow the user to edit a file manually.

        Args:
            file_name (str): The name of the file to edit.
        """
        file_path = os.path.join(self.config.dev_folder, file_name)
        if not os.path.exists(file_path):
            self.logger.warning(f"File not found for editing: {file_name}")
            print(colored(f"File {file_name} does not exist.", "red"))
            return

        content = await self.get_file_contents(file_name)
        print(colored(f"Current content of {file_name}:", "cyan"))
        print(content)
        
        new_content = await self.get_user_input("Enter the new content (press Ctrl+D when finished):\n", multiline=True)
        await self.save_file(file_name, new_content)
        self.logger.info(f"File {file_name} updated manually")
        print(colored(f"File {file_name} updated.", "green"))

    async def run_and_improve_application(self) -> None:
        """Run the application and allow for iterative improvements."""
        self.logger.info("Starting run and improve process")
        while True:
            error_message = await self.run_application()
            if not error_message:
                print(colored("Application ran successfully!", "green"))
                user_feedback = await self.get_user_input("Provide feedback for improvement (or 'quit' to stop): ")
                if user_feedback.lower() == 'quit':
                    break
                await self.update_application_files([], user_feedback)
            else:
                print(colored("Error detected. Attempting to fix...", "yellow"))
                await self.fix_application()
            
            await self.update_requirements()
        self.logger.info("Run and improve process completed")

    async def generate_unit_tests(self, file_name: str, file_content: str) -> str:
        """
        Generate unit tests for a given Python file.

        Args:
            file_name (str): The name of the file to generate tests for.
            file_content (str): The content of the file.

        Returns:
            str: The generated unit test code.
        """
        self.logger.info(f"Generating unit tests for {file_name}")
        system_message = """You are a Python testing expert. Create unit tests for the given Python file.
Your response should be in the following format:
<code>
import unittest
# Your unit test code here
</code>"""
        prompt = f"Create unit tests for the following Python file:\n\nFile: {file_name}\n\nContent:\n{file_content}\n\nEnsure comprehensive test coverage and include edge cases."
        
        response = await self.rate_limited_request(
            model="claude-3-5-sonnet-20240620",
            system=system_message,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        return self.extract_code(response.content[0].text)

    async def create_application_files(self, plan: str) -> None:
        """
        Create application files based on the given plan.

        Args:
            plan (str): The application plan in XML format.
        """
        self.logger.info("Creating application files")
        file_structure = self.parse_file_structure(plan)
        async for file_name, file_description in tqdm_asyncio(file_structure, desc="Creating Files"):
            await self.create_file(file_name, file_description, plan)
            if file_name.endswith('.py') and file_name != '__init__.py':
                await self.create_test_file(file_name)

    async def create_test_file(self, file_name: str) -> None:
        """
        Create a test file for the given Python file.

        Args:
            file_name (str): The name of the Python file to create tests for.
        """
        self.logger.info(f"Creating test file for {file_name}")
        content = await self.get_file_contents(file_name)
        test_content = await self.generate_unit_tests(file_name, content)
        test_file_name = f"test_{file_name}"
        await self.save_file(test_file_name, test_content)
        print(colored(f"Created unit test file: {test_file_name}", "green"))

    async def run_unit_tests(self) -> None:
        """Run all unit tests in the project."""
        self.logger.info("Running unit tests")
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover(self.config.dev_folder)
        test_runner = unittest.TextTestRunner(verbosity=2)
        
        print(colored("Running unit tests...", "yellow"))
        test_result = test_runner.run(test_suite)
        
        if test_result.wasSuccessful():
            self.logger.info("All unit tests passed successfully")
            print(colored("All unit tests passed successfully!", "green"))
        else:
            self.logger.warning(f"Some unit tests failed. Failures: {len(test_result.failures)}, Errors: {len(test_result.errors)}")
            print(colored(f"Some unit tests failed. Failures: {len(test_result.failures)}, Errors: {len(test_result.errors)}", "red"))
            
            for failure in test_result.failures:
                self.logger.error(f"Test case failure: {failure[0]}\nFailure: {failure[1]}")
                print(colored(f"\nTest case: {failure[0]}", "yellow"))
                print(colored(f"Failure: {failure[1]}", "red"))
            
            for error in test_result.errors:
                self.logger.error(f"Test case error: {error[0]}\nError: {error[1]}")
                print(colored(f"\nTest case: {error[0]}", "yellow"))
                print(colored(f"Error: {error[1]}", "red"))

    async def create_file(self, file_name: str, file_description: str, plan: str) -> None:
        """
        Create a new file with the given name and description.

        Args:
            file_name (str): The name of the file to create.
            file_description (str): A description of the file's purpose and contents.
            plan (str): The overall application plan.
        """
        self.logger.info(f"Creating file: {file_name}")
        system_message = """You are a Python expert. Write a Python file based on the given description and overall application plan.
Your response should be in the following format:
<code>
# Your Python code here
</code>"""
        prompt = f"Create file '{file_name}' with description: {file_description}\n\nOverall application plan:\n{plan}"
        response = await self.rate_limited_request(
            model="claude-3-5-sonnet-20240620",
            system=system_message,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        code = self.extract_code(response.content[0].text)
        await self.save_file(file_name, code)

    async def update_file_content(self, file_name: str, content: str, feedback: str, plan: str) -> str:
        """
        Update the content of a file based on user feedback and the application plan.

        Args:
            file_name (str): The name of the file to update.
            content (str): The current content of the file.
            feedback (str): User feedback for updates.
            plan (str): The overall application plan.

        Returns:
            str: The updated file content.
        """
        self.logger.info(f"Updating content of file: {file_name}")
        system_message = """You are a Python expert. Update the given file based on the user's feedback and overall application plan.
Your response should be in the following format:
<code>
# Your updated Python code here
</code>"""
        prompt = f"Update file '{file_name}' based on feedback:\n{feedback}\n\nCurrent content:\n{content}\n\nOverall application plan:\n{plan}"
        response = await self.rate_limited_request(
            model="claude-3-5-sonnet-20240620",
            system=system_message,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        return self.extract_code(response.content[0].text)

    async def fix_file_content(self, file_name: str, content: str, error_message: str, plan: str) -> str:
        """
        Fix the content of a file based on an error message and the application plan.

        Args:
            file_name (str): The name of the file to fix.
            content (str): The current content of the file.
            error_message (str): The error message to address.
            plan (str): The overall application plan.

        Returns:
            str: The fixed file content.
        """
        self.logger.info(f"Fixing content of file: {file_name}")
        system_message = """You are a Python debugging expert. Fix the given file based on the error message and overall application plan.
Your response should be in the following format:
<code>
# Your fixed Python code here
</code>"""
        prompt = f"Fix file '{file_name}' based on error:\n{error_message}\n\nCurrent content:\n{content}\n\nOverall application plan:\n{plan}"
        response = await self.rate_limited_request(
            model="claude-3-5-sonnet-20240620",
            system=system_message,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        return self.extract_code(response.content[0].text)

    async def select_files(self, method: str, feedback: str = "") -> List[str]:
        """
        Select files for updating based on the chosen method.

        Args:
            method (str): The method for file selection ('model' or 'manual').
            feedback (str): User feedback for updates (used in model-based selection).

        Returns:
            List[str]: List of selected file names.
        """
        self.logger.info(f"Selecting files using method: {method}")
        if method == "manual":
            return self.file_selector.select_files()
        else:
            plan = await self.load_application_plan()
            return await self.model_select_files(feedback, plan)

    async def model_select_files(self, feedback: str, plan: str) -> List[str]:
        """
        Use the AI model to select relevant files for updating based on feedback.

        Args:
            feedback (str): User feedback for updates.
            plan (str): The overall application plan.

        Returns:
            List[str]: List of selected file names.
        """
        self.logger.info("Using AI model to select relevant files")
        system_message = """You are an expert in understanding software architecture and user feedback. Select relevant files for update.
Your response should be in the following format:
<relevant_files>
<file>filename1.ext</file>
<file>filename2.ext</file>
</relevant_files>"""
        prompt = f"Select files to update based on feedback:\n{feedback}\n\nApplication plan:\n{plan}"
        response = await self.rate_limited_request(
            model="claude-3-5-sonnet-20240620",
            system=system_message,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        return self.extract_file_list(response.content[0].text)

    async def update_requirements(self) -> None:
        """Update the project requirements."""
        self.logger.info("Updating project requirements")
        self.requirements_manager.update_requirements()

    async def run_application(self) -> Optional[str]:
        """
        Run the application and capture any errors.

        Returns:
            Optional[str]: Error message if an error occurred, None otherwise.
        """
        self.logger.info("Running the application")
        print(colored("Running the application...", "yellow"))
        try:
            result = subprocess.run(
                [sys.executable, f"{self.config.dev_folder}/main.py"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode != 0:
                error_message = f"Error: {result.stderr}"
                self.logger.error(f"Application run failed: {error_message}")
                return error_message
            self.logger.info("Application ran successfully")
            print(colored("Application ran successfully!", "green"))
            return None
        except subprocess.TimeoutExpired:
            error_message = "Error: Application execution timed out"
            self.logger.error(error_message)
            return error_message
        except Exception as e:
            error_message = f"Error: {str(e)}"
            self.logger.error(f"Unexpected error during application run: {error_message}", exc_info=True)
            return error_message

    async def rate_limited_request(self, *args: Any, **kwargs: Any) -> Any:
        """
        Make a rate-limited request to the Anthropic API.

        Returns:
            Any: The response from the API.

        Raises:
            Exception: If the request fails after maximum retries.
        """
        while len(self.request_timestamps) >= self.config.request_limit:
            await asyncio.sleep(0.1)
            self.request_timestamps = [t for t in self.request_timestamps if time.time() - t <= self.config.time_window]

        for attempt in range(self.config.max_retries):
            try:
                response = await self.anthropic_client.messages.create(*args, **kwargs)
                self.request_timestamps.append(time.time())
                return response
            except (RateLimitError, APIError) as e:
                if attempt == self.config.max_retries - 1:
                    self.logger.error(f"API request failed after {self.config.max_retries} attempts: {str(e)}")
                    raise
                delay = self.config.base_delay * (2 ** attempt)
                self.logger.warning(f"API request failed. Retrying in {delay} seconds... (Attempt {attempt + 1}/{self.config.max_retries})")
                await asyncio.sleep(delay)

    async def get_user_input(self, prompt: str, default: str = "", multiline: bool = False) -> str:
        """
        Get input from the user, with optional default value and multiline support.

        Args:
            prompt (str): The prompt to display to the user.
            default (str, optional): Default value if user input is empty.
            multiline (bool, optional): Whether to allow multiline input.

        Returns:
            str: The user's input.
        """
        if multiline:
            print(colored(prompt, "green"))
            return sys.stdin.read().strip()
        else:
            user_input = input(colored(prompt, "green"))
            return user_input if user_input else default

    def extract_xml_plan(self, text: str) -> str:
        """
        Extract the application plan XML from the given text.

        Args:
            text (str): The text containing the XML plan.

        Returns:
            str: The extracted XML plan.
        """
        match = re.search(r'<application_plan>.*?</application_plan>', text, re.DOTALL)
        return match.group(0) if match else ""

    def parse_file_structure(self, plan: str) -> List[Tuple[str, str]]:
        """
        Parse the file structure from the application plan XML.

        Args:
            plan (str): The application plan XML.

        Returns:
            List[Tuple[str, str]]: List of tuples containing file names and descriptions.
        """
        root = ET.fromstring(plan)
        return [(file.find('name').text, file.find('description').text) for file in root.findall('.//file')]

    def extract_code(self, text: str) -> str:
        """
        Extract code from the given text.

        Args:
            text (str): The text containing the code.

        Returns:
            str: The extracted code, or an empty string if no code is found.
        """
        code_blocks = re.findall(r'<code>(.*?)</code>', text, re.DOTALL)
        if not code_blocks:
            self.logger.warning("No code block found in the text")
            return ""
        elif len(code_blocks) > 1:
            self.logger.info(f"Multiple code blocks found. Returning the first one. Total blocks: {len(code_blocks)}")
        
        extracted_code = code_blocks[0].strip()
        if not extracted_code:
            self.logger.warning("Extracted code block is empty")
        
        return extracted_code
    
    async def save_file(self, file_name: str, content: str) -> None:
        """
        Save content to a file asynchronously.

        Args:
            file_name (str): The name of the file to save.
            content (str): The content to write to the file.
        """
        file_path = os.path.join(self.config.dev_folder, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            async with aiofiles.open(file_path, 'w') as f:
                await f.write(content)
            self.logger.info(f"File saved successfully: {file_name}")
        except IOError as e:
            self.logger.error(f"Error saving file {file_name}: {str(e)}")
            print(colored(f"Error saving file {file_name}: {str(e)}", "red"))

    async def get_file_contents(self, file_name: str) -> str:
        """
        Get the contents of a file asynchronously.

        Args:
            file_name (str): The name of the file to read.

        Returns:
            str: The contents of the file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        file_path = os.path.join(self.config.dev_folder, file_name)
        try:
            async with aiofiles.open(file_path, 'r') as f:
                return await f.read()
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_name}")
            raise
        except IOError as e:
            self.logger.error(f"Error reading file {file_name}: {str(e)}")
            raise

    async def save_application_plan(self, plan: str) -> None:
        """
        Save the application plan to a file.

        Args:
            plan (str): The application plan XML to save.
        """
        await self.save_file('application_plan.xml', plan)
        self.logger.info("Application plan saved")

    async def load_application_plan(self) -> str:
        """
        Load the application plan from a file.

        Returns:
            str: The loaded application plan XML.

        Raises:
            FileNotFoundError: If the application plan file does not exist.
        """
        try:
            return await self.get_file_contents('application_plan.xml')
        except FileNotFoundError:
            self.logger.error("Application plan file not found")
            raise

    async def update_application_plan(self, updated_files: List[str]) -> None:
        """
        Update the application plan with information about updated files.

        Args:
            updated_files (List[str]): List of files that were updated.
        """
        try:
            plan = await self.load_application_plan()
            root = ET.fromstring(plan)
            for file in updated_files:
                file_elem = root.find(f".//file[name='{file}']")
                if file_elem is not None:
                    desc_elem = file_elem.find('description')
                    desc_elem.text += " (Updated)"
            updated_plan = ET.tostring(root, encoding='unicode')
            await self.save_application_plan(updated_plan)
            self.logger.info("Application plan updated")
        except Exception as e:
            self.logger.error(f"Error updating application plan: {str(e)}")
            print(colored(f"Error updating application plan: {str(e)}", "red"))

    def extract_error_files(self, error_message: str) -> List[str]:
        """
        Extract file names from an error message.

        Args:
            error_message (str): The error message to parse.

        Returns:
            List[str]: List of file names mentioned in the error message.
        """
        file_pattern = r'File "([^"]+)", line \d+'
        files = re.findall(file_pattern, error_message)
        return [os.path.relpath(f, self.config.dev_folder) for f in files if f.startswith(self.config.dev_folder)]

    def extract_file_list(self, text: str) -> List[str]:
        """
        Extract a list of file names from the given text.

        Args:
            text (str): The text containing file names in XML format.

        Returns:
            List[str]: List of extracted file names.
        """
        return re.findall(r'<file>(.*?)</file>', text)

    async def backup_project(self) -> None:
        """Create a backup of the current project state."""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_path = f"{self.config.backup_folder}_{timestamp}"
        try:
            shutil.copytree(self.config.dev_folder, backup_path)
            self.logger.info(f"Project backed up to {backup_path}")
            print(colored(f"Project backed up to {backup_path}", "green"))
        except Exception as e:
            self.logger.error(f"Error creating backup: {str(e)}")
            print(colored(f"Error creating backup: {str(e)}", "red"))

    async def restore_backup(self) -> None:
        """Restore the project from a selected backup."""
        backups = sorted([d for d in os.listdir() if d.startswith(f"{self.config.backup_folder}_")])
        if not backups:
            self.logger.warning("No backups found")
            print(colored("No backups found.", "yellow"))
            return

        print("Available backups:")
        for i, backup in enumerate(backups):
            print(f"{i + 1}. {backup}")

        choice = await self.get_validated_input("Choose a backup to restore (number) or 'c' to cancel: ", "backup_choice")
        if choice.lower() == 'c':
            return

        try:
            backup_to_restore = backups[int(choice) - 1]
            shutil.rmtree(self.config.dev_folder)
            shutil.copytree(backup_to_restore, self.config.dev_folder)
            self.logger.info(f"Project restored from {backup_to_restore}")
            print(colored(f"Project restored from {backup_to_restore}", "green"))
        except (ValueError, IndexError):
            self.logger.error("Invalid backup selection")
            print(colored("Invalid choice. Restoration cancelled.", "red"))
        except Exception as e:
            self.logger.error(f"Error restoring backup: {str(e)}")
            print(colored(f"Error restoring backup: {str(e)}", "red"))

    async def show_project_structure(self) -> None:
        """Display the current project structure."""
        print(colored("Current project structure:", "cyan"))
        for root, dirs, files in os.walk(self.config.dev_folder):
            level = root.replace(self.config.dev_folder, '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            sub_indent = ' ' * 4 * (level + 1)
            for file in files:
                print(f"{sub_indent}{file}")

    def validate_input(self, input_value: str, input_type: str) -> bool:
        """
        Validate user input based on the expected type.

        Args:
            input_value (str): The input value to validate.
            input_type (str): The expected type of the input.

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        if input_type == "action":
            valid_actions = ["create", "update", "fix", "run", "test", "backup", "restore", "structure", "quit"]
            return input_value.lower() in valid_actions
        elif input_type == "yes_no":
            return input_value.lower() in ["yes", "no", "y", "n"]
        elif input_type == "file_selection":
            return input_value.lower() in ["model", "manual"]
        elif input_type == "backup_choice":
            return input_value.lower() == 'c' or input_value.isdigit()
        elif input_type == "yes_no_refine":
            return input_value.lower() in ["yes", "no", "refine", "y", "n", "r"]
        # Add more validation types as needed
        return True

    async def get_validated_input(self, prompt: str, input_type: str, default: str = "") -> str:
        """
        Get and validate user input.

        Args:
            prompt (str): The prompt to display to the user.
            input_type (str): The type of input to validate.
            default (str, optional): Default value if user input is empty.

        Returns:
            str: The validated user input.
        """
        while True:
            user_input = await self.get_user_input(prompt, default)
            if self.validate_input(user_input, input_type):
                return user_input
            print(colored("Invalid input. Please try again.", "yellow"))

    def commit_changes(self, message: str) -> None:
        """
        Commit changes to the Git repository.

        Args:
            message (str): The commit message.
        """
        try:
            repo = git.Repo(self.config.dev_folder)
            repo.git.add(A=True)
            repo.index.commit(message)
            self.logger.info(f"Changes committed: {message}")
        except Exception as e:
            self.logger.error(f"Error committing changes: {str(e)}")
            print(colored(f"Error committing changes: {str(e)}", "red"))

    def lint_code(self, file_path: str) -> None:
        """
        Run pylint on the specified file.

        Args:
            file_path (str): The path to the file to lint.
        """
        try:
            pylint_opts = ['--disable=C0111', file_path]
            pylint.lint.Run(pylint_opts, exit=False)
            self.logger.info(f"Linting completed for {file_path}")
        except Exception as e:
            self.logger.error(f"Error during linting of {file_path}: {str(e)}")
            print(colored(f"Error during linting of {file_path}: {str(e)}", "red"))

    def sanitize_input(self, user_input: str) -> str:
        """
        Sanitize user input to prevent potential security issues.

        Args:
            user_input (str): The user input to sanitize.

        Returns:
            str: The sanitized user input.
        """
        return html.escape(user_input)

    def mask_sensitive_data(self, data: str) -> str:
        """
        Mask sensitive data in the given string.

        Args:
            data (str): The string potentially containing sensitive data.

        Returns:
            str: The string with sensitive data masked.
        """
        # Replace sensitive data patterns with asterisks
        # This is a simple example; adjust patterns as needed
        masked_data = re.sub(r'\b(?:\d{4}[-\s]?){3}\d{4}\b', '**** **** **** ****', data)
        masked_data = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '****@****.***', masked_data)
        return masked_data

if __name__ == "__main__":
    config = Config.from_file('config.yaml')
    anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    file_selector = FileTreeSelector(config.dev_folder)
    requirements_manager = RequirementsManager(config.dev_folder)
    
    logging.basicConfig(filename=f'{config.logs_folder}/ai_dev_tool.log', 
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('AIAssistedDevTool')
    
    tool = AIAssistedDevTool(config, anthropic_client, file_selector, requirements_manager, logger)
    asyncio.run(tool.run())