
import os
import sys
import logging
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
import traceback

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db, create_app
from app.models import User, Project, Task
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_db():
    """Initialize the database with default data."""
    app = create_app(Config)
    
    with app.app_context():
        try:
            # Check if the database already exists
            engine = db.engine
            inspector = inspect(engine)
            
            if inspector.has_table("user"):
                logger.warning("Database already initialized. Skipping initialization.")
                return

            # Create all tables
            db.create_all()
            logger.info("Database tables created successfully.")

            # Insert default data
            insert_default_data()
            logger.info("Default data inserted successfully.")

        except SQLAlchemyError as e:
            logger.error(f"An error occurred while initializing the database: {str(e)}")
            logger.error(traceback.format_exc())
            sys.exit(1)

def insert_default_data():
    """Insert default data into the database."""
    try:
        # Create a default admin user
        admin_user = User(username="admin", email="admin@example.com")
        admin_user.set_password("admin_password")
        db.session.add(admin_user)

        # Create a default project
        default_project = Project(name="Sample Project", description="This is a sample project", user_id=1)
        db.session.add(default_project)

        # Create some default tasks
        tasks = [
            Task(title="Task 1", description="Complete the project setup", status="pending", project_id=1),
            Task(title="Task 2", description="Implement user authentication", status="in_progress", project_id=1),
            Task(title="Task 3", description="Create the main dashboard", status="pending", project_id=1)
        ]
        db.session.add_all(tasks)

        db.session.commit()
        logger.info("Default data inserted successfully.")

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"An error occurred while inserting default data: {str(e)}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    init_db()
