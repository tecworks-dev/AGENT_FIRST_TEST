import asyncio
from anthropic import AsyncAnthropic, RateLimitError, APIError
import os
import xml.etree.ElementTree as ET
import re
from termcolor import colored
import subprocess
import traceback
import sys
import time
from requirements import do_requirements
import aiofiles
import shutil
import time
from collections import deque

show_user_consent = False
FILE_EXTENSIONS = (
    '.py', '.html', '.js', '.json', '.css', '.yaml', '.xml',
    '.java', '.mjs', '.tsx', '.ts', '.jsx', '.vue', '.svelte',
    '.php', '.go', '.cs', '.pyw', '.sh', '.bat', '.ps1',
    '.c', '.h', '.cpp'
)
requirements_installed = False
PRINT_RESPONSE = True
REQUEST_LIMIT = 145
TIME_WINDOW = 60  # seconds
MAX_RETRIES = 20 # number of ai retrys api issue
BASE_DELAY = 60  # second
REQUEST_COUNTER = 0
max_attempts = 5 # create application

# Function to check for consecutive user messages and add a separator
def add_separator_between_consecutive_user_messages(messages):
    for i in range(len(messages) - 1):
        if messages[i]["role"] == "user" and messages[i+1]["role"] == "user":
            messages.insert(i+1, {"role": "assistant", "content": " ..."})
    return messages



# Function for planner agents to discuss and plan the project
async def plan_project(user_input, iterations):
    system_message_1 = f"""You are a logical, critical application design expert. Your role is to discuss and plan with a critical and rigorous eye, a python application project based on user input. One of the main goals is to review the logic of the code to ensure a user-friendly and enjoyable application experience for the user. 
Focus on application mechanics, structure, and overall design and function and method inputs inputs(proper inputs and number of inputs) and returns of functions and methods. Do not suggest external media files or images. make sure no code files need any external files. All assets must be generated, for images or media use python place holder files. Critical objective is to keep the project structure simple while making sure no circular imports or broken imports occur. No need to discuss timelines or git commands. Main purpose is to review and evaluate the project structure so that when the final files and their descriptions are prepared the code will function without any errors. 
Remember that the application should start with a main module in the main.py file.
here is the user input: {user_input}
"""
    
    system_message_2 = f"""You are a logical, critical Python architecture expert. Your role is to discuss and plan with a critical and rigorous eye the file structure for a python application project. One of the main goals is to review the logic of the code to ensure a user-friendly and enjoyable application play experience for the user.
Focus on code organization, modularity, and best practices for functions and methods (proper inputs and number of inputs) and their returns. Make sure no code files need any external files. All assets must be generated, for images or media use python place holder files. Critical objective is to keep the project structure simple while making sure no circular imports or broken imports occur. No need to discuss timelines or git commands. Main purpose is to review and evaluate the project structure so that when the final files and their descriptions are prepared the code will function without any errors.
Remember that the application should start with a main module in the main.py file.
Here is the user input: {user_input}
"""
    messages_1 = [{"role": "user", "content": f"please plan a python application project based on the following user input: {user_input}. Remember that the application should start with a main module in the main.py file."}]
    messages_2 = []

    for i in range(iterations):
        print(colored(f"Iteration {i+1} of {iterations} planning iterations", "yellow"))
        is_final = i == iterations - 1

        if is_final:

            messages_1.append({"role": "user", "content": "this is the final iteration. Please provide your final application structure along with file structure you think is best for the application. return file paths with file names and descriptions. make sure to mention what imports are necessary for each file. Critical objective is to keep the project well structured while making sure no circular imports or broken imports occur. ensure function and method inputs are accurate as well as their returns. Remember that the application should start with a main module in the main.py file(main shouldn't take any arguments)."})

            messages_1 = add_separator_between_consecutive_user_messages(messages_1)

            response_1 = await rate_limited_request(
                model="claude-3-5-sonnet-20240620",
                system=system_message_1,
                messages=messages_1,
                max_tokens=4000
            )

            if PRINT_RESPONSE:
                print(colored(system_message_1, "magenta"))
                print(colored(messages_1, "magenta"))
                print(colored(response_1.content[0].text, "green"))
            messages_1.append({"role": "assistant", "content": response_1.content[0].text})
            messages_2.append({"role": "user", "content": response_1.content[0].text})

            if is_final:
                messages_2. append({"role": "user", "content": "This is the final iteration. Please review the application design carefully and provide your final response  in the following XML format:\n<application_plan>\n <overview>Overall application description</overview>\n <mechanics>Key application mechanics</mechanics>\n <files>\n <file>\n    <name>filename.ext</name>\n  <description>File purpose and contents</description>\n <file> element for each file -- >\n </files>\n</application_plan>. please return file names including there path and descriptions along with simple description of functions and methods along with their inputs and returns. Please return descriptions for all files. make sure to mention what imports are necessary for each file. Critical objective is to keep the project structure simple while making sure no circular imports or broken imports occur as well as the clear and accurate definition of function and method inputs. Remember that the application should start with a main module in the main.py file(main shouldn't take any arguments)."})

            messages_2 = add_separator_between_consecutive_user_messages(messages_2)

            response_2 = await rate_limited_request(
                model="claude-3-5-sonnet-20240620",
                system=system_message_2,
                messages=messages_2,
                max_tokens=4000
            )
            
            if PRINT_RESPONSE:
                print(colored(system_message_2, "magenta"))
                print(colored(messages_2, "magenta"))
                print(colored(response_2.content[0].text, "blue"))
            messages_2.append({"role": "assistant", "content": response_2.content[0].text})
            messages_1.append({"role": "user", "content": response_2.content[0].text})

    # Extract the XML content from the response
    xml_content = re.search(r'<application_plan>.*?</application_plan>', response_2.content[0].text, re.DOTALL)
    if xml_content:
        return xml_content.group(0)
    else:
        raise ValueError("No valid XML content found in the response")

# Function to call Claude 3.5 and write files
async def agent_write_file(file_name, file_description, application_plan):
    print(colored(f"Creating file '{file_name}' ... ", "yellow"))
    # create application folder if it doesnt exist
    os.makedirs("app", exist_ok=True)
    
    system_message = """You are a Python application development expert. Your task is to write a error free Python file for a python application application based on the overall project structure. Always return the full contents of the file. One of the main goals is to review the logic of the code to ensure a userfriendly and enjoyable application play experience for the user.
Do not include any external media files or images in your code instead include placeholders files with no content.
Write clean, well-commented code that follows best practices.
Add comment at top of file with purpose of the file and short description.
Make sure that any error is logged appropriately to the terminal use traceback.
Always add debugging statements to your code if DEBUG = True, DEBUG = True by default.
The application should start with a main module in the main.py file(main shouldn't take any arguments).
return the code for the file in the following format:
<code>
file code
</code>
"""
    if file_name == "main.py":
        main = ",  and should have a comment IMPORTANT: do not remove main function as automated test will fail IMPORTANT: do not remove this comment"
    else:
        main = ""
    prompt = f"""Create a Python file named '{file_name}' with the following description: {file_description}

    Here's the overall application plan which you should follow while writing the file:
    {application_plan}

    Remember, the application should start with a main module in the main.py file(main shouldn't take any arguments{main}). Always return the full contents of the file
    """
    
    response = await rate_limited_request(
        model="claude-3-5-sonnet-20240620",
        system=system_message,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
        )

    code = response.content[0].text
    code = code.split("<code>")[1].split("</code>")[0]
    
    # remove old backup folder then duplicate app folder to backup
    if os.path.exists("app_backup"):
        shutil.rmtree("app_backup")
    if os.path.exists("app"):
        shutil.copytree("app", "app_backup")
    dirname = os.path.dirname(os.path.join(os.path.dirname(__file__), f"app/{file_name}"))
    os.makedirs(dirname, exist_ok=True)
    with open(f"app/{file_name}", "w", encoding="utf-8") as f:
        f.write(code)

    print(f"File '{file_name}' has been created.")

# Function to parse file structure from planner agents' discussion

def parse_file_structure(xml_string):
    root = ET.fromstring(xml_string)
    files = []
    
    def parse_folder(element, current_path=''):
        for child in element:
            if child.tag == 'folder':
                new_path = os.path.join(current_path, child.text)
                parse_folder(child, new_path)
            elif child.tag == 'file':
                name = os.path.join(current_path, child.find('name').text)
                description = child.find('description').text
                files.append((name, description))
    
    parse_folder(root.find('.//files'))
    return files

# Function to fix errors in the application files
# Function to run the application and capture errors

async def run_application():
    global requirements_installed
    print(colored("Running the application ... ", "yellow"))
    full_output = ""
    full_error = ""
    try:
        do_requirements("./app")
        if not requirements_installed:
            colored("installing requirements ...", "yellow")
            process = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "./app/requirements.txt"], timeout=60)
            colored("requirements installed.", "yellow")
            requirements_installed = True
    except:
        pass

    try:
        # change directory to app if current folder is not app
        process = subprocess.Popen(
            [sys.executable, "-c", "import sys;  import main; main.main();"],
            cwd="app",
            bufsize=1,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print(colored("application is running. Please play the application. Close the window to stop.", "cyan"))

        while True:
            try:
                output = process.stdout.readline()
                error = process.stderr.readline()

                if output:
                    full_output += output
                    print(output.strip())
                if error:
                    full_error += error
                    print(colored(f"Runtime error: {error.strip()}", "red"))

                if process.poll() is not None:
                    break

                await asyncio.sleep(0.1)
            except KeyboardInterrupt:
                print(colored("\napplication stopped by user.", "yellow"))
                process.terminate()
                break

        stdout, stderr = process.communicate()
        full_output += stdout
        full_error += stderr
        
        if process.returncode != 0:
            full_error += f"\nProcess exited with return code {process.returncode}"
        full_error = full_error.replace(os.getcwd() + "/", "")
        full_output = full_output.replace(os.getcwd() + "/", "")

    except Exception as e:
        full_error += f"\nError running application: {str(e)}\n{traceback.format_exc()}"
        full_error = full_error.replace(os.getcwd() + "/", "")
        full_output = full_output.replace(os.getcwd() + "/", "")

    error_summary = ""
    if full_error:
        error_summary += f"Runtime errors:\n{full_error}\n"
    if "error" in full_output.lower() or "exception" in full_output.lower():
        error_summary += f"Possible errors in output: \n{full_output}\n"

    if error_summary:
        print(colored(error_summary, "red"))
        error_summary.strip("""NameError: name 'diagnostic_report' is not define""")
        return error_summary
    else:
        print(colored("application completed successfully", "green"))
    return None

async def run_unittests(file_contents):
    print(colored("Creating unit tests ... ", "yellow"))
    system_message = """You are a full stack expert developer:"""
    prompt = f"""Please create unit tests for the following Python code:\n\n{file_contents}

Based on the application_plan.xml please generate a debugging diagnostic write a full unittest script to test all classes and functions and produce a report of any unexpected ensure that all, be sure to order put the tests in a logical order be carefully to include required dependence for each test, Use try except and trackback to output the errors. Important make sure to output details and reason for test before each test and the filename the test is for between tests. make sure that the the script uses def main() with no arguments. Only print output details for tests that fail or errors

Return the updated file contents in the following format only for the files that require updates:
<file name="diagnostic_report.py">
updated_file_contents
</file>    
    """
    response = await rate_limited_request(
        model="claude-3-5-sonnet-20240620",
        system=system_message,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    corrected_files = re.findall(r'<file name="(.*?)">(.*?)</file>', response.content[0].text, re.DOTALL)
        if corrected_files:
            for filename, content in corrected_files:
                file_path = os.path.join('app', filename)
                dir_name = os.path.dirname(file_path)
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name, exist_ok=True)
                # Write the file
                with open(file_path, 'w', encoding="utf-8") as f:
                    f.write(content.strip())
                print(f"Updated file: {file_path}")
    
    try:
        # change directory to app if current folder is not app
        process = subprocess.Popen(
            [sys.executable, "-c", "import sys;  import main; diagnostic_report.main();"],
            cwd="app",
            bufsize=1,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        

        while True:
            try:
                output = process.stdout.readline()
                error = process.stderr.readline()

                if output:
                    full_output += output
                    print(output.strip())
                if error:
                    full_error += error
                    print(colored(f"Runtime error: {error.strip()}", "red"))

                if process.poll() is not None:
                    break

                await asyncio.sleep(0.1)
            except KeyboardInterrupt:
                process.terminate()
                break

        stdout, stderr = process.communicate()
        full_output += stdout
        full_error += stderr
        
        if process.returncode != 0:
            full_error += f"\nProcess exited with return code {process.returncode}"
        full_error = full_error.replace(os.getcwd() + "/", "")
        full_output = full_output.replace(os.getcwd() + "/", "")

    except Exception as e:
        full_error += f"\nError running application: {str(e)}\n{traceback.format_exc()}"
        full_error = full_error.replace(os.getcwd() + "/", "")
        full_output = full_output.replace(os.getcwd() + "/", "")

    error_summary = ""
    if full_error:
        error_summary += f"Runtime errors:\n{full_error}\n"
    if "error" in full_output.lower() or "exception" in full_output.lower():
        error_summary += f"Possible errors in output: \n{full_output}\n"

    if error_summary:
        print(colored(error_summary, "red"))
        return error_summary
    else:
        print(colored("Unittest completed", "green"))
    return None
# Function to fix errors in the application files
async def fix_application_files(error_message):
    print(colored("Attempting to fix the error ... ", "yellow"))

    # Extract all filenames from the error message
    pattern = r'\b([^/\\:*?"<>|\r\n]+(?:' + '|'.join(re.escape(ext) for ext in FILE_EXTENSIONS) + r'))\b'
    error_filenames = re.findall(pattern, error_message)
    # error_filenames = re.findall(r'\b([^/\\:*?"<>|\r\n]+\.py)\b', error_message)
    error_filenames = list(set(error_filenames)) # Remove duplicates

    # Remove agent_application_maker.py from the list if present
    error_filenames = [f for f in error_filenames if f != 'agent_application_maker.py']

    file_contents = {}

    encodings = ['utf-8', 'latin-1', 'ascii']
    
    for root, dirs, files in os.walk('app'):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
            dirs.remove('__pycache__')  # prevent os.walk from recursing into it
        dirs[:] = [d for d in dirs if d not in ['node_modules', 'venv', '.venv', 'env', '.env', 'build', 'dist']]    
        ignored_filenames = ["__init__.py", "agent_application_maker.py"]
        for filename in files:
            if filename.endswith(FILE_EXTENSIONS ) and filename not in ignored_filenames:
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, 'app')
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            file_contents[relative_path] = f.read()
                        print(f"Successfully read {relative_path} with {encoding} encoding")
                        break
                    except UnicodeDecodeError:
                        if encoding == encodings[-1]:
                            print(f"Error: Unable to read {relative_path} with any of the attempted encodings")
                    except Exception as e:
                        print(f"Error reading {relative_path}: {str(e)}")
                        break
    comment = ""
    if error_filenames:
        print(f"Error occurred in files: {', '.join(error_filenames)}")
    else:
        print("""Could not determine specific files causing the error 
Please provide a comment about the error (press ctrl+z enter to finish): """)
        comment = "\n\n" + get_multiline_input()
    diagnostics_report = await run_unittests( file_contents)
    print(f"Sending all files for error correction in 3 seconds. Files: {','.join(file_contents.keys())}")
    time.sleep(3)
    system_message = """You are a Python application development expert. Your task is to fix errors in python application project files.
Analyze the error message and the contents of the application files, then provide the corrected versions of the files.
Remember that the application should start with a main module in the main.py file(main shouldn't take any arguments).
carefully reason about the error in a step by step manner ahead of providing the corrected code. No external files are allowed within the application. One of the main goals is to review the logic of the code to ensure a user-friendly and enjoyable application play experience for the user.
<reasoning>
reasoning about the error
</reasoning>
Return the corrected file contents in the following format only for the files that requires correction:
<file name="path/to/filename.ext">
corrected_file_contents
</file>
"""

    prompt = f"""An error occurred while running the python application project. Here's the error message:
    
    {error_message}

Here are the contents of the files involved in the error:

    {file_contents}

Here is the output of diagnostics_report.py unittest:

    {diagnostics_report}
    
Here a reminder of the error:
    
    {error_message}{comment}
    
Please analyze the error and provide corrected versions of the files to resolve the error. return the full content of the files Remember that the application should start with a main module in the main.py file(main shouldn't take any arguments)."""

    response = await rate_limited_request(
        model="claude-3-5-sonnet-20240620",
        system=system_message,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    if PRINT_RESPONSE:
        print(colored(system_message, "magenta"))
        print(colored(prompt, "magenta"))
        if response.content[0].text:
            print(colored(response.content[0].text, "magenta"))
        else:
            print(response)
        # Extract corrected file contents from the response
    corrected_files = re.findall(r'<file name="(.*?)">(.*?)</file>', response.content[0].text, re.DOTALL)
    if corrected_files:
        # remove old backup folder then duplicate app folder to backup
        if os.path.exists("app_backup"):
            shutil.rmtree("app_backup")
        if os.path.exists("app"):
            shutil.copytree("app", "app_backup")
        for filename, content in corrected_files:
            file_path = os.path.join('app', filename)
            dir_name = os.path.dirname(file_path)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
            # Write the file
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(content.strip())
            print(f"Updated file: {file_path}")
            
            # Retry mechanism for reading the file back
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    await asyncio.sleep(0.5)  # Short delay before reading
                    with open(file_path, 'r', encoding="utf-8") as f:
                        written_content = f.read()
                    if written_content.strip() == content.strip():
                        print(f"File {file_path} written and verified successfully.")
                        break
                    else:
                        print(f"Warning: File {file_path} content mismatch. Retrying...")
                except Exception as e:
                    print(f"Error reading {file_path} (attempt {attempt + 1}/{max_retries}): {str(e)}")
                    if attempt == max_retries - 1:
                        print(f"Failed to verify {file_path} after {max_retries} attempts.")
            
        # Clear Python's module cache for the app directory
        for module_name in list(sys.modules.keys()):
            if module_name.startswith('app.'):
                del sys.modules[module_name]
        
        await asyncio.sleep(1)  # Add a small delay to ensure files are fully written
    else:
        print("No corrected file content found in the response.")

        
        

async def update_application_files(user_feedback):
    # Gather all existing application files
    application_files = {}
    encodings = ['utf-8', 'latin-1', 'ascii']

    for root, dirs, files in os.walk('app'):
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
            dirs.remove('__pycache__')  # prevent os.walk from recursing into it
        # Remove other directories we want to skip
        dirs[:] = [d for d in dirs if d not in ['node_modules', 'venv', '.venv', 'env', '.env', 'build', 'dist']]
        
        for filename in files:
            if filename.endswith(FILE_EXTENSIONS ):
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, 'app')
                for encoding in encodings:
                    try:
                        async with aiofiles.open(file_path, 'r', encoding=encoding) as f:
                            content = await f.read()
                        application_files[relative_path] = content
                        print(f"Successfully read {relative_path} with {encoding} encoding")
                        break
                    except UnicodeDecodeError:
                        if encoding == encodings[-1]:
                            print(f"Error: Unable to read {relative_path} with any of the attempted encodings")
                    except Exception as e:
                        print(f"Error reading {relative_path}: {str(e)}")
                        break

            # Prepare the prompt for the API
    file_contents = "\n\n".join([f"File: {filename}\n\n{content}" for filename, content in application_files.items()])

    prompt = f"""Here are the current contents of the python application project files:

{file_contents}

The user has provided the following feedback about the application:

{user_feedback}

Please analyze the feedback ane suggest updates to the application files to address the user's comments.
Provide the full updated content for any files that need changes.
Return the updated file contents in the following format only for the files that require updates:
<file name="path/to/filename.ext">
updated_file_contents
</file>
always return the full content of the files
application should start with a main module in the main.py file(main shouldn't take any arguments).
"""

    system_message = """You are an expert Python and python application developer. Your task is to update a python application project based on user feedback.
Analyze the current application files and the user's feedback, then provide updated versions of any files that need changes to address the feedback. Always return the full content of the files. One of the main goals is to review the logic of the code to ensure a user-friendly and enjoyable application play experience for the user. no external files are allowed within the application
Ensure that your changes are consistent with the existing code structure and python application best practices. Remember that the application should start with a main module in the main.py file(main shouldn't take any arguments)."""
        
    response = await rate_limited_request(
        model="claude-3-5-sonnet-20240620",
        system=system_message,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    
    if PRINT_RESPONSE:
        print(colored(system_message, "magenta"))
        print(colored(prompt, "magenta"))
        print(colored(response.content[0].text, "magenta"))
        
        # Extract updated file contents from the response
        updated_files = re.findall(r'<file name="(.*?)">(.*?)</file>', response.content[0].text, re.DOTALL)
        if updated_files:
            # remove old backup folder then duplicate app folder to backup
            if os.path.exists("app_backup"):
                shutil.rmtree("app_backup")
            if os.path.exists("app"):
                shutil.copytree("app", "app_backup")
            for filename, content in updated_files:
                file_path = os.path.join('app', filename)
                dir_name = os.path.dirname(file_path)
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name, exist_ok=True)
                with open(file_path, 'w', encoding="utf-8") as f:
                    f.write(content.strip())
                print(f"Updated file: {filename}")

                # Ensure the file is written correctly by reading it back
                with open(file_path, 'r') as f:
                    written_content = f.read()
                if written_content.strip() != content.strip():
                    print(f"Warning: File {filename} may not have been written correctly.")
                    
            # Clear Python's module cache for the app directory
            for module_name in list(sys.modules.keys()):
                if module_name.startswith('app.'):
                    del sys.modules[module_name]

            time.sleep(1) # Add a small delay to ensure files are fully written
        else:
            print("No updates were necessary based on the user's feedback.")


def count_lines_of_code():
    total_lines = 0

    encodings = ['utf-8', 'latin-1', 'ascii']
    
    for root, dirs, files in os.walk('app'):
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
            dirs.remove('__pycache__')  # prevent os.walk from recursing into it
        
        # Remove other directories we want to skip
        dirs[:] = [d for d in dirs if d not in ['node_modules', 'venv', '.venv', 'env', '.env', 'build', 'dist']]
        
        for filename in files:
            if filename.endswith(FILE_EXTENSIONS ):
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, 'app')
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as file:
                            file_lines = sum(1 for line in file if line.strip())
                            total_lines += file_lines
                            print(colored(f"File: {relative_path}, Lines: {file_lines}", "cyan"))
                        print(f"Successfully read {relative_path} with {encoding} encoding")
                        break
                    except UnicodeDecodeError:
                        if encoding == encodings[-1]:
                            print(colored(f"Error: Unable to read {relative_path} with any of the attempted encodings", "red"))
                    except Exception as e:
                        print(colored(f"Error reading {relative_path}: {str(e)}", "red"))
                        break

    print(colored(f"Total lines of code written by agent_application_maker: {total_lines}", "yellow"))
    
def get_multiline_input():
    print("Enter your multiline input. Press Ctrl+D (Unix) or Ctrl+Z (Windows) followed by Enter to finish:")
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    return "\n".join(lines)
# Main function to orchestrate the application creation process
async def create_application(fix):
    global max_attempts
    if fix == "2":
        user_input = input(colored("Describe the python application application you want to create: ", "green"))
        system_message = f"""You are a prompt rewrite the following:"""
        response = await rate_limited_request(
            model="claude-3-5-sonnet-20240620",
            system=system_message,
            messages=[{"role": "user", "content": user_input}],
            max_tokens=4000
        )
        user_input = response.content[0].text
        
        if PRINT_RESPONSE:
            print(colored(system_message, "magenta"))
            print(colored(user_input, "green"))
        while True:
            iterations = input(colored("How many planning iterations do you want? Default is 2: ", "green"))
            if iterations == "" or iterations == None:
                iterations = 2
                break
            else:
                # check if iterations is interger break
                try:
                    iterations = int(iterations)
                    break
                except ValueError:
                    print("Please enter a valid integer.")
                    continue  # Skip the rest of the loop and go back to the start
    if fix == "2" or fix == "4":
        if fix == "4":
            final_plan = get_multiline_input()
        else:
            print("Planning the application structure ... ")
            final_plan = await plan_project(user_input, iterations)
        print (colored("writing application plan to application_plan.xml", "yellow"))
        os.makedirs("app", exist_ok=True)
        with open("app/application_plan.xml", "w", encoding="utf-8") as f:
            f.write(final_plan)

        file_structure = parse_file_structure(final_plan)


        print("Creating application files ... ")

        tasks = []
        for file_name, file_description in file_structure:
            task = asyncio.create_task(agent_write_file(file_name, file_description, final_plan))
            tasks.append(task)
        
        await asyncio.gather(*tasks)

        count_lines_of_code()

        print("application creation complete!")
        print("Final application plan:")
    #else:
        
    # print(final_plan)
    attempt = 0
    # Run the application in a loop to catch and fix errors, then enter feedback loop
    attempt_to_fix = 0
    while True:
        if not fix == "3":
            error_message = await run_application()
            fix = "1"
        else:
            error_message = None
        if error_message is None:
            print(colored("application ran successfully!", "green"))
            feedback = input(colored("Please provide your feedback on the application for iterative improvement (or type 'quit' to exit): ", "green"))
            if feedback.lower() == 'quit':
                break
            print("Updating application based on feedback ... ")
            await update_application_files(feedback)
            count_lines_of_code()
        else:
            print(colored(f"Error detected: {error_message}", "red"))
            if ".wav" in error_message or ".png" in error_message or ".jpg" in error_message or ".mp3" in  error_message:
                input(colored("Missing media file please and it then press Enter if ?__debugger is not in the error will attempt to fix ", "red"))
                if not "?__debugger" in error_message:
                    continue
            if attempt_to_fix == 0:
                attempt_to_fix += 1
                # skip first fix due to requirements
                continue
            if attempt_to_fix > max_attempts:
                feedback = input(colored("Attempt to fix error? (or type 'quit' to exit): ", "green"))
                if feedback.lower() == 'quit':
                    break
            else:
                attempt_to_fix += 1
            
            #for attempt in range(max_attempts):
            attempt += 1
            print(f"Attempt {attempt} to fix the errors ... ")
            await fix_application_files(error_message)
            count_lines_of_code()
            time.sleep(1) # Allow time for files to be written
            # Try running the application again after fixing
            #error_message = await run_application()
            #if error_message is None:
            #    print(colored("Errors fixed successfully!", "green"))
            #    break
            #else:
            #    print(colored(f"Failed to fix all errors after {max_attempts} attempts.", "red"))
            #    user_choice = input(colored("Press Enter to continue error correcting, or type 'no' to quit: ", "yellow")). lower()
            #    
            #    if user_choice == 'no':
            #        return
                


async def rate_limited_request(*args, **kwargs):
    current_time = time.time()
    global REQUEST_COUNTER
    # Remove timestamps older than TIME_WINDOW
    while request_timestamps and current_time - request_timestamps[0] > TIME_WINDOW:
        request_timestamps.popleft()
    
    # If we've reached the limit, wait until enough time has passed
    if len(request_timestamps) >= REQUEST_LIMIT:
        sleep_time = TIME_WINDOW - (current_time - request_timestamps[0])
        if sleep_time > 0:
            print(f"Rate limit reached. Waiting for {sleep_time:.2f} seconds...")
            await asyncio.sleep(sleep_time)
    
    for attempt in range(MAX_RETRIES):
        try:
            # Make the request
            response = await client.messages.create(*args, **kwargs)
                    
            print(f"made {REQUEST_COUNTER} requests")
            REQUEST_COUNTER += 1
            # Add the current timestamp to our list
            request_timestamps.append(time.time())
            
            return response
        
        except RateLimitError as e:
            if attempt < MAX_RETRIES - 1:
                delay = BASE_DELAY * (2 ** attempt)  # Exponential backoff
                print(f"Rate limit exceeded. Retrying in {delay} seconds... (Attempt {attempt + 1}/{MAX_RETRIES})")
                print(f"Error: {str(e)}")
                await asyncio.sleep(delay)
            else:
                print(f"Max retries reached. Last error: {str(e)}")
                return None
        
        except APIError as e:
            print(f"API Error occurred: {str(e)}")
            if "credit balance is too low to access the Claude API. Please go to Plans & Billing to upgrade or purchase credits." in str(e):
                input("TOP UP and press Enter")
            # else:
            #     return None
        
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            # return None
    
    print("Max retries reached without successful request")
    return None

# Run the application creation process
if __name__ == "__main__":
    # if args --fix then fix = True else fix = false
    if len(sys.argv) == 2 and sys.argv[1] == "--fix":
        fix = "1"
        #print(sys.argv[1])
        print("fix ./app")
    elif len(sys.argv) == 2 and sys.argv[1] == "--feedback":
        print("fix ./app")
        fix = "3"
    elif len(sys.argv) == 2 and sys.argv[1] == "--plan":
        print("fix ./app")
        fix = "4"
        #print(sys.argv[1])
        #print(len(sys.argv))
    else:
        fix = "2"
        
        # WARNING: THIS SCRIPT WILL AUTOMATICALLY EXECUTE CODE ON YOUR MACHINE.
        # THIS CAN BE POTENTIALLY DANGEROUS.
        # IF YOU UNDERSTAND AND ACCEPT THIS RISK, PLEASE TYPE 'YES' TO CONTINUE.

        print(colored("Welcome to Agent application Dev!", "cyan"))
        print(colored("This tool will help you create a python application project using AI assistance.", "cyan"))
        print(colored("Please follow the prompts carefully and enjoy the application development process!", "cyan"))
        print()
        if show_user_consent:
            user_consent = input(colored("WARNING: THIS SCRIPT WILL AUTOMATICALLY EXECUTE CODE ON YOUR MACHINE. THIS CAN BE POTENTIALLY DANGEROUS. IF YOU UNDERSTAND AND ACCEPT THIS RISK, PLEASE TYPE 'YES' TO CONTINUE: ", "red")).strip().upper()

            if user_consent != "YES":
                print(colored("Script Agent application Dev.", "yellow"))
                sys.exit(0)

        print(colored("User consent received. Proceeding with Agent application Dev.", "green"))


        # move the app Directory anf its contents 1f it exists
        try:
            if os.path.exists("app"):
                # rename "app" folder to the current time/date and move to "projects" folder
                projects_folder = os.path.join(os.getcwd(), "projects")
                current_time = time.strftime("%Y%m%d-%H%M%S")
                shutil.move("app", os.path.join(projects_folder, current_time))
                print(colored("Moved app folder to projects folder." + os.path.join(projects_folder, current_time), "green"))
                
                
                
                
                
        except Exception as e:
            print(colored(f"please close any terminal which has app folder open and run the application again. error: {e}", "red"))

    #sys.exit(0)

    # Initialize Anthropic client
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    request_timestamps = deque()
    asyncio.run(create_application(fix))
    print(f"made {REQUEST_COUNTER} requests")