import asyncio
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from typing import List, Dict, Tuple
import subprocess

import aiofiles
import aiohttp
from anthropic import AsyncAnthropic, RateLimitError, APIError
from termcolor import colored

# Import custom modules
from file_selector import FileTreeSelector
from requirements_manager import RequirementsManager

class AIAssistedDevTool:
    def __init__(self):
        self.dev_folder = "app"
        self.backup_folder = f"{self.dev_folder}_backup"
        self.logs_folder = f"{self.dev_folder}/logs"
        self.anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.request_limit = 145
        self.time_window = 60  # seconds
        self.max_retries = 20
        self.base_delay = 60  # seconds
        self.request_counter = 0
        self.request_timestamps = []
        self.max_fix_attempts = 5

    async def run(self):
        print(colored("Welcome to AI Assisted Dev Tool!", "cyan"))
        while True:
            action = await self.get_user_input("Choose an action (create/update/fix/run/quit): ", default="create")
            if action == "quit":
                break
            elif action == "create":
                await self.create_application()
            elif action == "update":
                await self.update_application()
            elif action == "fix":
                await self.fix_application()
            elif action == "run":
                await self.run_and_improve_application()


    async def create_application(self):
        user_input = await self.get_user_input("Describe the Python application you want to create: ")
        plan = await self.iterative_planning(user_input)
        await self.save_application_plan(plan)
        await self.create_application_files(plan)
        await self.update_requirements()

    async def iterative_planning(self, initial_input: str, max_iterations: int = 3) -> str:
        current_plan = await self.generate_application_plan(initial_input)
        
        for iteration in range(max_iterations):
            print(colored(f"\nIteration {iteration + 1}/{max_iterations}", "cyan"))
            print(colored("Current Application Plan:", "yellow"))
            print(current_plan)
            
            user_approval = await self.get_user_input("Do you approve this plan? (yes/no/refine): ", default="yes")
            
            if user_approval.lower() == 'yes':
                return current_plan
            elif user_approval.lower() == 'no':
                user_feedback = await self.get_user_input("Please provide feedback for improvement: ")
                current_plan = await self.refine_application_plan(current_plan, user_feedback)
            else:  # refine
                current_plan = await self.refine_application_plan(current_plan)
        
        return current_plan

    async def generate_application_plan(self, user_input: str) -> str:
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

    async def update_application(self):
        feedback = await self.get_user_input("Provide feedback for application update: ")
        selection_method = await self.get_user_input("Choose file selection method (model/manual): ", default="model")
        files_to_update = await self.select_files(selection_method, feedback)
        await self.update_application_files(files_to_update, feedback)
        await self.update_requirements()

    async def fix_application(self):
        for attempt in range(self.max_fix_attempts):
            error_message = await self.run_application()
            if not error_message:
                print(colored(f"Application fixed successfully after {attempt + 1} attempts!", "green"))
                return
            
            print(colored(f"Fix attempt {attempt + 1}/{self.max_fix_attempts}", "yellow"))
            await self.fix_application_files(error_message)
            await self.update_requirements()
        
        print(colored(f"Failed to fix the application after {self.max_fix_attempts} attempts.", "red"))
        user_choice = await self.get_user_input("Do you want to try manual fixing? (yes/no): ", default="yes")
        if user_choice.lower() == "yes":
            await self.manual_fix()

    async def manual_fix(self):
        while True:
            error_message = await self.run_application()
            if not error_message:
                print(colored("Application fixed successfully!", "green"))
                return
            
            print(colored("Current error:", "red"))
            print(error_message)
            
            file_to_edit = await self.get_user_input("Enter the file name to edit (or 'quit' to stop): ")
            if file_to_edit.lower() == 'quit':
                break
            
            await self.edit_file(file_to_edit)
            await self.update_requirements()

    async def edit_file(self, file_name):
        file_path = os.path.join(self.dev_folder, file_name)
        if not os.path.exists(file_path):
            print(colored(f"File {file_name} does not exist.", "red"))
            return

        content = await self.get_file_contents(file_name)
        print(colored(f"Current content of {file_name}:", "cyan"))
        print(content)
        
        new_content = await self.get_user_input("Enter the new content (press Ctrl+D when finished):\n", multiline=True)
        await self.save_file(file_name, new_content)
        print(colored(f"File {file_name} updated.", "green"))

    async def run_and_improve_application(self):
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

    async def generate_application_plan(self, user_input: str) -> str:
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


    async def generate_unit_tests(self, file_name: str, file_content: str) -> str:
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

    async def create_application_files(self, plan: str):
        file_structure = self.parse_file_structure(plan)
        for file_name, file_description in file_structure:
            await self.create_file(file_name, file_description, plan)
            if file_name.endswith('.py') and file_name != '__init__.py':
                await self.create_test_file(file_name)

    async def create_test_file(self, file_name: str):
        content = await self.get_file_contents(file_name)
        test_content = await self.generate_unit_tests(file_name, content)
        test_file_name = f"test_{file_name}"
        await self.save_file(test_file_name, test_content)
        print(colored(f"Created unit test file: {test_file_name}", "green"))

    async def run_unit_tests(self):
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover(self.dev_folder)
        test_runner = unittest.TextTestRunner(verbosity=2)
        
        print(colored("Running unit tests...", "yellow"))
        test_result = test_runner.run(test_suite)
        
        if test_result.wasSuccessful():
            print(colored("All unit tests passed successfully!", "green"))
        else:
            print(colored(f"Some unit tests failed. Failures: {len(test_result.failures)}, Errors: {len(test_result.errors)}", "red"))
            
            for failure in test_result.failures:
                print(colored(f"\nTest case: {failure[0]}", "yellow"))
                print(colored(f"Failure: {failure[1]}", "red"))
            
            for error in test_result.errors:
                print(colored(f"\nTest case: {error[0]}", "yellow"))
                print(colored(f"Error: {error[1]}", "red"))

    async def create_file(self, file_name: str, file_description: str, plan: str):
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

    async def update_application_files(self, files: List[str], feedback: str):
        plan = await self.load_application_plan()
        if not files:  # If no specific files are provided, update all files
            files = [f for f in os.listdir(self.dev_folder) if f.endswith('.py')]
        for file in files:
            content = await self.get_file_contents(file)
            updated_content = await self.update_file_content(file, content, feedback, plan)
            await self.save_file(file, updated_content)
            await self.create_test_file(file)  # Update or create test file
        await self.update_application_plan(files)
        await self.run_unit_tests()  # Run unit tests after updates

    async def update_file_content(self, file_name: str, content: str, feedback: str, plan: str) -> str:
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

    async def fix_application(self):
        for attempt in range(self.max_fix_attempts):
            error_message = await self.run_application()
            if not error_message:
                print(colored(f"Application fixed successfully after {attempt + 1} attempts!", "green"))
                await self.run_unit_tests()  # Run unit tests after successful fix
                return
            
            print(colored(f"Fix attempt {attempt + 1}/{self.max_fix_attempts}", "yellow"))
            await self.fix_application_files(error_message)
            await self.update_requirements()
        
        print(colored(f"Failed to fix the application after {self.max_fix_attempts} attempts.", "red"))
        user_choice = await self.get_user_input("Do you want to try manual fixing? (yes/no): ", default="yes")
        if user_choice.lower() == "yes":
            await self.manual_fix()

    async def fix_file_content(self, file_name: str, content: str, error_message: str, plan: str) -> str:
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
        if method == "manual":
            return FileTreeSelector(self.dev_folder).select_files()
        else:
            plan = await self.load_application_plan()
            return await self.model_select_files(feedback, plan)

    async def model_select_files(self, feedback: str, plan: str) -> List[str]:
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

    async def update_requirements(self):
        RequirementsManager(self.dev_folder).update_requirements()

    async def run_application(self) -> str:
        print(colored("Running the application...", "yellow"))
        try:
            result = subprocess.run(
                [sys.executable, f"{self.dev_folder}/main.py"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode != 0:
                return f"Error: {result.stderr}"
            print(colored("Application ran successfully!", "green"))
            return None
        except subprocess.TimeoutExpired:
            return "Error: Application execution timed out"
        except Exception as e:
            return f"Error: {str(e)}"

    async def rate_limited_request(self, *args, **kwargs):
        while len(self.request_timestamps) >= self.request_limit:
            await asyncio.sleep(0.1)
            self.request_timestamps = [t for t in self.request_timestamps if time.time() - t <= self.time_window]

        for attempt in range(self.max_retries):
            try:
                response = await self.anthropic_client.messages.create(*args, **kwargs)
                self.request_timestamps.append(time.time())
                return response
            except (RateLimitError, APIError) as e:
                if attempt == self.max_retries - 1:
                    raise
                delay = self.base_delay * (2 ** attempt)
                await asyncio.sleep(delay)

    # Helper methods
    async def get_user_input(self, prompt: str, default: str = "", multiline: bool = False) -> str:
        if multiline:
            print(colored(prompt, "green"))
            return sys.stdin.read().strip()
        else:
            user_input = input(colored(prompt, "green"))
            return user_input if user_input else default

    def extract_xml_plan(self, text: str) -> str:
        match = re.search(r'<application_plan>.*?</application_plan>', text, re.DOTALL)
        return match.group(0) if match else ""

    def parse_file_structure(self, plan: str) -> List[Tuple[str, str]]:
        root = ET.fromstring(plan)
        return [(file.find('name').text, file.find('description').text) for file in root.findall('.//file')]

    def extract_code(self, text: str) -> str:
        match = re.search(r'<code>(.*?)</code>', text, re.DOTALL)
        return match.group(1) if match else text

    async def save_file(self, file_name: str, content: str):
        file_path = os.path.join(self.dev_folder, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(content)

    async def get_file_contents(self, file_name: str) -> str:
        file_path = os.path.join(self.dev_folder, file_name)
        async with aiofiles.open(file_path, 'r') as f:
            return await f.read()

    async def save_application_plan(self, plan: str):
        await self.save_file('application_plan.xml', plan)

    async def load_application_plan(self) -> str:
        return await self.get_file_contents('application_plan.xml')

    async def update_application_plan(self, updated_files: List[str]):
        plan = await self.load_application_plan()
        root = ET.fromstring(plan)
        for file in updated_files:
            file_elem = root.find(f".//file[name='{file}']")
            if file_elem is not None:
                desc_elem = file_elem.find('description')
                desc_elem.text += " (Updated)"
        updated_plan = ET.tostring(root, encoding='unicode')
        await self.save_application_plan(updated_plan)

    def extract_error_files(self, error_message: str) -> List[str]:
        file_pattern = r'File "([^"]+)", line \d+'
        files = re.findall(file_pattern, error_message)
        return [os.path.relpath(f, self.dev_folder) for f in files if f.startswith(self.dev_folder)]

    def extract_file_list(self, text: str) -> List[str]:
        return re.findall(r'<file>(.*?)</file>', text)

    async def backup_project(self):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_path = f"{self.backup_folder}_{timestamp}"
        shutil.copytree(self.dev_folder, backup_path)
        print(colored(f"Project backed up to {backup_path}", "green"))

    async def restore_backup(self):
        backups = sorted([d for d in os.listdir() if d.startswith(f"{self.backup_folder}_")])
        if not backups:
            print(colored("No backups found.", "yellow"))
            return

        print("Available backups:")
        for i, backup in enumerate(backups):
            print(f"{i + 1}. {backup}")

        choice = await self.get_user_input("Choose a backup to restore (number) or 'c' to cancel: ")
        if choice.lower() == 'c':
            return

        try:
            backup_to_restore = backups[int(choice) - 1]
            shutil.rmtree(self.dev_folder)
            shutil.copytree(backup_to_restore, self.dev_folder)
            print(colored(f"Project restored from {backup_to_restore}", "green"))
        except (ValueError, IndexError):
            print(colored("Invalid choice. Restoration cancelled.", "red"))

    async def show_project_structure(self):
        print(colored("Current project structure:", "cyan"))
        for root, dirs, files in os.walk(self.dev_folder):
            level = root.replace(self.dev_folder, '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            sub_indent = ' ' * 4 * (level + 1)
            for file in files:
                print(f"{sub_indent}{file}")


    async def run(self):
        print(colored("Welcome to AI Assisted Dev Tool!", "cyan"))
        while True:
            action = await self.get_user_input(
                "Choose an action (create/update/fix/run/test/backup/restore/structure/quit): ",
                default="create"
            )
            try:
                if action == "quit":
                    break
                elif action == "create":
                    await self.create_application()
                elif action == "update":
                    await self.update_application()
                elif action == "fix":
                    await self.fix_application()
                elif action == "run":
                    await self.run_and_improve_application()
                elif action == "test":
                    await self.run_unit_tests()
                elif action == "backup":
                    await self.backup_project()
                elif action == "restore":
                    await self.restore_backup()
                elif action == "structure":
                    await self.show_project_structure()
                else:
                    print(colored("Invalid action. Please try again.", "yellow"))
            except Exception as e:
                print(colored(f"An error occurred: {str(e)}", "red"))
                print("Traceback:")
                traceback.print_exc()
                user_choice = await self.get_user_input("Do you want to continue? (yes/no): ", default="yes")
                if user_choice.lower() != "yes":
                    break

        print(colored("Thank you for using AI Assisted Dev Tool. Goodbye!", "cyan"))

if __name__ == "__main__":
    tool = AIAssistedDevTool()
    asyncio.run(tool.run())
                            
