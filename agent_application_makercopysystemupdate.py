from curses import nonl
import re
import asyncio
import sys
# from telnetlib import AYT
# from threading import local
import time
import subprocess
import traceback
import os
import shutil
import signal
from threading import Thread
from pynput.keyboard import Listener, Key
import xml.etree.ElementTree as ET
from collections import deque
import aiofiles
import aiofiles.os
from huggingface_hub.commands import user
from numpy import full
from termcolor import colored
import aioconsole
from pynput import keyboard
from anthropic import AsyncAnthropic, RateLimitError, APIError
# from simple_editor import SimpleEditor
# from fileselector import FileTreeSelector
from fileselector import select_files_manually
from requirements import do_requirements

show_user_consent = False
FILE_EXTENSIONS = (
    '.py', '.html', '.js', '.json', '.css', '.yaml', '.xml',
    '.java', '.mjs', '.tsx', '.ts', '.jsx', '.vue', '.svelte',
    '.php', '.go', '.cs', '.pyw', '.sh', '.bat', '.ps1',
    '.c', '.h', '.cpp', '.txt', ".md"
)
FOLDERS_TO_EXCLUDE = ['node_modules', 'venv', '.venv', 'env', '.env', 'build',
                      'dist', '.log', '.system', '__pycache__']
# Convert the folders to exclude into patterns that shutil.ignore_patterns can use
IGNORE_PATTERNS = [f for f in FOLDERS_TO_EXCLUDE]
FILES_TO_EXCLUDE = ['appmap.log']
ENCODINGS = ['utf-8', 'latin-1', 'ascii']
unittest_exists = False
requirements_installed = False
dont_send_diagnostic_file = True
max_attempts = 5 # create application
default_number_of_iterations = 2
PRINT_RESPONSE = True
REQUEST_LIMIT = 145
TIME_WINDOW = 60  # seconds
MAX_RETRIES = 20 # number of ai retrys api issue
BASE_DELAY = 60  # second
request_counter = 0
DEV_FOLDER = "devfolder"
THIS_DIRECTORY = os.getcwd()
PROJECT_SYSTEM_FOLDER = f"{THIS_DIRECTORY}/{DEV_FOLDER}/.system"
BACKUP_FOLDER = f"{PROJECT_SYSTEM_FOLDER}/{DEV_FOLDER}_backup"
LOGS_FOLDER = f"{PROJECT_SYSTEM_FOLDER}/logs"
current_line_count = 0
ANTHROPIC_API_KEY = "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"
print(__name__)
if "ANTHROPIC_API_KEY" not in os.environ:
    print(colored("Make sure api key ANTHROPIC_API_KEY is set in environment variable.", "yellow"))
    print(colored("""in powershell: $env:ANTHROPIC_API_KEY = "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" """, "yellow"))
    print(colored("""in linux: export ANTHROPIC_API_KEY = "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" """, "yellow"))
    if ANTHROPIC_API_KEY is not None:
        os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
    else:
        print(colored("Make sure api key ANTHROPIC_API_KEY is set in environment variable.", "yellow"))
        os.environ["ANTHROPIC_API_KEY"] = input(colored("Enter your ANTHROPIC_API_KEY to set here: ", "yellow"))
    if "ANTHROPIC_API_KEY" not in os.environ or len(os.environ["ANTHROPIC_API_KEY"]) < 10:
        print(colored("Make sure api key ANTHROPIC_API_KEY is set in environment variable.", "yellow"))
        sys.exit(0)

# Initialize Anthropic client
client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Function to check for consecutive user messages and add a separator
def add_separator_between_consecutive_user_messages(messages):
    """
    Add a separator between consecutive user messages in a list of messages.

    Args:
        messages (List[Dict[str, str]]): A list of dictionaries representing messages, where each dictionary has keys "role" and "content".

    Returns:
        List[Dict[str, str]]: The modified list of messages with a separator added between consecutive user messages.
    """
    for i in range(len(messages) - 1):
        if messages[i]["role"] == "user" and messages[i+1]["role"] == "user":
            messages.insert(i+1, {"role": "assistant", "content": " ..."})
    return messages

# Function for planner agents to discuss and plan the project
async def plan_project(user_input, iterations):
    """
    Plan a Python application project based on user input and number of iterations.
    """
    system_message_1 = f"""You are a logical, critical application design expert. Your role is to discuss and plan with a critical and rigorous eye, a python Full Stack applications project based on user input. One of the main goals is to review the logic of the code to ensure a user-friendly and enjoyable application experience for the user.
Focus on application mechanics, structure, and overall design and function and method inputs inputs(proper inputs and number of inputs) and returns of functions and methods. Do not suggest external media files or images. make sure no code files need any external files. All assets must be generated. for images or media use place holder files. Critical objective is to keep the project logically structured simple while making sure no circular imports or broken imports occur. No need to discuss timelines or git commands. Main purpose is to review and evaluate the project structure so that when the final files and their descriptions are prepared the code will function without any errors.
Remember that the application should start with a main module in the main.py file.
here is the user input: {user_input}
"""
    await save_file_contents(f"{LOGS_FOLDER}/initial_project_plan_file_system_prompt_1.txt", system_message_1)
    system_message_2 = f"""You are a logical, critical Python architecture expert Full Stack Developer. Your role is to discuss and plan with a critical and rigorous eye the file structure for a python application project. One of the main goals is to review the logic of the code to ensure a user-friendly and enjoyable application play experience for the user.
Focus on code organization, modularity, and best practices for functions and methods (proper inputs and number of inputs) and their returns. Make sure no code files need any external files. All assets must be generated. for images or media use place holder files. Critical objective is to keep the project structure logical while making sure no circular imports or broken imports occur. No need to discuss timelines or git commands. Main purpose is to review and evaluate the project structure so that when the final files and their descriptions are prepared the code will function without any errors.
Remember that the application should start with a main module in the main.py file.
Here is the user input: {user_input}
"""
    await save_file_contents(f"{LOGS_FOLDER}/initial_project_plan_file_system_prompt_2.txt", system_message_2, mode="a")
    messages_1 = [{"role": "user", "content": f"please plan a python application project based on the following user input: {user_input}. Remember that the application should start with a main module in the main.py file."}]

    messages_2 = []
    response_2 = False
    # Loop through the number of iterations
    # for i in range(iterations):
    i = 0
    while True:
        i += 1
        print(colored(f"Iteration {i+1} of {iterations} planning iterations", "yellow"))
        is_final = i == iterations - 1

        if is_final:

            messages_1.append({"role": "user", "content": """this is a full and final iteration. Please provide your final application structure along with file structure you think is best for the application. return file paths with file names and descriptions. make sure to mention what imports are necessary for each file.
Critical objective is to keep the project logically structured while making sure no circular imports or broken imports occur. ensure function and method inputs are accurate as well as their returns. Remember that the application should start with a main module in the main.py file(main shouldn't take any arguments)."""})

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
                if response_1 and hasattr(response_1, "content") and response_1.content[0] and hasattr(response_1.content[0], "text"):
                    print(colored(response_1.content[0].text, "green"))  # type: ignore
            if response_1 and hasattr(response_1, "content") and response_1.content[0] and hasattr(response_1.content[0], "text"):
                messages_1.append({"role": "assistant", "content": response_1.content[0].text})  # type: ignore
                messages_2.append({"role": "user", "content": response_1.content[0].text})  # type: ignore

            messages_2.append({"role": "user", "content": """This is the full and final iteration. Please review the application design carefully and provide your final and complete response in the following XML format:
<application_plan>
    <overview>Overall application description</overview>
    <mechanics>Key application mechanics</mechanics>
    <components>
        - a list of components in project
    </components>
    <files>
        <file>
            <name>filename.ext</name>
            <description>File purpose and contents</description>
        </file>
        <file element for each file -- >
    </files>
    <logic>
        - logic flow markdown
    </logic>
</application_plan>

IMPORTANT please return all file names including there relative path ./ along with simple description of functions and methods along with their inputs and returns. Make sure to mention what imports are necessary for each file. Critical objective is to keep the project structure logical while making sure no circular imports or broken imports occur as well as the clear and accurate definition of function and method inputs. Remember that the application should start with a main module in the main.py file(main shouldn't take any arguments)."""})
            # Add a assistant prompt separator between consecutive user messages
            messages_2 = add_separator_between_consecutive_user_messages(messages_2)
            # Call the model and get the response
            response_2 = await rate_limited_request(
                model="claude-3-5-sonnet-20240620",
                system=system_message_2,
                messages=messages_2,
                max_tokens=4000
            )
            if response_2 and hasattr(response_2, "content") and response_2.content[0] and hasattr(response_2.content[0], "text"):
                messages_2.append({"role": "assistant", "content": response_2.content[0].text})  # type: ignore
                messages_1.append({"role": "user", "content": response_2.content[0].text})  # type: ignore
            break

        if PRINT_RESPONSE:
            print(colored(system_message_2, "magenta"))
            print(colored(messages_2, "magenta"))
            if response_2 and hasattr(response_2, "content") and response_2.content[0] and hasattr(response_2.content[0], "text"):
                print(colored(response_2.content[0].text, "blue"))  # type: ignore
        print(colored("Application structure so far : do you want to continue?", "green"))
        x = get_string_from_user(colored("(y/n): ", "green"), default_string="y")
        if x == "n":
            is_final = True
    for i, message in enumerate(messages_1):
        await save_file_contents(f"{LOGS_FOLDER}/initial_project_plan_file_message_1.txt", message["content"]+"\n\n", mode="a")
    for i, message in enumerate(messages_2):
        await save_file_contents(f"{LOGS_FOLDER}/initial_project_plan_file_message_2.txt", message["content"]+"\n\n", mode="a")
    xml_content = False
    if response_2 and hasattr(response_2, "content") and response_2.content[0] and hasattr(response_2.content[0], "text"):    # Extract the XML content from the response
        xml_content = re.search(r'<application_plan>.*?</application_plan>', response_2.content[0].text, re.DOTALL) # type: ignore
    if xml_content:
        return xml_content.group(0)
    else:
        raise ValueError("No valid XML content found in the response")

# Function to call model and write files
async def agent_write_file(file_name, file_description, application_plan):
    if os.path.exists(f"{DEV_FOLDER}/{file_name}"):
        pass
    else:
        print(colored(f"Creating file '{file_name}' ... ", "yellow"))
        # create application folder if it doesnt exist
        os.makedirs(f"{DEV_FOLDER}", exist_ok=True)
        additional_system_message = ""
        if os.path.exists(f"{THIS_DIRECTORY}/additional_info.txt"):
            additional_info = await get_file_contents(f"{THIS_DIRECTORY}/additional_info.txt")
            additional_system_message = f"heres some additional references: \n{additional_info}"
        system_message = f"""You are a Python and Web Full Stack expert Developer. Your task is to write a error free code file for a the application based on the overall project logical structure. IMPORTANT Always return the full contents of the file. One of the main goals is to review the logic of the code to ensure a user-friendly and welformed enjoyable application experience for the user.
Do not include any external media files or images in your code instead include placeholders files with no content.
Write clean, well-commented code that follows best practices.
Add comment at top of file with purpose of the file and short simple description.
Make sure that any error is logged appropriately to the terminal use traceback.
Always add debugging statements to your code if DEBUG = True, DEBUG = True by default. Debug and Verify All Pathways.
The application should start with a main module in the main.py file(main shouldn't take any arguments).
return the code for the file in the following format:
<code>
file code
</code>

    {additional_system_message}
    """
        await save_file_contents(f"{LOGS_FOLDER}/initial_project_file_system_prompt.txt", system_message, mode="w")
        if file_name == "main.py":
            main = ",  and should have a comment IMPORTANT: do not remove main function as automated test will fail IMPORTANT: do not remove this comment"
        else:
            main = ""
        prompt = f"""Create a file named '{file_name}' with the following description: {file_description}

For python files include famework such as unittest


Here's the overall application plan which you should follow while writing the file:
{application_plan}

Remember, the application should start with a main module in the main.py file(main shouldn't take any arguments{main}). Always return the full contents of the file
        """
        await save_file_contents(f"{LOGS_FOLDER}/{file_name}", prompt, mode="w")
        # send prompt to model
        response = await rate_limited_request(
            model="claude-3-5-sonnet-20240620",
            system=system_message,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
            )
        # extract code
        if response and hasattr(response, "content") and response.content[0] and hasattr(response.content[0], "text"):
            code = response.content[0].text  # type: ignore
        else:
            code = ""
            print(colored(f"response : {response}"))
        code = code.split("<code>")[1].split("</code>")[0]

        # remove old backup folder then duplicate app folder to backup
        print(colored(f"Warning ! {DEV_FOLDER}_backup will be deleted. Creating backup folder ... ", "red"))
        await update_backup_folder()
        dirname = os.path.dirname(os.path.join(os.path.dirname(__file__), f"{DEV_FOLDER}/{file_name}"))
        await aiofiles.os.makedirs(dirname, exist_ok=True)
        await save_file_contents(f"{DEV_FOLDER}/{file_name}", code)

        print(f"File '{file_name}' has been created.")


# Function to create plan or application_plan.xml
async def create_plan(coding_phase):
    """
    Asynchronously creates a plan for a Python application based on the given coding phase.

    Args:
        coding_phase (str): The phase of coding. Can be either "create" or "plan".

    Returns:
        Tuple[str, str]: A tuple containing the coding phase and the final plan for the application.

    Raises:
        None

    Description:
        This function first checks if the coding phase is "create". If it is, it prompts the user to describe the Python application they want to create and saves the user input to a log file. It then sends the user input to a model for prompt rewriting and uses the response to update the user input. It then prompts the user for the number of planning iterations they want and saves the final plan to a file. If the coding phase is "plan", it prompts the user to enter the multiline input for the application plan. Otherwise, it plans the application structure using the user input and saves the final plan to a file. It then creates the application files based on the file structure and counts the lines of code in the application. Finally, it returns the coding phase and the final plan for the application.
    """
    iterations = 2
    if coding_phase == "create":
        user_input = input(colored("Describe the python application application you want to create: ", "green"))
        await save_file_contents(f"{LOGS_FOLDER}/initial_project_description.txt", user_input, mode="a")
        system_message = """You are a prompt rewrite the following:"""
        # send prompt to model
        response = await rate_limited_request(
            model="claude-3-5-sonnet-20240620",
            system=system_message,
            messages=[{"role": "user", "content": user_input}],
            max_tokens=4000
        )
        if response and hasattr(response, "content") and response.content[0] and hasattr(response.content[0], "text"):
            user_input = response.content[0].text  # type: ignore

        if PRINT_RESPONSE:
            print(colored(system_message, "magenta"))
            print(colored(user_input, "green"))
        iterations = await get_number_from_user("How many planning iterations do you want? Higher numbers for more planning: ", default_number=default_number_of_iterations)
    if coding_phase == "create" or coding_phase == "plan":
        if coding_phase == "plan":
            # get multiline input for manual input of application_plan.xml
            print(colored(f"Enter your multiline input {PROJECT_SYSTEM_FOLDER}/application_plan.xml file contents. Press Ctrl+D (Unix) or Ctrl+Z (Windows) followed by Enter to finish:", "green"))
            final_plan = get_multiline_input()
        else:
            print(colored("Planning the application structure ... ", "yellow"))
            final_plan = await plan_project(user_input, iterations)

        await save_application_plan(final_plan)
        print(colored(f"saved application plan to {PROJECT_SYSTEM_FOLDER}/application_plan.xml", "yellow"))
        print(colored("Parsing application plan ... ", "yellow"))
        file_structure = parse_file_structure_xml(final_plan)
        print(colored("Creating application files ... ", "yellow"))
        tasks = []
        for file_name, file_description in file_structure:
            task = asyncio.create_task(agent_write_file(file_name, file_description, final_plan))
            tasks.append(task)
        await asyncio.gather(*tasks)

        print(colored("Application files Created.", "yellow"))
        print(colored("Analizing Application files ... ", "yellow"))
        current_line_count = await count_lines_of_code(False)
        if current_line_count:
            pass

        print("Base Application creation complete!")
        if PRINT_RESPONSE:
            print("Final application plan:")
            print(final_plan)
    final_plan = await get_file_contents(f"{PROJECT_SYSTEM_FOLDER}/application_plan.xml")
    return coding_phase, final_plan

# Main function to orchestrate the application creation process
async def create_application(coding_phase):
    """
    Creates an application by running it in a loop to catch and fix errors, then entering a feedback loop.

    Args:
        coding_phase (str): The current coding phase.

    Returns:
        None
    """
    global max_attempts
    if PRINT_RESPONSE:
        print(colored("Creating application ... ", "yellow"))
    coding_phase, final_plan = await create_plan(coding_phase)
    if final_plan:
        pass
    attempt = 0
    # Run the application in a loop to catch and fix errors, then enter feedback loop
    attempt_to_fix = 0
    while True:
        if not coding_phase == "feedback":
            coding_phase = "fix"
            error_message = await run_application()
        else:
            error_message = None
        if error_message is None:
            print(colored("application ran successfully with no error!", "green"))
            print(colored("Please provide your feedback on the application for iterative improvement (or type 'q' to exit): ", "green"))
            feedback = get_multiline_input()
            if feedback.lower() == 'q':
                break
            print("Updating application based on feedback ... ")
            await get_application_update(feedback)
            current_line_count = await count_lines_of_code(False)
            if current_line_count:
                pass
            coding_phase = "fix"
        else:
            if PRINT_RESPONSE:
                print(colored(f"Error detected:\n{error_message}", "red"))
                print(colored("------------------------end of error output------------------------ ", "red"))

            if ".wav" in error_message or ".png" in error_message or ".jpg" in error_message or ".mp3" in error_message:
                input(colored("Missing media file please and it then press Enter if ?__debugger is not in the error will attempt to fix ", "red"))
                if "?__debugger" not in error_message:
                    error_message = "\n".join([line for line in string.split('\n') if '/admin/?__debugger__=yes' not in line])
                    continue
            if attempt_to_fix == 0:
                attempt_to_fix += 1
                # skip first fix due to install requirements
                continue
            if attempt_to_fix > max_attempts:
                feedback = input(colored("Attempt to fix error? (or type 'q' to exit): ", "green"))
                if feedback.lower() == 'q':
                    break
            else:
                attempt_to_fix += 1

            attempt += 1
            print(f"Attempt {attempt} to fix the errors ... ")
            # print(error_message)
            
            # print(error_message)
            # sys.exit(0)
            print("exiting ... ", os.getcwd(), THIS_DIRECTORY)
            await save_file_contents(LOGS_FOLDER + "/error_message_logs.txt", error_message, encoding="utf-8", mode="a")
            user_input = await get_string_from_user("Do you want to try autofixing the error? Y/N: default is y", default_string="y")
            if user_input.lower() == "y":
                await fix_application_files(error_message)
                time.sleep(1) # Allow time for files to be written
                current_line_count = await count_lines_of_code(False)
                if current_line_count:
                    pass
                time.sleep(1)
            

# Function to run the application and capture errors

async def run_application():
    global requirements_installed
    print(colored("Running the application ...", "yellow"))
    full_output = ""
    full_error = ""
    user_terminated_flag = False

    output, error, full_out_array = [], [], []
    try:
        do_requirements(f"./{DEV_FOLDER}", FOLDERS_TO_EXCLUDE)
        if not requirements_installed:
            print(colored("Installing requirements ...", "yellow"))
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", f"./{DEV_FOLDER}/requirements.txt"], timeout=60, check=True)
            print(colored("Requirements installed.", "yellow"))
            requirements_installed = True

    except Exception as e:
        print(colored(f"Error installing requirements: {e}", "red"))
        return f"Error installing requirements: {e}"

    try:
        cmd = [sys.executable, "main.py"]
        cwd = os.path.join(THIS_DIRECTORY, DEV_FOLDER)
        
        # cmd = [sys.executable, "-m", "pip", "install", "-r", f"./{DEV_FOLDER}/requirements.txt"]
        # cwd = os.path.join(os.getcwd(), "devfolder")
        _, full_error, full_output = await runner_cmd(cmd, cwd)

    except Exception as e:
        print("subprocess try Exception")
        # if not user_terminated_flag:
        #     full_error += f"\nError running application: {str(e)}\n{traceback.format_exc()}"
        print(f"\nError running application: {str(e)}\n{traceback.format_exc()}")
    # os.system('reset')  # Use 'stty sane' if 'reset' does not work as expected

    
    # print("full error")
    # print(full_error)
    # print("full output")
    # print(full_output)
    # print("full out array")
    # print(full_out_array)
    
    full_output = "".join(f"{name} {line}" for name, line in full_out_array)  # Correctly compile the output
    
    print(full_output)
    print("run finished")
    error_summary = ""
    if full_error or "error" in full_output.lower() or "exception" in full_output.lower():
        error_summary = f"Runtime errors:\n{full_error}\nPossible errors in output: \n{full_output}\n"
        # print(colored("Application completed with errors", "white"))

    if error_summary:
        error_summary = error_summary.replace(THIS_DIRECTORY + "/", "")
        error_summary = error_summary.replace(THIS_DIRECTORY + "\\", "")
        error_summary = error_summary.replace("\\", "/")
        error_summary = error_summary.replace(sys.exec_prefix.replace("\\", "/"), "venv")
        libs = get_python_library_directory()
        if libs is not None:
            error_summary = error_summary.replace(libs.replace("\\", "/"), "venv/lib")
        error_summary = error_summary.replace(f"{DEV_FOLDER}/", "")
        print(colored("Application completed with errors", "white"))
        return error_summary
    else:
        print(colored("Application completed successfully", "green"))
    return None



def get_python_library_directory():
    """
    Returns the directory where the Python standard libraries are stored.
    This directory is typically included in the sys.path variable.
    """
    # sys.path contains a list of directories where Python looks for modules.
    # The first entry is typically the path to the standard library.
    for path in sys.path:
        # print(path)
        if '\\lib' in path.lower():
            # print("returning lib path")
            return path
    for path in sys.path:
        # print(path)
        if '/lib' in path.lower():
            # print("returning lib path")
            return path
    
    return None  # Return None if no typical lib directory is found

# Function to fix errors in the application files
async def fix_application_files(error_message):
    """
    Asynchronously fixes errors in the application files.

    Args:
        error_message (str): The error message to fix.

    Returns:
        None

    This function attempts to fix errors in the application files by analyzing the error message and the contents of the application files. It provides corrected versions of the files to resolve the error. The corrected file contents are returned in the following format:

    <file name="path/to/filename.ext">
    corrected_file_contents
    </file>

    The function first prints a message indicating that it is attempting to fix the error. It then extracts all filenames from the error message and removes 'agent_application_maker.py' from the list if present. It loads the application plan and retrieves relevant files based on the error message and the application plan. It prompts the user to provide a comment about the error if no specific files are found. It then prints a message indicating that it is sending all files for error correction in 3 seconds. It constructs a system message that provides instructions on how to fix errors in the application files. It runs diagnostics_report.py unittest and includes the output in the prompt. It includes the contents of the files involved in the error, the error message, and a reminder of the error in the prompt. It sends the prompt to the model and extracts corrected file contents from the response. It updates the backup folder, writes the corrected file contents, and verifies that the file was written successfully. It clears Python's module cache for the app directory.

    Note: This function assumes that the necessary imports and variables are defined in the codebase.

    """
    print(colored("Attempting to fix the error ... ", "yellow"))

    # Extract all filenames from the error message
    pattern = r'\b([^/\\:*?"<>|\r\n]+(?:' + '|'.join(re.escape(ext) for ext in FILE_EXTENSIONS) + r'))\b'
    error_filenames = re.findall(pattern, error_message)
    error_filenames = list(set(error_filenames)) # Remove duplicates

    # Remove agent_application_maker.py from the list if present
    error_filenames = [f for f in error_filenames if f != 'agent_application_maker.py']
    application_plan = await load_application_plan()
    # file_contents, application_files = await get_project_files_contents()
    relevant_files = await select_relevant_files(error_message, application_plan)
    print(colored(f"Model selected files: {relevant_files}\ndo you want to change the file selection y/n enter for no?", "yellow"))
    inputs = await get_string_from_user("Input: ", default_string="n")
    if inputs.lower() == "y":
        relevant_files = select_files_manually(location=DEV_FOLDER, our_selected_files=relevant_files)
    file_contents, application_files = await get_project_files_contents(selected_files=relevant_files)
    comment = ""
    if error_filenames:
        print(colored(f"Error occurred in files: {', '.join(error_filenames)}", "red"))
    else:
        print(colored("""Could not determine specific files causing the error
Please provide a comment about the error (press Ctrl+Z enter to finish): """, "green"))
    print(colored("do you have any comments Press Ctrl+Z enter to finish", "green"))
    user_response = get_multiline_input()
    if user_response.strip() != "":
        comment = "\n\nUser comment: " + user_response

    print(f"Sending these files for error correction in 3 seconds. Files: {','.join(application_files.keys())}")
    time.sleep(3)
    system_message = """You are a Python Full Stack Web and application development expert. Your task is to fix errors in python application project files.
Analyze the error message and the contents of the application files, then provide the corrected versions of the files.
Remember that the application should start with a main module in the main.py file(main shouldn't take any arguments). The file app/main.py must have def main(no arguments) and should have a comment IMPORTANT: do not remove main function as automated test will fail IMPORTANT: do not remove this comment
carefully reason about the error in a step by step manner ahead of providing the corrected code. No external files are allowed within the application. One of the main goals is to review the logic of the code to ensure a user-friendly and enjoyable application play experience for the user.
<reasoning>
reasoning about the error
</reasoning>
Return the corrected file contents in the following format only for the files that requires correction:
<file name="path/to/filename.ext">
corrected_file_contents
</file>
"""
    diagnostics_report = await run_unittests()

    if diagnostics_report is not None:
        diagnostics_report = diagnostics_report.replace(os.getcwd() + "/", "")
        diagnostics_report = f"""

Here is the output of diagnostics_report.py unittest:

{diagnostics_report}

"""
    else:
        diagnostics_report = ""

    prompt = f"""An error occurred while running the python application project. Here's the error message:

{error_message}

Here are the contents of the files involved in the error:{file_contents}
{diagnostics_report}
Here a reminder of the error:

{error_message}{comment}

Please analyze the error and provide corrected versions of the files to resolve the error. return the full content of the files Remember that the application should start with a main module in the main.py file(main shouldn't take any arguments)."""
    await save_file_contents(file_name=f"{LOGS_FOLDER}/last_fix_application_files.txt", content=prompt)

    # Send the prompt to the model
    response = await rate_limited_request(
        model="claude-3-5-sonnet-20240620",
        system=system_message,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    if PRINT_RESPONSE:
        print(colored(system_message, "magenta"))
        print(colored(prompt, "magenta"))
        if response and hasattr(response, "content") and response.content[0] and hasattr(response.content[0], "text"):
            print(colored(response.content[0].text, "magenta"))  # type: ignore
        else:
            print(response)
    corrected_files = False
    # Extract corrected file contents from the response
    if response and hasattr(response, "content") and response.content[0] and hasattr(response.content[0], "text"):
        corrected_files = re.findall(r'<file name="(.*?)">(.*?)</file>', response.content[0].text, re.DOTALL)  # type: ignore
    if corrected_files:
        # remove old backup folder then duplicate app folder to backup
        await update_backup_folder()
        for filename, content in corrected_files:
            file_path = os.path.join(f"{DEV_FOLDER}", filename)
            dir_name = os.path.dirname(file_path)
            os.makedirs(dir_name, exist_ok=True)
            # Write the file
            await save_file_contents(file_path, content)
            print(f"Updated file: {file_path}")
            # Retry mechanism for reading the file back
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    await asyncio.sleep(0.5)  # Short delay before reading
                    
                    written_content = await get_file_contents(file_path)
                    if written_content.strip() == content.strip(): # type: ignore
                        print(f"File {file_path} written and verified successfully.")
                        break
                    else:
                        print(f"Warning: File {file_path} content mismatch. Retrying...")
                except Exception as e:
                    print(f"fix_application_files Error reading {file_path} (attempt {attempt + 1}/{max_retries}): {str(e)}")
                    if attempt == max_retries - 1:
                        print(f"Failed to verify {file_path} after {max_retries} attempts.")
        # Clear Python's module cache for the app directory
        for module_name in list(sys.modules.keys()):
            if module_name.startswith(f"{DEV_FOLDER}/."):
                del sys.modules[module_name]
        await asyncio.sleep(1)  # Add a small delay to ensure files are fully written
    else:
        print("No corrected file content found in the response.")


async def create_unittests():
    """
    A function that creates unit tests based on specified Python code and application plan.
    This function prompts the user to create unit tests and generate a debugging diagnostic.
    It handles the retrieval and update of file contents, including diagnostic_report.py.
    The generated unit tests are saved in the specified file format.
    """
    global unittest_exists, dont_send_diagnostic_file
    unittest_exists = True
    file_contents, application_files = await get_project_files_contents()
    application_plan = await load_application_plan()
    updated_file_contents = None
    if os.path.exists(f"{DEV_FOLDER}/diagnostic_report.py"):
        diagnostic_report = await get_file_contents(f"{DEV_FOLDER}/diagnostic_report.py")
        updated_file_contents = f"\n# diagnostic_report.py\n\n{diagnostic_report}\n\n"
    if not updated_file_contents:
        updated_file_contents = ""
    print(colored("Creating unit tests ... ", "yellow"))
    system_message = """You are a full stack expert developer:"""
    prompt = f"""Please create unit tests for the following Python code:\n\n{file_contents}
# application_plan.xml\n\n{application_plan}
{updated_file_contents}
Based on the application_plan.xml please generate a debugging diagnostic write a full unittest script to test all classes and functions and produce a report of any unexpected ensure that all, be sure to order put the tests in a logical order be carefully to include required dependence for each test, Use try except and traceback to output the errors. Important make sure to output details and reason for test before each test and the filename the test is for between tests. make sure that the the script uses def main() with no arguments. Only print output details for tests that fail or errors. This file will be saved as diagnostic_report.py Ensure to handle NameError: name 'diagnostic_report' is not defined in the unittest as it fails and cause Runtime error Traceback.

Return the updated file contents in the following format only for the files that require updates:
<file name="diagnostic_report.py">
updated_file_contents
</file>
"""
    await save_file_contents(f"{LOGS_FOLDER}/diagnostic_report_initial_project_file_system_prompt.txt", system_message, mode="w")
    if len(prompt) < 4000:
        # Send the prompt to the model
        response = await rate_limited_request(
            model="claude-3-5-sonnet-20240620",
            system=system_message,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )
        corrected_files = False
        # Extract corrected file contents from the response
        if response and hasattr(response, "content") and response.content[0] and hasattr(response.content[0], "text"):
            corrected_files = re.findall(r'<file name="(.*?)">(.*?)</file>', response.content[0].text, re.DOTALL)  # type: ignore
        if dont_send_diagnostic_file:
            pass
            corrected_files = list(filter(lambda x: x[0] != 'diagnostic_report.py', corrected_files)) # type: ignore
            corrected_files = list(filter(lambda x: x[0] != 'README.md', corrected_files))
        if corrected_files:
            for filename, content in corrected_files:
                file_path = os.path.join(f"{DEV_FOLDER}", filename)
                dir_name = os.path.dirname(file_path)
                os.makedirs(dir_name, exist_ok=True)
                await save_file_contents(file_path, content)
                print(f"Updated file: {file_path}")
    else:
        await save_file_contents(f"{DEV_FOLDER}/diagnostic_report.py", "print('unable to generate unit tests due to source code size.')")


# run the unittests
async def run_unittests():
    """
    Asynchronously runs unit tests.

    This function checks if the unit tests have already been created and if not, creates them.
    It then attempts to read the contents of the `diagnostic_report.py` file. If the file is older
    than 500 seconds, it sets the `unittest_exists` flag to False.

    If the file is not found or an error occurs while reading the file, the `unittest_exists`
    flag is set to False.

    If the `unittest_exists` flag is False, the function calls the `create_unittests` function.

    The function then attempts to force an update of the file system by calling `aiofiles.os.stat`
    on the `diagnostic_report.py` file. If the file is not found or an error occurs, the
    `unittest_exists` flag is set to False.

    If the `unittest_exists` flag is still False, the function calls the `create_unittests`
    function.

    The function then starts a subprocess to run the `diagnostic_report.py` file. It reads the
    output and error streams of the subprocess asynchronously.

    The function defines two helper functions:
    - `read_stream(stream, is_error=False)`: This function reads lines from a given stream
      asynchronously. It skips specific lines based on their content and prints the lines
      with appropriate formatting.
    - `user_input()`: This function handles user input while the subprocess is running.
      It reads user input from the standard input and terminates the subprocess if the input
      is 'q'.

    The function awaits the completion of the subprocess. If the return code is not 0, it
    appends the return code to the `full_error` variable.

    The function returns the `full_error` variable if there are any errors. Otherwise, it
    returns None.

    Args:
        None

    Returns:
        str or None: The `full_error` variable if there are any errors. Otherwise, None.

    Raises:
        None

    """
    global unittest_exists
    user_terminated = False
    print(colored("Running unit tests ... ", "yellow"))
    # clear os file stats cache
    try:
        content = await get_file_contents(f"{DEV_FOLDER}/diagnostic_report.py")
        if not content:
            pass
        else:
            # if file age older than 500 seconds pass
            date_of_diagnostic_file = time.time() - os.path.getmtime(f"{DEV_FOLDER}/diagnostic_report.py")
            print(f"File age: {date_of_diagnostic_file}")
            if time.time() - os.stat(f"{DEV_FOLDER}/diagnostic_report.py").st_mtime > 500:
                unittest_exists = False
            else:
                unittest_exists = True

    except FileNotFoundError:
        print(f"File not found: {DEV_FOLDER}/diagnostic_report.py")
        unittest_exists = False
    except Exception as e:
        print(f"Error reading {DEV_FOLDER}/diagnostic_report.py: {str(e)}")
        unittest_exists = False

    if not unittest_exists:
        await create_unittests()
    try:
        # subprocess force file system update with stat
        await aiofiles.os.stat(f"{DEV_FOLDER}/diagnostic_report.py")
    except FileNotFoundError:
        print(f"File not found: {DEV_FOLDER}/diagnostic_report.py")
        unittest_exists = False
    except Exception as e:
        print(f"Error reading {DEV_FOLDER}/diagnostic_report.py: {str(e)}")
        unittest_exists = False
    if not unittest_exists:
        await create_unittests()
        time.sleep(0.5)
    full_error = ""
    full_output = ""
    user_terminated_flag = False
    try:
        # change directory to app if current folder is not app
        print(sys.executable, "diagnostic_report.py")
        process = subprocess.Popen(
            [sys.executable, "diagnostic_report.py"],
            cwd=os.path.join(THIS_DIRECTORY, DEV_FOLDER),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        async def read_stream(stream, is_error=False, subprocess=None):
            """
            Asynchronously reads lines from a given stream. Skips specific lines based on content.
            Handles error and output lines differently. Appends lines to respective variables.

            Args:
                stream (TextIO): The stream to read from.
                is_error (bool, optional): Indicates whether the lines are errors or not. Defaults to False.

            Returns:
                None
            """
            nonlocal user_terminated_flag
            while not user_terminated_flag and (line := await asyncio.to_thread(stream.readline)):

                
                
                # Skip specific lines based on content
                skip_lines = [
                    "---------------------------------------------------------------------",
                    "* Running on ",
                    "ent server. Do not use it in a product",
                    "ion deployment. Use a production WSGI server instead.",
                    "INFO:werkzeug: * Restarting with stat",
                    "INFO:werkzeug: * Debugger PIN",
                    "DEBUG:app:Application starting in DEBUG"
                ]
                if any(line.startswith(s) or s in line for s in skip_lines):
                    continue
                
                if is_error:
                    if PRINT_RESPONSE:
                        print("-------------- line below is an error -------------------")
                        # print(colored(f"Runtime error: {line}", "red"))
                        print(colored(f"Runtime error: {line.strip()}", "red"))
                        print("-------------- line above is an error -------------------")
                    nonlocal full_error
                    full_error += line
                else:
                    if PRINT_RESPONSE:
                        print("-------------- line below is output -------------------")
                        print(line.strip())
                        print("-------------- line above is output -------------------")
                    nonlocal full_output
                    full_output += line

                if user_terminated_flag:
                    print(colored("read_stream Application stopped by user.", "yellow"))
                    break
                if subprocess is not None and subprocess.poll() is not None:
                    print(colored("Application stopped ending monitor output.", "yellow"))
                    break

        async def user_input(process):
            """
            A function that handles key presses.
                
            Parameters:
                key: The key object representing the pressed key.
        
            Returns:
                False if the key press indicates the user wants to stop the application, otherwise None.
            """
            
            def key_press(key):
                """
                A function that handles key presses.
                
                Parameters:
                    key: The key object representing the pressed key.

                Returns:
                    False if the key press indicates the user wants to stop the application, otherwise None.
                """
                # print(key)
                if (hasattr(key, 'char') and key.char == 'q') or key == Key.esc:
                    while process.poll() is None:
                        print("terminated")
                        process.kill()
                    
                    nonlocal user_terminated_flag
                    user_terminated_flag = True
                    print(colored("key_press Application stopped by user.", "yellow"))
                    return None  # Stop the listener
                
            listener = Listener(on_press=key_press)
            listener.start()
            nonlocal user_terminated_flag
            while not user_terminated_flag and process.poll() is None:
                await asyncio.sleep(0.1)
            listener.stop()
            
        # Concurrently read output streams and listen for user input
        await asyncio.gather(
            read_stream(process.stdout, is_error=False, subprocess=process),
            read_stream(process.stderr, is_error=True, subprocess=process),
            user_input(process)
        )
        print(colored("diagnostic_report.py stopped.", "yellow"))
        return_code = process.wait()
        if return_code != 0:
            full_error += f"\nProcess exited with return code {return_code}"
    except KeyboardInterrupt:
        full_error += f"\nError running diagnostic_report.py user interrupted: {str(e)}\n{traceback.format_exc()}"
    except Exception as e:
        if not user_terminated_flag:
            full_error += f"\nError running diagnostic_report.py : {str(e)}\n{traceback.format_exc()}"
            
    # print(colored(full_output, "yellow"))
    # print("--------------------------------------------------------------------")
    # print(colored(full_error, "yellow"))
    # Error summary and cleanup
    error_summary = ""
    if not user_terminated_flag:
        if full_error or "error" in full_output.lower() or "exception" in full_output.lower():
            error_summary = f"Runtime errors:\n{full_error}\nPossible errors in output: \n{full_output}\n"
            print(colored("Application completed with errors", "white"))
        
    # print(error_summary)
    if error_summary:
        print(colored("Application completed with errors", "white"))
        error_summary = error_summary.replace(THIS_DIRECTORY + "/", "")
        error_summary = error_summary.replace(THIS_DIRECTORY + "\\", "")
        error_summary = error_summary.replace("\\", "/")
        error_summary = error_summary.replace(sys.exec_prefix.replace("\\", "/"), "venv")
        libs = get_python_library_directory()
        if libs is not None:
            error_summary = error_summary.replace(libs.replace("\\", "/"), "venv/lib")
        error_summary = error_summary.replace(f"{DEV_FOLDER}/", "")
        print(colored("Diagnostic completed with errors", "white"))
        print(colored(error_summary, "red"))
        print(colored("break now to cancel ", "yellow"))
        time.sleep(5)
        user_response = get_string_from_user(message="Press enter to submit error summary or N to skip", default_string="y")
        if user_response.lower() == "y":
            return error_summary
        else:
            return None
    else:
        print(colored("Unittest completed", "green"))
    return None

# Function to get multiline input
def get_multiline_input():
    """
    A function that prompts the user to enter multiline input and returns it as a single string.
    No parameters are taken, and the function returns a string.
    """
    print("Enter your multiline input. Press Ctrl+D (Unix) or Ctrl+Z (Windows) followed by Enter to finish:")
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    if "".join(lines) == "":
        return ""
    else:
        return "\n".join(lines)

# New function to update application_plan.xml

async def update_application_plan(updated_xml):
    file_path = f"{PROJECT_SYSTEM_FOLDER}/application_plan.xml"
    if await aiofiles.os.path.exists(file_path):
        current_plan = await load_application_plan()
        if current_plan is False:
            current_plan = ""
    else:
        print(colored(f"File '{file_path}' does not exist. Creating a new application plan.", "yellow"))
        current_plan = "<application_plan><files></files><logicsteps></logicsteps><mechanics></mechanics><components></components></application_plan>"

    current_root = ET.fromstring(current_plan)
    updated_root = ET.fromstring(updated_xml)

    def update_section(section_name):
        current_element = current_root.find(f".//{section_name}")
        updated_element = updated_root.find(f".//{section_name}")

        if updated_element is not None:
            if "(Updated)" in updated_element.text:
                new_content = updated_element.text.replace("(Updated)", "").strip()
                if current_element.text:
                    current_element.text += "\n" + new_content
                else:
                    current_element.text = new_content
            else:
                current_element.text = updated_element.text

    # Sections to update
    update_section("logicsteps")
    update_section("mechanics")
    update_section("components")

    # Files need special handling
    current_files_element = current_root.find('.//files')
    updated_files_element = updated_root.find('.//files')

    for updated_file in updated_files_element.findall('file'):
        filename = updated_file.find('name').text
        description = updated_file.find('description').text
        existing_file = current_files_element.find(f"file[name='{filename}']")

        if existing_file is not None:
            if "(Updated)" in description:
                description = description.replace("(Updated)", "").strip()
                existing_file_description = existing_file.find('description').text
                existing_file.find('description').text = existing_file_description + "\n" + description
            else:
                existing_file.find('description').text = description
        else:
            current_files_element.append(updated_file)

    # Save the updated XML content
    updated_plan = ET.tostring(current_root, encoding='unicode')
    await save_application_plan(updated_plan)


# New function to select relevant files for user feedback
async def select_relevant_files(user_feedback, application_plan):
    """
    A function to select relevant files based on user feedback and application plan.
    Parameters:
        user_feedback: The feedback provided by the user.
        application_plan: The current application plan.
    Returns:
        List of files that are most likely to need updates to address the feedback.
    """
    system_message = "You are an expert in understanding software architecture and user feedback. Your task is to identify which files in the project are likely to be affected by the given user feedback."

    prompt = f"""
    Given the following user feedback and the current application plan, please identify which files are most likely to need updates to address the feedback.

    User Feedback:
    {user_feedback}

    Application Plan:
    {application_plan}

    Please return your response in the following format:
    <relevant_files>
    <file>filename1.ext</file>
    <file>filename2.ext</file>
    </relevant_files>
    """

    response = await rate_limited_request(
        model="claude-3-5-sonnet-20240620",
        system=system_message,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    if response and hasattr(response, "content") and len(response.content) > -1 and hasattr(response.content[0], "text"):
        await save_file_contents(file_name=f"{LOGS_FOLDER}/select_relevant_files.txt", content=response.content[0].text) # type: ignore
        relevant_files = re.findall(r'<file>(.*?)</file>', response.content[0].text) # type: ignore
    else:
        relevant_files = []
    return relevant_files

async def get_application_update(user_feedback):
    """
    Asynchronously updates a Python application project based on user feedback.

    Args:
        user_feedback (str): The feedback provided by the user about the application.

    Returns:
        None

    This function loads the current application plan, prompts the user to choose a file selection method, and selects relevant files based on the user's feedback. It then loads the contents of the selected files and provides them to the model for analysis. The model analyzes the user's feedback and provides updates to the application files. The function saves the updated file contents and the application plan, and clears the Python module cache for the app directory.

    Note:
        - The function assumes that the model is available and can be accessed through the `rate_limited_request` function.
        - The function assumes that the necessary functions (`load_application_plan`, `get_string_from_user`, `select_files_manually`, `get_project_files_contents`, `save_file_contents`, `update_backup_folder`, `update_application_files`, `update_application_plan`) are defined and accessible.
        - The function assumes that the necessary constants (`DEV_FOLDER`, `LOGS_FOLDER`, `PRINT_RESPONSE`) are defined and accessible.
    """
    application_plan = await load_application_plan()

    # Prompt user to choose file selection method
    selection_method = await get_string_from_user("Choose file selection method (model/manual) press m for manual default is ai select: ", default_string="model")

    if selection_method.lower() == "m":
        # Use FileTreeSelector for manual file selection
        relevant_files = select_files_manually(location=DEV_FOLDER)
    else:
        # Use model-based file selection
        relevant_files = await select_relevant_files(user_feedback, application_plan)
        print(colored(f"Model selected files: {relevant_files}\ndo you want to change the file selection y/n enter for no?", "yellow"))
        inputs = await get_string_from_user("Input: ", default_string="n")
        if inputs.lower() == "y":
            relevant_files = select_files_manually(location=DEV_FOLDER, our_selected_files=relevant_files)


    file_contents, application_files = await get_project_files_contents(selected_files=relevant_files)
    print(colored("File contents loaded", "green"))
    relevant_file_contents = "\n\n".join([f"File: {filename}\n\n{application_files[filename]}" for filename in relevant_files if filename in application_files])

    print(colored(f"Model selected files: {relevant_files}\ndo you want to change the file selection y/n enter for no?", "yellow"))
    inputs = input()
    if inputs.lower() == "y":
        relevant_files = select_files_manually(location=DEV_FOLDER, our_selected_files=relevant_files)
        file_contents, application_files = await get_project_files_contents(selected_files=relevant_files)
        print(colored("File contents loaded", "green"))
    prompt = f"""
Here are the current contents of the relevant python application project files:
{relevant_file_contents}

The current application plan is application_plan xml:
{application_plan}

The user has provided the following feedback about the application:
{user_feedback}

Please analyze the feedback and suggest Full updates to the application files to address the user's comments.
Provide the Full updated content for any files that need changes.
Return the updated Full file contents in the following format only for the files that require updates:
<file name="path/to/filename.ext">
updated_file_contents
</file>
Important: ensure to provide a full and complete xml application_plan  with any changes or additions.
"""

    system_message = """You are an expert Python and python application developer. Your task is to update a python application project based on user feedback.
Analyze the current application files and the user's feedback, then provide updated versions of any files that need changes to address the feedback. Always return the full content of the files. One of the main goals is to review the logic of the code to ensure a user-friendly and enjoyable application play experience for the user. no external files are allowed within the application
Ensure that your changes are consistent with the existing code structure and python application best practices. Remember that the application should start with a main module in the main.py file(main shouldn't take any arguments) the file app/main.py must have def main(no arguments) and should have a comment IMPORTANT: do not remove main function as automated test will fail IMPORTANT: do not remove this comment."""
    print(f"{LOGS_FOLDER}/last_get_application_update.txt")

    await save_file_contents(f"{LOGS_FOLDER}/last_get_application_update.txt", prompt)
    # send the prompt to the model
    response = await rate_limited_request(
        model="claude-3-5-sonnet-20240620",
        system=system_message,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )

    if PRINT_RESPONSE:
        print(colored(system_message, "magenta"))
        print(colored(prompt, "magenta"))
        try:
            print(colored(response.content[0].text, "magenta")) # type: ignore
        except Exception as e:
            print(f"No content found in the response. {e}")
            print(response)
    if response and hasattr(response, "content") and len(response.content) > 0 and hasattr(response.content[0], "text"):
        await save_file_contents(file_name=f"{LOGS_FOLDER}/last_get_application_update_response.txt", content=response.content[0].text) # type: ignore
    # Extract the XML content from the response
    updated_files = False
    plan = False
    if response and hasattr(response, "content") and len(response.content) > 0 and hasattr(response.content[0], "text"):
        plan = re.search(r'<application_plan>.*?</application_plan>', response.content[0].text, re.DOTALL) # type: ignore
        updated_files = re.findall(r'<file name="(.*?)">(.*?)</file>', response.content[0].text, re.DOTALL) # type: ignore
    if updated_files:
        await update_backup_folder()
        await update_application_files(updated_files)
        if plan and plan.group(0):
            # Update application_plan.xml
            await update_application_plan(plan.group(0))

        # Clear Python's module cache for the app directory
        for module_name in list(sys.modules.keys()):
            if module_name.startswith(f'{DEV_FOLDER}.'):
                del sys.modules[module_name]

        time.sleep(1) # Add a small delay to ensure files are fully written
    else:
        print(colored("No updates were necessary based on the user's feedback.", "yellow"))


async def update_application_files(updated_files):
    """
    A function that updates files with the provided content.
    It ensures the correct writing of the files by reading them back and comparing the content.
    If the file is not written correctly, it retries the writing process.
    """
    updated_files = [(filename, content.strip()) for filename, content in updated_files]
    for filename, content in updated_files:
        file_path = os.path.join(f"{DEV_FOLDER}", filename)
        dir_name = os.path.dirname(file_path)
        if not await aiofiles.os.path.exists(dir_name):
            await aiofiles.os.makedirs(dir_name, exist_ok=True)
        await save_file_contents(file_name=file_path, content=content.strip())
        print(f"Updated file: {filename}")

        # Ensure the file is written correctly by reading it back
        written_content = await get_file_contents(file_path)
        if written_content.strip() != content.strip(): # type: ignore
            print(colored(f"Warning: File {filename} may not have been written correctly. retrying...", "yellow"))
            file_path = os.path.join(f"{DEV_FOLDER}", filename)
            dir_name = os.path.dirname(file_path)
            if not await aiofiles.os.path.exists(dir_name):
                await aiofiles.os.makedirs(dir_name, exist_ok=True)
            await save_file_contents(file_name=file_path, content=content.strip())
            print(f"Updated file: {filename}")
            written_content = await get_file_contents(file_path)
            if written_content.strip() != content.strip(): # type: ignore
                print(colored(f"Warning: File {filename} may not have been written correctly. ..", "red"))

# Function to parse file structure from planner agents' discussion
def parse_file_structure_xml(xml_string):
    """
    Recursively parses a folder structure represented by an XML element and appends the file names and descriptions to a list.

    Parameters:
        element (xml.etree.ElementTree.Element): The XML element representing the folder structure.
        current_path (str, optional): The current path to the folder being parsed. Defaults to an empty string.

    Returns:
        None
    """
    root = ET.fromstring(xml_string)
    files = []

    def parse_folder(element, current_path=''):
        """
        Recursively parses a folder structure represented by an XML element and appends the file names and descriptions to a list.

        Parameters:
            element (xml.etree.ElementTree.Element): The XML element representing the folder structure.
            current_path (str, optional): The current path to the folder being parsed. Defaults to an empty string.

        Returns:
            None
        """
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

# Updated function to get project files contents, excluding backups
async def get_project_files_contents(selected_files=None):
    """
    Function to get the contents of project files, excluding certain directories and files.

    Parameters:
        selected_files (list): A list of selected files to retrieve contents for.

    Returns:
        tuple: A tuple containing the concatenated file contents and a dictionary of file paths and contents.
    """
    application_files = {}
    for root, dirs, files in os.walk(f"{DEV_FOLDER}"):

        # Rest of the function remains the same
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
            dirs.remove('__pycache__')

        dirs[:] = [d for d in dirs if d not in FOLDERS_TO_EXCLUDE]
        if dont_send_diagnostic_file:
            dirs[:] = [d for d in dirs if d not in ['diagnostic_report.py']]
        for filename in files:
            if filename.endswith(FILE_EXTENSIONS):
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, f"{DEV_FOLDER}").replace('\\', '/')
                # print("get_project_files_contents : ", file_path)
                if selected_files is not None:
                    if relative_path not in selected_files:
                        continue
                for encoding in ENCODINGS:
                    try:
                        content = await get_file_contents(file_name=file_path, encoding=encoding)
                        application_files[relative_path] = content
                        print(f"Successfully read {relative_path} with {encoding} encoding")
                        break
                    except UnicodeDecodeError:
                        if encoding == ENCODINGS[-1]:
                            print(f"Error: Unable to read {relative_path} with any of the attempted ENCODINGS")
                    except Exception as e:
                        print(f"get_project_files_contents Error reading {relative_path}: {str(e)}")
                        break
    file_contents = "\n\n".join([f"File: {filename}\n\n{content}" for filename, content in application_files.items()])
    return file_contents, application_files


async def count_lines_of_code(silent=True):
    """
    Counts the number of lines of code in the files in the specified directory and its subdirectories.
    
    Args:
        silent (bool, optional): If True, suppresses the output of file and encoding information. Defaults to True.
    
    Returns:
        int: The total number of lines of code in the specified directory and its subdirectories.
    
    Raises:
        Exception: If there is an error reading a file with any of the attempted encodings.
    
    Note:
        - The function uses the `os.walk` function to recursively traverse the directory and its subdirectories.
        - The function uses the `os.path.join` function to construct the absolute file path.
        - The function uses the `os.path.relpath` function to get the relative file path.
        - The function uses the `aiofiles.open` function to open the file asynchronously.
        - The function uses the `async for` loop to iterate over the lines of the file asynchronously.
        - The function uses the `colored` function from the `termcolor` module to colorize the output.
    """
    total_lines = 0
    for root, dirs, files in os.walk(f"{DEV_FOLDER}"):
        dirs[:] = [d for d in dirs if d not in FOLDERS_TO_EXCLUDE]

        for filename in files:
            if filename.endswith(tuple(FILE_EXTENSIONS)):  # Using tuple for endswith check on multiple extensions
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, DEV_FOLDER)
                
                for encoding in ENCODINGS:
                    try:
                        async with aiofiles.open(file_path, mode='r', encoding=encoding) as file:
                            file_lines = 0
                            async for line in file:
                                if line.strip():  # Count non-empty lines
                                    file_lines += 1
                            total_lines += file_lines
                            if not silent:
                                print(colored(f"File: {relative_path}, Lines: {file_lines}", "cyan"))
                        if not silent:
                            print(f"Successfully read {relative_path} with {encoding} encoding")
                        break
                    except UnicodeDecodeError:
                        continue  # Try the next encoding
                    except Exception as e:
                        if not silent:
                            print(colored(f"count_lines_of_code Error reading {relative_path}: {str(e)}", "red"))
                        break

    if not silent:
        print(colored(f"Total lines of code: {total_lines}", "yellow"))
    return total_lines


async def get_string_from_user(message="", default_string="y"):
    """
    Asynchronously prompts the user for a string input.

    Args:
        message (str, optional): The message to display to the user before the input prompt. Defaults to "".
        default_string (str, optional): The default string to use if the user does not provide an input. Defaults to "y".

    Returns:
        str: The user-provided string input.

    Raises:
        None

    Notes:
        - If the user does not provide an input, the default string is used.
        - If the user provides an input that is not a valid string, they will be prompted to re-enter a valid input.
    """
    while True:
        user_input = input(colored(f"{message} Default is {default_string}: ", "green"))
        if user_input == "" or user_input is None:
            user_input = default_string
            print(f"Using default string. {default_string}")
            break
        else:
            # check if user_input is string break
            try:
                user_input = str(user_input)
                print(f"user_input: {user_input}")
                break
            except ValueError:
                print("Please enter a valid string.")
                continue  # Skip the rest of the loop and go back to the start
    return user_input


async def get_number_from_user(message="", default_number=2):
    """
    Asynchronously prompts the user for a number input.

    Args:
        message (str, optional): The message to display to the user before the input prompt. Defaults to "".
        default_number (int, optional): The default number to use if the user does not provide an input. Defaults to 2.

    Returns:
        int: The user-provided integer input.

    Raises:
        None

    Notes:
        - If the user does not provide an input, the default number is used.
        - If the user provides an input that is not a valid integer, they will be prompted to re-enter a valid input.
    """
    while True:
        user_input = input(colored(f"{message} Default is {default_number}: ", "green"))
        if user_input == "" or user_input is None:
            user_input = default_number
            break
        else:
            # check if user_input is interger break
            try:
                user_input = int(user_input)
                break
            except ValueError:
                print("Please enter a valid integer.")
                continue  # Skip the rest of the loop and go back to the start
    return user_input


# Updated function to create backups within the app folder

async def update_backup_folder():
    """
    Asynchronously updates backup files from DEV_FOLDER to BACKUP_FOLDER.
    Creates a new backup folder with a timestamp and maintains a limited number of backups.
    
    Returns:
        True if backup was successful, False otherwise.
    """
    print(colored("Updating backup files ...", "yellow"))

    try:
        if os.path.exists(os.path.join(THIS_DIRECTORY, DEV_FOLDER)):
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            await aiofiles.os.makedirs(BACKUP_FOLDER, exist_ok=True)
            new_backup_folder = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}")

            print(colored(f"Moving {DEV_FOLDER} to {new_backup_folder}", "yellow"))

            if await aiofiles.os.path.exists(os.path.join(THIS_DIRECTORY, DEV_FOLDER)):
                await asyncio.to_thread(shutil.copytree, os.path.join(THIS_DIRECTORY, DEV_FOLDER), new_backup_folder, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))
                await asyncio.to_thread(shutil.copy, f"{PROJECT_SYSTEM_FOLDER}/application_plan.xml", f"{new_backup_folder}/application_plan.xml")

            # Maintain a limited number of backups
            backups = sorted([d for d in os.listdir(BACKUP_FOLDER) if d.startswith("backup_")])
            while len(backups) > 5:  # Keep only the 5 most recent backups
                shutil.rmtree(os.path.join(BACKUP_FOLDER, backups.pop(0)))

            return True
    except Exception as e:
        print(colored(f"Error updating backup files: {e}", "red"))

    await asyncio.sleep(2)  # Simulate delay even in case of error
    return False


async def load_application_plan():
    """
    Asynchronously loads the application plan from a file specified by 'file_name'.

    Returns:
        str: The content of the application plan if the file is found, False otherwise.
    """
    file_name = f"{PROJECT_SYSTEM_FOLDER}/application_plan.xml"
    print(colored(f"loading application plan from '{file_name}'", "yellow"))
    if await aiofiles.os.path.exists(file_name):
        async with aiofiles.open(file_name, "r", encoding="utf-8") as f:
            content = await f.read()
        return content
    print(colored(f"File not found '{file_name}' load failed", "red"))
    return False


async def save_application_plan(final_plan):
    """
    Asynchronously saves the final plan to a file specified by 'file_name'.
    
    Parameters:
        final_plan (str): The plan to be saved.
    
    Returns:
        bool: True if the file was successfully saved, False otherwise.
    """
    file_name = f"{PROJECT_SYSTEM_FOLDER}/application_plan.xml"
    print(colored(f"writing application plan to {file_name}", "yellow"))

    await save_file_contents(file_name=file_name, content=final_plan)
    if await aiofiles.os.path.exists(file_name):
        return True
    print(colored(f"File not found '{file_name}' save failed", "red"))
    return False


async def save_file_contents(file_name="", content="", encoding="utf-8", mode="w"):
    """
    Asynchronously saves the content to a file specified by 'file_name'.
    
    Parameters:
        file_name (str): The path to the file to be saved.
        content (str): The content to be written to the file.
        encoding (str): The encoding to be used for writing the file (default is 'utf-8').
        mode (str): The file mode for opening the file (default is 'w').

    Returns:
        bool: True if the file was successfully saved, False otherwise.
    """
    dir_name = os.path.dirname(file_name)
    print(colored(f"making directory: '{dir_name}' file with mode: {mode}", "yellow"))
    await aiofiles.os.makedirs(os.path.dirname(file_name), exist_ok=True)
    print(colored(f"Saving file: '{file_name}' file with mode: {mode}", "yellow"))
    async with aiofiles.open(file=file_name, mode=mode, encoding=encoding) as f: # type: ignore
        await f.write(content)
    if await aiofiles.os.path.exists(file_name):
        return True
    print(colored(f"File not found: '{file_name}'", "red"))
    await asyncio.sleep(0.5)
    return False


async def get_file_contents(file_name="", encoding="utf-8"):
    """
    Asynchronously reads the contents of a file.

    Args:
        file_name (str): The path to the file to be read. Defaults to an empty string.
        encoding (str): The encoding to use when reading the file. Defaults to "utf-8".

    Returns:
        Union[str, bool]: The contents of the file as a string if the file exists, False otherwise.

    """
    file_name = file_name.replace("\\", "/")
    print(colored(f"Loading file: '{file_name}'", "yellow"))
    if await aiofiles.os.path.exists(file_name):
        async with aiofiles.open(file_name, "r", encoding=encoding) as f:
            content = await f.read()
        return content
    print(colored(f"File not found: '{file_name}'", "red"))
    return False


async def async_process_simulator(cmd, cwd, stop_event):
    """Run a subprocess and manage stdout, stderr, and a combined output."""
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        print("Subprocess started. Press 'q' to terminate.")
        combined_output = []
        stdout_data = []
        stderr_data = []

        stdout_task = asyncio.create_task(read_stream(process.stdout, "STDOUT", combined_output, stdout_data, stop_event))
        stderr_task = asyncio.create_task(read_stream(process.stderr, "STDERR", combined_output, stderr_data, stop_event))
        wait_task = asyncio.create_task(process.wait())

        done, pending = await asyncio.wait(
            [stdout_task, stderr_task, wait_task],
            return_when=asyncio.FIRST_COMPLETED
        )

        if stop_event.is_set():
            print("Termination requested...")
            process.terminate()
            await process.wait()
            print("Process terminated by user.")

        await asyncio.gather(*pending)

        combined_output_str = "\n".join([f"{src}: {text}" for src, text in combined_output])
        stdout_str = "\n".join(stdout_data)
        stderr_str = "\n".join(stderr_data)

        return stdout_str, stderr_str, combined_output_str

    except Exception as e:
        print(f"An error occurred: {e}")
        return "", "", ""

async def read_stream(stream, identifier, combined_output, individual_output, stop_event):
    """Read from a stream and append outputs to the respective buffers."""
    while not stream.at_eof() and not stop_event.is_set():
        try:
            data = await asyncio.wait_for(stream.read(1024), timeout=0.1)
            if data:
                decoded = data.decode('utf-8').strip()
                combined_output.append((identifier, decoded))
                individual_output.append(decoded)
                print(f"{identifier}: {decoded}")
            else:
                break  # No more data
        except asyncio.TimeoutError:
            continue  # Continue to check for stop condition

def on_press(key, stop_event):
    """Respond to 'q' key press to initiate termination."""
    if hasattr(key, 'char') and key.char == 'q' or key == Key.esc:
        print("Key 'q' pressed. Initiating termination...")
        stop_event.set()
        return False  # Return False to stop the listener

def listen_for_termination(stop_event):
    """Handle key presses in a separate thread."""
    with Listener(on_press=lambda key: on_press(key, stop_event)) as listener:
        listener.join()



def flush_input():
    """Flush all input from stdin buffer in a cross-platform manner."""
    try:
        fd = sys.stdin.fileno()
        
        if os.name == 'posix':
            # Handling for Linux and macOS using termios and fcntl or select
            import termios
            import fcntl
            import select
            
            # Save the old terminal settings and adjust the current settings
            oldterm = termios.tcgetattr(fd)
            newattr = termios.tcgetattr(fd)
            newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSANOW, newattr)
            
            oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

            try:
                while select.select([sys.stdin], [], [], 0)[0]:
                    sys.stdin.read(1)
            finally:
                # Restore the old terminal settings
                termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
                fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        elif os.name == 'nt':
            # Handling for Windows using msvcrt
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
                
    except Exception as e:
        print(f"Failed to flush stdin: {e}")

    
async def runner_cmd(cmd, cwd):
    """Manage subprocess execution and key listener."""
    stop_event = asyncio.Event()
    listener_thread = Thread(target=listen_for_termination, args=(stop_event,))
    listener_thread.start()
    stdout, stderr, combined_output = await async_process_simulator(cmd, cwd, stop_event)
    print("Subprocess Standard Output:")
    print(stdout)
    print("Subprocess Error Output:")
    print(stderr)
    print("Combined Subprocess Output:")
    print(combined_output)
    # Wait for the listener thread to finish
    listener_thread.join()
    
    flush_input()
    return stdout, stderr, combined_output

# Function to limit the number of requests to the API
async def rate_limited_request(*args, **kwargs):
    """
    Asynchronously makes a rate-limited request using the given arguments and keyword arguments.

    Args:
        *args: Positional arguments to be passed to the request.
        **kwargs: Keyword arguments to be passed to the request.

    Returns:
        The response from the request if successful, None if the maximum number of retries is reached without a successful request.

    Raises:
        RateLimitError: If the rate limit is exceeded and the maximum number of retries is not reached.
        APIError: If an API error occurs and the error message contains the string "credit balance is too low to access the Claude API. Please go to Plans & Billing to upgrade or purchase credits.".
        Exception: If an unexpected error occurs.

    """
    current_time = time.time()
    # print **kwargs for message limit to first 30 characters
    if "message" in kwargs and len(kwargs["message"]) > 30:
        #kwargs["message"] = kwargs["message"][:30] + "..."
        print(kwargs["message"][:30] + "...")
    global request_counter
    
    request_timestamps = deque() # Initialize request timestamps deque
    # Remove timestamps older than TIME_WINDOW
    while request_timestamps and current_time - request_timestamps[0] > TIME_WINDOW:
        request_timestamps.popleft()

    # If we've reached the limit, wait until enough time has passed
    if len(request_timestamps) >= REQUEST_LIMIT:
        sleep_time = TIME_WINDOW - (current_time - request_timestamps[0])
        if sleep_time > 0:
            print(f"Rate limit reached. Waiting for {sleep_time:.2f} seconds...")
            await asyncio.sleep(sleep_time)

    for request_attempt in range(MAX_RETRIES):
        try:
            # Make the request
            response = await client.messages.create(*args, **kwargs)
            print(f"made {request_counter} requests")
            request_counter += 1
            # Add the current timestamp to our list
            request_timestamps.append(time.time())
            return response

        except RateLimitError as e:
            if request_attempt < MAX_RETRIES - 1:
                delay = BASE_DELAY * (request_attempt)
                print(f"Rate limit exceeded. Retrying in {delay} seconds... (Attempt {request_attempt + 1}/{MAX_RETRIES})")
                print(f"Error: {str(e)}")
                await asyncio.sleep(delay)
            else:
                print(f"Max retries reached. Last error: {str(e)}")
                return None

        except APIError as e:
            print(f"API Error occurred: {str(e)}")
            if "credit balance is too low to access the Claude API. Please go to Plans & Billing to upgrade or purchase credits." in str(e):
                input("TOP UP and press Enter")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            # return None
    print("Max retries reached without successful request")
    return None


def get_project_name(project_plan):
    """
    Get the project name from the project plan.

    Args:
        project_plan (str): The project plan containing project information.

    Returns:
        str: The extracted project name.
    """
    project_name = ""
    overview = re.findall(r'<overview>(.*?)</overview>', project_plan, re.DOTALL)
    # get first 20 characters
    print(overview)
    project_name = overview[0][0:30].strip().replace(" ", "_")
    print(overview)
    return project_name


# Run the application creation process
if __name__ == "__main__":
    # if args --fix then coding_phase = True else coding_phase = false
    if len(sys.argv) == 2 and sys.argv[1] == "--fix":
        coding_phase = "fix"
        print(sys.argv[1])
        # print(f"{fix} ./app")
    elif len(sys.argv) == 2 and sys.argv[1] == "--feedback":
        coding_phase = "feedback"
        print(f"{coding_phase} ./{DEV_FOLDER}")
    elif len(sys.argv) == 2 and sys.argv[1] == "--plan":
        coding_phase = "plan"
        print(f"{coding_phase} ./{DEV_FOLDER}")
        # print(sys.argv[1])
        # print(len(sys.argv))
    else:
        coding_phase = "create"

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

        # move the app Directory and its contents if it exists
        try:
            if os.path.exists(f"{DEV_FOLDER}"):
                if os.path.exists(f"{PROJECT_SYSTEM_FOLDER}/application_plan.xml"):
                    plan = asyncio.run(load_application_plan())
                    project_name = get_project_name(plan)
                # rename f"{DEV_FOLDER}" folder to the current time/date and move to "projects" folder
                projects_folder = os.path.join(os.getcwd(), "projects")
                current_time = time.strftime("%Y%m%d-%H%M%S")
                project_name = f"{project_name}_{current_time}"
                project_path = os.path.join(projects_folder, project_name)
                print(colored(f"Move app folder to projects folder: {project_path}", "green"))
                shutil.move(f"{DEV_FOLDER}", os.path.join(projects_folder, f"{project_name}_{current_time}"))
                print(os.path.join(projects_folder, f"{project_name}_{current_time}"))
        except Exception as e:
            print(colored(f"please close any terminal which has app folder open and run the application again. error: {e}", "red"))

    try:
        asyncio.run(create_application(coding_phase))
        print(f"made {request_counter} requests")

    except (KeyboardInterrupt, SystemExit):
        print(colored("Create Application exited.", "yellow"))
    finally:
        try:
            if 'loop' in locals():
                if not loop.is_closed():
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(loop.shutdown_asyncgens())
        except RuntimeError as e:
            print(f"RuntimeError during shutdown: {e}")
        finally:
            if 'loop' in locals():
                if not loop.is_closed():
                    loop.close()