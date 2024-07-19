
# app/cli.py
"""
Implements custom Flask CLI commands for database management and utility operations.
This file provides commands for initializing the database, populating test data,
and other utility functions to assist in application management.
"""

import click
from flask.cli import with_appcontext
from app import db
from app.models import User, Project, Task
import traceback

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database."""
    try:
        db.create_all()
        click.echo('Initialized the database.')
    except Exception as e:
        click.echo(f'Error initializing database: {str(e)}')
        if __debug__:
            click.echo(traceback.format_exc())

@click.command('populate-test-data')
@with_appcontext
def populate_test_data_command():
    """Populate the database with test data."""
    try:
        # Create test users
        user1 = User(username='testuser1', email='testuser1@example.com')
        user1.set_password('password123')
        user2 = User(username='testuser2', email='testuser2@example.com')
        user2.set_password('password456')
        db.session.add_all([user1, user2])

        # Create test projects
        project1 = Project(name='Test Project 1', description='A test project', user_id=1)
        project2 = Project(name='Test Project 2', description='Another test project', user_id=2)
        db.session.add_all([project1, project2])

        # Create test tasks
        task1 = Task(title='Task 1', description='Do something', project_id=1)
        task2 = Task(title='Task 2', description='Do something else', project_id=1)
        task3 = Task(title='Task 3', description='Another task', project_id=2)
        db.session.add_all([task1, task2, task3])

        db.session.commit()
        click.echo('Test data has been populated.')
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error populating test data: {str(e)}')
        if __debug__:
            click.echo(traceback.format_exc())

@click.command('clear-db')
@with_appcontext
def clear_db_command():
    """Clear all data from the database."""
    try:
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        click.echo('All data has been cleared from the database.')
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error clearing database: {str(e)}')
        if __debug__:
            click.echo(traceback.format_exc())

@click.command('list-users')
@with_appcontext
def list_users_command():
    """List all users in the database."""
    try:
        users = User.query.all()
        if users:
            for user in users:
                click.echo(f'ID: {user.id}, Username: {user.username}, Email: {user.email}')
        else:
            click.echo('No users found in the database.')
    except Exception as e:
        click.echo(f'Error listing users: {str(e)}')
        if __debug__:
            click.echo(traceback.format_exc())

def init_app(app):
    """Register CLI commands with the Flask application."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_test_data_command)
    app.cli.add_command(clear_db_command)
    app.cli.add_command(list_users_command)

if __name__ == '__main__':
    click.echo("This script is intended to be used with Flask's CLI.")
    click.echo("Please run your Flask application and use 'flask' commands instead.")
