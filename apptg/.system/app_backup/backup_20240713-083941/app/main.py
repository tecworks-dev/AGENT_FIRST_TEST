
"""
Purpose: Main entry point for the application.
This file initializes the Flask application and sets up necessary configurations.
"""

import asyncio
from flask import Flask
from app import create_app, socketio
from app.models import db

# Global flag for user termination
user_terminated_flag = asyncio.Event()

def main():
    """
    IMPORTANT: do not remove main function as automated test will fail
    IMPORTANT: do not remove this comment
    """
    app = create_app()
    
    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return "Welcome to the Secure Messaging App!"

    # Run the Flask application with SocketIO
    socketio.run(app, debug=True)

if __name__ == '__main__':
    main()

# Asynchronous function to handle user input
async def user_input(process, user_terminated_flag):
    while not user_terminated_flag.is_set():
        user_in = await asyncio.get_event_loop().run_in_executor(None, input, "Enter 'q' to quit: ")
        if user_in.lower() == 'q':
            user_terminated_flag.set()
            process.terminate()
            break

# Function to run the application asynchronously
async def run_application():
    process = await asyncio.create_subprocess_exec(
        'python', 'app/main.py',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    user_input_task = asyncio.create_task(user_input(process, user_terminated_flag))

    stdout, stderr = await process.communicate()

    if stdout:
        print(f'Application output: {stdout.decode()}')
    if stderr:
        print(f'Application error: {stderr.decode()}')

    await user_input_task

# Run the application
if __name__ == '__main__':
    asyncio.run(run_application())
