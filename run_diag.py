import time
import os
import asyncio
import aiofiles
import aiofiles.os
import subprocess
import sys
from termcolor import colored
from agent_application_makercopysystemupdate import get_file_contents
from agent_application_makercopysystemupdate import get_python_library_directory


DEV_FOLDER = "app"
THIS_DIRECTORY = os.getcwd()
PROJECT_SYSTEM_FOLDER = f"{THIS_DIRECTORY}/{DEV_FOLDER}/.system"
BACKUP_FOLDER = f"{PROJECT_SYSTEM_FOLDER}/{DEV_FOLDER}_backup"
LOGS_FOLDER = f"{PROJECT_SYSTEM_FOLDER}/logs"
PRINT_RESPONSE = True
# run the unittests
async def run_unittests():
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
            if time.time() - os.stat(f"{DEV_FOLDER}/diagnostic_report.py").st_mtime < 500:
                unittest_exists = False
            else:
                unittest_exists = True

    except FileNotFoundError:
        print(f"File not found: {DEV_FOLDER}/diagnostic_report.py")
        unittest_exists = False
    except Exception as e:
        print(f"Error reading {DEV_FOLDER}/diagnostic_report.py: {str(e)}")
        unittest_exists = False

    # if not unittest_exists:
        # await create_unittests()
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
        # await create_unittests()
        time.sleep(0.5)
    full_error = ""
    full_output = ""
    try:
        # change directory to app if current folder is not app
        print(sys.executable, f"diagnostic_report.py")
        process = subprocess.Popen(
            [sys.executable, f"diagnostic_report.py"],
            cwd=f"{THIS_DIRECTORY}/{DEV_FOLDER}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        async def read_stream(stream, is_error=False):
            while True:
                line = await asyncio.to_thread(stream.readline)
                if not line:
                    break
                if is_error:
                    if PRINT_RESPONSE:
                        print("-------------- line below is an error -------------------")
                        # print(colored(f"Runtime error: {line}", "red"))
                        print(colored(f"Runtime error: {line.strip()}", "red"))
                        print("-------------- line above is an error -------------------")
                else:
                    if PRINT_RESPONSE:
                        print("-------------- line below is output -------------------")
                        print(line.strip())
                        print("-------------- line above is output -------------------")
                if is_error:
                    nonlocal full_error
                    full_error += line
                else:
                    nonlocal full_output
                    full_output += line

        async def user_input():
            while process.poll() is None:
                try:
                    user_input = await asyncio.wait_for(asyncio.to_thread(sys.stdin.readline), timeout=1.0)
                    if user_input.strip().lower() == 'q':
                        process.terminate()
                        nonlocal user_terminated
                        user_terminated = True
                        print(colored("Application stopped by user.", "yellow"))
                        break
                except asyncio.TimeoutError:
                    continue  # 

        print(colored("Application is running. Press 'q' and Enter to stop.", "cyan"))
        await asyncio.gather(
            read_stream(process.stdout),
            read_stream(process.stderr, is_error=True),
            user_input()
        )

        return_code = process.wait()
        if return_code != 0:
            full_error += f"\nProcess exited with return code {return_code}"
            

    except Exception as e:
        if not user_terminated:
            full_error += f"\nError running diagnostic_report.py : {str(e)}\n{traceback.format_exc()}"

        full_error = full_error.replace(THIS_DIRECTORY + "/", "")
        full_error = full_error.replace(THIS_DIRECTORY + "/", "")
        full_output = full_output.replace(THIS_DIRECTORY + "\\", "")
        full_output = full_output.replace(THIS_DIRECTORY + "\\", "")
        # print(os.getcwd())

        error_summary = ""
        if not user_terminated:
            if full_error:
                error_summary += f"Runtime errors:\n{full_error}\n"
            if "error" in full_output.lower() or "exception" in full_output.lower():
                error_summary += f"Possible errors in output: \n{full_output}\n"

        if error_summary:
            print(colored("Diagnostic completed with errors", "white"))
            error_summary = error_summary.replace(THIS_DIRECTORY + "/", "")
            error_summary = error_summary.replace(THIS_DIRECTORY + "\\", "")
            error_summary = error_summary.replace("\\", "/")
            error_summary = error_summary.replace(sys.exec_prefix.replace("\\", "/"), "venv")
            error_summary = error_summary.replace(get_python_library_directory().replace("\\", "/"), "venv/lib")
            
            # print(colored(error_summary, "red"))"
        
            print(colored(error_summary, "red"))
            print(colored("break now to cancel ", "yellow"))
            time.sleep(10)
            
            return error_summary
    else:
        print(colored("Unittest completed", "green"))
    return None

asyncio.run(run_unittests())