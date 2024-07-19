import asyncio
import subprocess
from pynput.keyboard import Listener, Key
from termcolor import colored
process = subprocess.Popen(["python", "fileselector.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
async def user_input(process):
    """
    Handles user input from the keyboard, looking for 'q' or ESC to terminate the process.
    """
    user_terminated_flag = False
    def on_press(key):
        try:
            # Check if the key pressed is 'q' or Escape
            if (hasattr(key, 'char') and key.char == 'q') or key == Key.esc:
                process.terminate()  # Send terminate signal to the process
                nonlocal user_terminated_flag
                user_terminated_flag = True
                print(colored("Application stopped by user.", "yellow"))
                return False  # Stop the listener
        except AttributeError:
            pass  # In case the key event doesn't have a 'char' attribute

    listener = Listener(on_press=on_press)
    listener.start()
    try:
        while not user_terminated_flag and process.poll() is None:
            await asyncio.sleep(0.1)  # Continue to sleep and check until condition changes
    finally:
        listener.stop()  # Ensure the listener is stopped properly

asyncio.run(user_input(process))