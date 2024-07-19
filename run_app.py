import asyncio
import subprocess
import sys
from termcolor import colored
from requirements import do_requirements
import traceback
import os

THIS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DEV_FOLDER = "app"
requirements_installed = False  # Initialize the global variable



# Function to run the application and capture errors
async def run_application():
    global requirements_installed
    print(colored("Running the application ... ", "yellow"))
    full_output = ""
    full_error = ""
    try:
        do_requirements(f"./{DEV_FOLDER}")
        if not requirements_installed:
            print(colored("Installing requirements ...", "yellow"))
            process = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "./app/requirements.txt"], timeout=60)
            print(colored("Requirements installed.", "yellow"))
            requirements_installed = True
    except:
        pass

    try:
        process = subprocess.Popen(
            [sys.executable, "main.py"],
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
                    print("-------------- line below is an error -------------------")
                    print(colored(f"Runtime error: {line}", "red"))
                    print("-------------- line above is an error -------------------")
                    print(colored(f"Runtime error: {line.strip()}", "red"))
                else:
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
            """Handles user input asynchronously to allow stopping the process with 'q'."""
            user_input = await asyncio.to_thread(sys.stdin.readline)
            if user_input.strip().lower() == 'q':
                process.terminate()
                print(colored("Application stopped by user.", "yellow"))
                

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
        error_summary = error_summary.replace(THIS_DIRECTORY + "/", "")
        return error_summary
    else:
        print(colored("Application completed successfully", "green"))
    return None

if __name__ == "__main__":
    asyncio.run(run_application())
