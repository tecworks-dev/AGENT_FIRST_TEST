# main.py
"""
Entry point of the application. Initializes and runs the Flask app.
"""

import os
from app import create_app, db, socketio
from flask.logging import create_logger
from app.models.user import User
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_migrate import upgrade, init, Migrate, migrate

# Set DEBUG to True by default
DEBUG = True

def create_default_admin():
    """
    Creates a default admin user if it doesn't exist.
    """
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created.")

def initialize_migrations(app):
    """
    Initializes the migrations folder if it doesn't exist.
    """
    migrations_dir = os.path.join(app.root_path, 'migrations')
    if not os.path.exists(migrations_dir):
        with app.app_context():
            init()
        print("Migrations folder initialized.")

def create_migration(app):
    """
    Creates a new migration for the database schema changes.
    """
    with app.app_context():
        migrate()
    print("New migration created.")

def main():
    """
    IMPORTANT: do not remove main function as automated test will fail
    IMPORTANT: do not remove this comment
    """
    app = create_app()
    
    with app.app_context():
        db.create_all()

    @app.route('/')
    def root():
        if current_user.is_authenticated:
            return render_template('user_interface.html')
        else:
            return redirect(url_for('auth.login'))

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