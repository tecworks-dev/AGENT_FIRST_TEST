import asyncio
import os
import sys
from pynput.keyboard import Listener, Key
from threading import Thread
from pynput.keyboard import Controller, KeyCode
import time
import pty


async def read_stream(fd, identifier, combined_output, individual_output, stop_event):
    """Read from a file descriptor and append outputs to the respective buffers."""
    loop = asyncio.get_running_loop()
    while not stop_event.is_set():
        try:
            data = await loop.run_in_executor(None, os.read, fd, 1024)
            if data:
                decoded = data.decode('utf-8').strip()
                combined_output.append((identifier, decoded))
                individual_output.append(decoded)
                print(f"{identifier}: {decoded}")
            else:
                break  # No more data
        except Exception as e:
            print(f"Error reading stream: {e}")
            break

async def async_process_simulator(cmd, cwd, stop_event):
    """Run a subprocess in a pseudo-terminal and manage outputs."""
    master_fd, slave_fd = pty.openpty()  # Open a pseudo-terminal
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=cwd,
            stdout=slave_fd,
            stderr=slave_fd,
            stdin=slave_fd
        )
        os.close(slave_fd)  # Close the slave FD because we don't need it in the parent process.

        print("Subprocess started. Press 'q' to terminate.")
        combined_output = []
        stdout_data = []
        stderr_data = []

        stream_task = asyncio.create_task(read_stream(master_fd, "OUTPUT", combined_output, stdout_data, stop_event))

        await asyncio.wait([stream_task, process.wait()], return_when=asyncio.FIRST_COMPLETED)

        if stop_event.is_set():
            print("Termination requested...")
            process.terminate()

        await process.wait()
        print("Process terminated by user.")

        await asyncio.gather(stream_task)

        os.close(master_fd)  # Close the master FD on completion.

        combined_output_str = "\n".join([f"{src}: {text}" for src, text in combined_output])
        stdout_str = "\n".join(stdout_data)  # This may contain both stdout and stderr
        stderr_str = ""  # Not separately captured

        return stdout_str, stderr_str, combined_output_str

    except Exception as e:
        print(f"An error occurred: {e}")
        return "", "", ""

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

async def main():
    """Main function for handling asynchronous operations and user input."""
    cmd = [sys.executable, "main.py"]
    cwd = os.path.join(os.getcwd(), "devfolder")
    await runner_cmd(cmd, cwd)
    time.sleep(5)
    print("Enter something:")
    response = input()
    print(f"You entered: {response}")

asyncio.run(main())
