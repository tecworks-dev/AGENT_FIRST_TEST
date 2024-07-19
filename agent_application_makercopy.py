import asyncio
import aiofiles.os
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
from simple_editor import SimpleEditor
from fileselector import FileTreeSelector

show_user_consent = False
FILE_EXTENSIONS = (
    '.py', '.html', '.js', '.json', '.css', '.yaml', '.xml',
    '.java', '.mjs', '.tsx', '.ts', '.jsx', '.vue', '.svelte',
    '.php', '.go', '.cs', '.pyw', '.sh', '.bat', '.ps1',
    '.c', '.h', '.cpp', '.txt'
)
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
REQUEST_COUNTER = 0
DEV_FOLDER = "app"
BACKUP_FOLDER = f"{DEV_FOLDER}_backup"
THIS_DIRECTORY = os.getcwd()
LOGS_FOLDER = f"{THIS_DIRECTORY}/{DEV_FOLDER}/logs"
current_number_of_lines_of_code = 0
ANTHROPIC_API_KEY = "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"
if "ANTHROPIC_API_KEY" not in os.environ:
    print(colored("Make sure api key ANTHROPIC_API_KEY is set in environment variable.", "yellow"))
    print(colored("""in powershell: $env:ANTHROPIC_API_KEY = "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" """, "yellow"))
    print(colored("""in linux: export ANTHROPIC_API_KEY = "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" """, "yellow"))
    if ANTHROPIC_API_KEY is not None:
        os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
    print(colored("Make sure api key ANTHROPIC_API_KEY is set in environment variable.", "yellow"))
    os.environ["ANTHROPIC_API_KEY"] = input("Enter your ANTHROPIC_API_KEY to set here: ")
    if "ANTHROPIC_API_KEY" not in os.environ or len(os.environ["ANTHROPIC_API_KEY"]) < 10:
        print(colored("Make sure api key ANTHROPIC_API_KEY is set in environment variable.", "yellow"))
        sys.exit(0)
        
# Initialize Anthropic client
client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Function to check for consecutive user messages and add a separator
def add_separator_between_consecutive_user_messages(messages):
    for i in range(len(messages) - 1):
        if messages[i]["role"] == "user" and messages[i+1]["role"] == "user":
            messages.insert(i+1, {"role": "assistant", "content": " ..."})
    return messages

# Function for planner agents to discuss and plan the project
async def plan_project(user_input, iterations):
    system_message_1 = f"""You are a logical, critical application design expert. Your role is to discuss and plan with a critical and rigorous eye, a python Full Stack applications project based on user input. One of the main goals is to review the logic of the code to ensure a user-friendly and enjoyable application experience for the user. 
Focus on application mechanics, structure, and overall design and function and method inputs inputs(proper inputs and number of inputs) and returns of functions and methods. Do not suggest external media files or images. make sure no code files need any external files. All assets must be generated. for images or media use place holder files. Critical objective is to keep the project logically structured simple while making sure no circular imports or broken imports occur. No need to discuss timelines or git commands. Main purpose is to review and evaluate the project structure so that when the final files and their descriptions are prepared the code will function without any errors. 
Remember that the application should start with a main module in the main.py file.
here is the user input: {user_input}
"""
    save_file_contents(f"{LOGS_FOLDER}/initial_project_plan_file_system_prompt_1.txt", system_message_1)
    system_message_2 = f"""You are a logical, critical Python architecture expert Full Stack Developer. Your role is to discuss and plan with a critical and rigorous eye the file structure for a python application project. One of the main goals is to review the logic of the code to ensure a user-friendly and enjoyable application play experience for the user.
Focus on code organization, modularity, and best practices for functions and methods (proper inputs and number of inputs) and their returns. Make sure no code files need any external files. All assets must be generated. for images or media use place holder files. Critical objective is to keep the project structure logical while making sure no circular imports or broken imports occur. No need to discuss timelines or git commands. Main purpose is to review and evaluate the project structure so that when the final files and their descriptions are prepared the code will function without any errors.
Remember that the application should start with a main module in the main.py file.
Here is the user input: {user_input}
"""
    save_file_contents(f"{LOGS_FOLDER}/initial_project_plan_file_system_prompt_2.txt", system_message_2,mode="a")
    messages_1 = [{"role": "user", "content": f"please plan a python application project based on the following user input: {user_input}. Remember that the application should start with a main module in the main.py file."}]
    
    messages_2 = []

    # Loop through the number of iterations
    for i in range(iterations):
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
                print(colored(response_1.content[0].text, "green"))
            messages_1.append({"role": "assistant", "content": response_1.content[0].text})
            messages_2.append({"role": "user", "content": response_1.content[0].text})

            if is_final:
                messages_2. append({"role": "user", "content": """This is the full and final iteration. Please review the application design carefully and provide your final and complete response in the following XML format:\n<application_plan>\n <overview>Overall application description</overview>\n <mechanics>Key application mechanics</mechanics>\n <files>\n <file>\n    <name>filename.ext</name>\n  <description>File purpose and contents</description>\n <file> element for each file -- >\n </files>\n</application_plan>. IMPORTANT please return all file names including there path along with simple description of functions and methods along with their inputs and returns. Make sure to mention what imports are necessary for each file. Critical objective is to keep the project structure logical while making sure no circular imports or broken imports occur as well as the clear and accurate definition of function and method inputs. Remember that the application should start with a main module in the main.py file(main shouldn't take any arguments)."""})
            # Add a assistant prompt separator between consecutive user messages
            messages_2 = add_separator_between_consecutive_user_messages(messages_2)
            # Call the model and get the response
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
    for i, message in enumerate(messages_1):
        await save_file_contents(f"{LOGS_FOLDER}/initial_project_plan_file_message_1.txt", message["content"]+"\n\n", mode="a")
    for i, message in enumerate(messages_2):
        await save_file_contents(f"{LOGS_FOLDER}/initial_project_plan_file_message_2.txt", message["content"]+"\n\n", mode="a")
    # Extract the XML content from the response
    xml_content = re.search(r'<application_plan>.*?</application_plan>', response_2.content[0].text, re.DOTALL)
    if xml_content:
        return xml_content.group(0)
    else:
        raise ValueError("No valid XML content found in the response")

# Function to call model and write files
async def agent_write_file(file_name, file_description, application_plan):
    print(colored(f"Creating file '{file_name}' ... ", "yellow"))
    # create application folder if it doesnt exist
    os.makedirs(f"{DEV_FOLDER}", exist_ok=True)
    
    system_message = """You are a Python and Web Full Stack expert Developer. Your task is to write a error free code file for a the application based on the overall project logical structure. IMPORTANT Always return the full contents of the file. One of the main goals is to review the logic of the code to ensure a user-friendly and welformed enjoyable application experience for the user.
Do not include any external media files or images in your code instead include placeholders files with no content.
Write clean, well-commented code that follows best practices.
Add comment at top of file with purpose of the file and short simple description.
Make sure that any error is logged appropriately to the terminal use traceback.
Always add debugging statements to your code if DEBUG = True, DEBUG = True by default.
The application should start with a main module in the main.py file(main shouldn't take any arguments).
return the code for the file in the following format:
<code>
file code
</code>
"""
    await save_file_contents(f"{LOGS_FOLDER}/initial_project_file_system_prompt.txt", system_message, mode="w")
    if file_name == "main.py":
        main = ",  and should have a comment IMPORTANT: do not remove main function as automated test will fail IMPORTANT: do not remove this comment"
    else:
        main = ""
    prompt = f"""Create a file named '{file_name}' with the following description: {file_description}

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
    code = response.content[0].text
    code = code.split("<code>")[1].split("</code>")[0]
    
    # remove old backup folder then duplicate app folder to backup
    print(colored(f"Warning ! {DEV_FOLDER}_backup will be deleted. Creating backup folder ... ", "red"))
    update_backup_folder()
    dirname = os.path.dirname(os.path.join(os.path.dirname(__file__), f"{DEV_FOLDER}/{file_name}"))
    os.makedirs(dirname, exist_ok=True)
    await save_file_contents(f"{DEV_FOLDER}/{file_name}", code)

    print(f"File '{file_name}' has been created.")

# Function to create plan or application_plan.xml
async def create_plan(coding_phase):
    
    if coding_phase == "create":
        user_input = input(colored("Describe the python application application you want to create: ", "green"))
        system_message = """You are a prompt rewrite the following:"""
        # send prompt to model
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
        iterations = await get_number_from_user("How many planning iterations do you want? Higher numbers for more planning: ", default_number=default_number_of_iterations)
    if coding_phase == "create" or coding_phase == "plan":
        if coding_phase == "plan":
            # get multiline input for manual input of application_plan.xml
            print(colored(f"Enter your multiline input {DEV_FOLDER}application_plan.xml file contents. Press Ctrl+D (Unix) or Ctrl+Z (Windows) followed by Enter to finish:", "green"))
            final_plan = get_multiline_input()
        else:
            print(colored("Planning the application structure ... ", "yellow"))
            final_plan = await plan_project(user_input, iterations)
            
        save_application_plan(final_plan)
        print(colored("saved application plan to application_plan.xml", "yellow"))
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
        count_lines_of_code()

        print("Base Application creation complete!")
        if PRINT_RESPONSE:
            print("Final application plan:")
            print(final_plan)
    final_plan = await load_application_plan()
    return coding_phase, final_plan

# Main function to orchestrate the application creation process
async def create_application(coding_phase):
    global max_attempts
    coding_phase, final_plan = await create_plan(coding_phase)
    attempt = 0
    # Run the application in a loop to catch and fix errors, then enter feedback loop
    attempt_to_fix = 0
    while True:
        if not coding_phase == "feedback":
            error_message = await run_application()
            coding_phase = "fix"
        else:
            error_message = None
        if error_message is None:
            print(colored("application ran successfully!", "green"))
            print(colored("Please provide your feedback on the application for iterative improvement (or type 'quit' to exit): ", "green"))
            feedback = get_multiline_input()
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
                # skip first fix due to install requirements
                continue
            if attempt_to_fix > max_attempts:
                feedback = input(colored("Attempt to fix error? (or type 'quit' to exit): ", "green"))
                if feedback.lower() == 'quit':
                    break
            else:
                attempt_to_fix += 1
            
            # for attempt in range(max_attempts):
            attempt += 1
            print(f"Attempt {attempt} to fix the errors ... ")
            await fix_application_files(error_message)
            time.sleep(1) # Allow time for files to be written
            current_number_of_lines_of_code = count_lines_of_code()
            time.sleep(1) 
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


# Function to run the application and capture errors
async def run_application():
    global requirements_installed
    print(colored("Running the application ... ", "yellow"))
    full_output = ""
    full_error = ""
    try:
        do_requirements(f"./{DEV_FOLDER}")
        if not requirements_installed:
            print(colored("Installing requirements ...", "yellow"))  # Changed to print function
            process = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "./app/requirements.txt"], timeout=60)
            print(colored("Requirements installed.", "yellow"))  # Changed to print function
            requirements_installed = True
    except:
        pass

    try:
        # change directory to app if current folder is not app
        process = subprocess.Popen(
            [sys.executable, "-c", "import sys;  import main; main.main();"],
            cwd=f"{DEV_FOLDER}",
            bufsize=1,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(colored("application is running. Please play the application. Close the window to stop. maybe Ctrl+C", "cyan"))

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
        return error_summary
    else:
        print(colored("application completed successfully", "green"))
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
    file_contents, application_files = await get_project_files_contents()
    comment = ""
    if error_filenames:
        print(f"Error occurred in files: {', '.join(error_filenames)}")
    else:
        print("""Could not determine specific files causing the error 
Please provide a comment about the error (press ctrl+z enter to finish): """)
        comment = "\n\n" + get_multiline_input()

    print(f"Sending all files for error correction in 3 seconds. Files: {','.join(application_files.keys())}")
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
    
    if  diagnostics_report is not None:
        diagnostics_report = diagnostics_report.replace(os.getcwd() + "/", "")
        
    prompt = f"""An error occurred while running the python application project. Here's the error message:
    
{error_message}

Here is the output of diagnostics_report.py unittest:

{diagnostics_report}

Here are the contents of the files involved in the error:{file_contents}

Here a reminder of the error:
    
{error_message}{comment}
    
Please analyze the error and provide corrected versions of the files to resolve the error. return the full content of the files Remember that the application should start with a main module in the main.py file(main shouldn't take any arguments)."""
    await save_file_contents(file_name="last_fix_application_files.txt", content=prompt)
        
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
        if response.content[0].text:
            print(colored(response.content[0].text, "magenta"))
        else:
            print(response)
        # Extract corrected file contents from the response
    corrected_files = re.findall(r'<file name="(.*?)">(.*?)</file>', response.content[0].text, re.DOTALL)
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
            if module_name.startswith(f"{DEV_FOLDER}/."):
                del sys.modules[module_name]
        await asyncio.sleep(1)  # Add a small delay to ensure files are fully written
    else:
        print("No corrected file content found in the response.")
        
async def create_unittests():
    global unittest_exists, dont_send_diagnostic_file
    unittest_exists = True
    file_contents, application_files = await get_project_files_contents()
    print(colored("Creating unit tests ... ", "yellow"))
    system_message = """You are a full stack expert developer:"""
    prompt = f"""Please create unit tests for the following Python code:\n\n{file_contents}

Based on the application_plan.xml please generate a debugging diagnostic write a full unittest script to test all classes and functions and produce a report of any unexpected ensure that all, be sure to order put the tests in a logical order be carefully to include required dependence for each test, Use try except and traceback to output the errors. Important make sure to output details and reason for test before each test and the filename the test is for between tests. make sure that the the script uses def main() with no arguments. Only print output details for tests that fail or errors. This file will be saved as diagnostic_report.py Ensure to handle NameError: name 'diagnostic_report' is not defined in the unittest as it fails and cause Runtime error Traceback.

Return the updated file contents in the following format only for the files that require updates:
<file name="diagnostic_report.py">
updated_file_contents
</file>    
    """
    # Send the prompt to the model
    response = await rate_limited_request(
        model="claude-3-5-sonnet-20240620",
        system=system_message,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    # Extract corrected file contents from the response
    corrected_files = re.findall(r'<file name="(.*?)">(.*?)</file>', response.content[0].text, re.DOTALL)
    if dont_send_diagnostic_file:
        corrected_files = list(filter(lambda x: x[0] != 'diagnostic_report.py', corrected_files))
        corrected_files = list(filter(lambda x: x[0] != 'README.md', corrected_files))
    if corrected_files:
        for filename, content in corrected_files:
            file_path = os.path.join(f"{DEV_FOLDER}", filename)
            dir_name = os.path.dirname(file_path)
            os.makedirs(dir_name, exist_ok=True)
            
            # Write the file
            await save_file_contents(file_path, content)
            print(f"Updated file: {file_path}")

# run the unittests
async def run_unittests():
    global unittest_exists
    print(colored("Running unit tests ... ", "yellow"))
    # clear os file stats cache
    try:
        content = await get_file_contents(f"{DEV_FOLDER}/diagnostic_report.py")
        if not content == False:
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
        aiofiles.os.stat(f"{DEV_FOLDER}/diagnostic_report.py")
    except FileNotFoundError:
        print(f"File not found: {DEV_FOLDER}/diagnostic_report.py")
        unittest_exists = False
    except Exception as e:
        print(f"Error reading {DEV_FOLDER}/diagnostic_report.py: {str(e)}")
        unittest_exists = False
    if not unittest_exists:
        await create_unittests()
    try:
        # change directory to app if current folder is not app
        process = subprocess.Popen(
            [sys.executable, "-c", "import sys;  import main; diagnostic_report.main();"],
            cwd=f"{DEV_FOLDER}",
            bufsize=1,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        full_error = ""
        full_output = ""
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

# Function to get multiline input
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

async def update_application_files(user_feedback):
    # Gather all existing application files
    file_contents, application_files = await get_project_files_contents()
    diagnostics_report = await run_unittests()
    if diagnostics_report is not None:
        diagnostics_report = diagnostics_report.replace(os.getcwd() + "/", "")
    prompt = f"""Here are the current contents of the python application project files:{file_contents}


Here is the output of diagnostics_report.py unittest:

{diagnostics_report}

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
Ensure that your changes are consistent with the existing code structure and python application best practices. Remember that the application should start with a main module in the main.py file(main shouldn't take any arguments) the file app/main.py must have def main(no arguments) and should have a comment IMPORTANT: do not remove main function as automated test will fail IMPORTANT: do not remove this comment."""
    system_message = """You are a full stack expert developer"""
    
    await save_file_contents("last_update_application_files.txt", prompt)
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
            print(colored(response.content[0].text, "magenta"))
        except:
            print("No content found in the response.")
            print(response)
        
        # Extract updated file contents from the response
        updated_files = re.findall(r'<file name="(.*?)">(.*?)</file>', response.content[0].text, re.DOTALL)
        if updated_files:
            # remove old backup folder then duplicate app folder to backup
            print(colored("Updating backup files ... ", "yellow"))
            await update_backup_folder()
            for filename, content in updated_files:
                file_path = os.path.join(f"{DEV_FOLDER}", filename)
                dir_name = os.path.dirname(file_path)
                if not await aiofiles.os.path.exists(dir_name):
                    await aiofiles.os.makedirs(dir_name, exist_ok=True)
                await save_file_contents(file_name=file_path, content=content.strip())
                print(f"Updated file: {filename}")

                # Ensure the file is written correctly by reading it back
                written_content = await get_file_contents(file_name=file_path)
                if written_content.strip() != content.strip():
                    print(colored(f"Warning: File {filename} may not have been written correctly."))
                    
            # Clear Python's module cache for the app directory
            for module_name in list(sys.modules.keys()):
                if module_name.startswith(f'{DEV_FOLDER}.'):
                    del sys.modules[module_name]

            time.sleep(1) # Add a small delay to ensure files are fully written
        else:
            print(colored("No updates were necessary based on the user's feedback.", "yellow"))

# Function to parse file structure from planner agents' discussion
def parse_file_structure_xml(xml_string):
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

# files in the application folder
async def get_project_files_contents():
    application_files = {}
    for root, dirs, files in os.walk(f"{DEV_FOLDER}"):
        # Remove **pycache** directories
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
            dirs.remove('__pycache__')  # prevent os.walk from recursing into it
        # Remove other directories we want to skip
        dirs[:] = [d for d in dirs if d not in ['node_modules', 'venv', '.venv', 'env', '.env', 'build', 'dist']]
        if dont_send_diagnostic_file:
            dirs[:] = [d for d in dirs if d not in ['diagnostic_report.py']]
            dirs[:] = [d for d in dirs if d not in ['README.md']]
        for filename in files:
            if filename.endswith(FILE_EXTENSIONS):
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, f"{DEV_FOLDER}")
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
                        print(f"Error reading {relative_path}: {str(e)}")
                        break
    # Prepare the prompt for the API
    file_contents = "\n\n".join([f"File: {filename}\n\n{content}" for filename, content in application_files.items()])
    return file_contents, application_files

def count_lines_of_code(silent=True):
    total_lines = 0
    for root, dirs, files in os.walk(f"{DEV_FOLDER}"):
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
            dirs.remove('__pycache__')  # prevent os.walk from recursing into it
        
        # Remove other directories we want to skip
        dirs[:] = [d for d in dirs if d not in ['node_modules', 'venv', '.venv', 'env', '.env', 'build', 'dist']]
        if dont_send_diagnostic_file:
            dirs[:] = [d for d in dirs if d not in ['diagnostic_report.py']]
            dirs[:] = [d for d in dirs if d not in ['README.md']]
        for filename in files:
            if filename.endswith(FILE_EXTENSIONS ):
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, f"{DEV_FOLDER}")
                for encoding in ENCODINGS:
                    try:
                        with aiofiles.open(file_path, 'r', encoding=encoding) as file:
                            file_lines = sum(1 for line in file if line.strip())
                            total_lines += file_lines
                            if not silent:
                                print(colored(f"File: {relative_path}, Lines: {file_lines}", "cyan"))
                        if not silent:
                            print(f"Successfully read {relative_path} with {encoding} encoding")
                        break
                    except UnicodeDecodeError:
                        if encoding == ENCODINGS[-1]:
                            if not silent:
                                print(colored(f"Error: Unable to read {relative_path} with any of the attempted ENCODINGS", "red"))
                    except Exception as e:
                        if not silent:
                            print(colored(f"Error reading {relative_path}: {str(e)}", "red"))
                        break
    if not silent:                        
        print(colored(f"Total lines of code written by agent_application_maker: {total_lines}", "yellow"))
    return total_lines

async def get_string_from_user(message = "", default_string="y"):
    while True:
        user_input = input(colored(f"{message} Default is {default_string}: ", "green"))
        if user_input == "" or user_input is None:
            user_input = default_string
            break
        else:
            # check if user_input is string break
            try:
                user_input = str(user_input)
                break
            except ValueError:
                print("Please enter a valid string.")
                continue  # Skip the rest of the loop and go back to the start
    return user_input

async def get_number_from_user(message = "",default_number=2):
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

async def save_application_plan(final_plan):
    file_name = f"{DEV_FOLDER}/application_plan.xml"
    print(colored(f"writing application plan to {DEV_FOLDER}application_plan.xml", "yellow"))
    
    await save_file_contents(file_name=file_name, content=final_plan)
    if aiofiles.os.path.exists(file_name):
        return True
    print(colored(f"File not found 'file_name' save failed", "red"))
    return False

async def update_backup_folder():
    if os.path.exists( f"{DEV_FOLDER}_backup"):
        shutil.rmtree( f"{DEV_FOLDER}_backup")
    if os.path.exists(f"{DEV_FOLDER}"):
        shutil.copytree(f"{DEV_FOLDER}",  f"{DEV_FOLDER}_backup")
    os.makedirs(f"{DEV_FOLDER}", exist_ok=True)

async def load_application_plan():
    file_name = f"{DEV_FOLDER}/application_plan.xml"
    print(colored(f"loading application plan from '{file_name}'", "yellow"))
    if await aiofiles.os.path.exists(file_name):
        with await aiofiles.open(file_name, "r", encoding="utf-8") as f:
            content = await f.read()
        return content
    print(colored(f"File not found '{file_name}' load failed", "red"))
    return False

async def save_file_contents(file_name = None, content = "", encoding="utf-8", mode="w"):
    aiofiles.os.makedirs(os.path.dirname(file_name), exist_ok=True)
    print(colored(f"Saving file: '{file_name}' file with mode: {mode}", "yellow"))
    with await aiofiles.open(file_name, mode, encoding=encoding) as f:
        content = await f.write(content)
    if await aiofiles.os.path.exists(file_name):
        return content
    print(colored(f"File not found: '{file_name}'", "red"))
    await asyncio.sleep(0.5)
    return False

async def get_file_contents(file_name = None, encoding="utf-8"):
    print(colored(f"Loading file: '{file_name}'", "yellow"))
    if await aiofiles.os.path.exists(file_name):
        content = ""
        with await aiofiles.open(file_name, "r", encoding=encoding) as f:
            content = await f.read(content)
        return content
    print(colored(f"File not found: '{file_name}'", "red"))
    return False


# Function to limit the number of requests to the API
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
    
    for request_attempt in range(MAX_RETRIES):
        try:
            # Make the request
            response = await client.messages.create(*args, **kwargs)
            print(f"made {REQUEST_COUNTER} requests")
            REQUEST_COUNTER += 1
            # Add the current timestamp to our list
            request_timestamps.append(time.time())            
            return response
        
        except RateLimitError as e:
            if request_attempt < MAX_RETRIES - 1:
                delay = BASE_DELAY * (2 ** request_attempt)  # Exponential backoff
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
        coding_phase = "start"
        
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
            if os.path.exists(f"{DEV_FOLDER}"):
                # rename f"{DEV_FOLDER}" folder to the current time/date and move to "projects" folder
                projects_folder = os.path.join(os.getcwd(), "projects")
                current_time = time.strftime("%Y%m%d-%H%M%S")
                shutil.move(f"{DEV_FOLDER}", os.path.join(projects_folder, current_time))
                print(colored("Moved app folder to projects folder." + os.path.join(projects_folder, current_time), "green"))
                                
        except Exception as e:
            print(colored(f"please close any terminal which has app folder open and run the application again. error: {e}", "red"))

    #sys.exit(0)

    request_timestamps = deque()
    asyncio.run(create_application(coding_phase))
    print(f"made {REQUEST_COUNTER} requests")