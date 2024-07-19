
# main.py
# Entry point for the AI Software Factory application. Orchestrates the entire process from planning to feedback incorporation.

import asyncio
from flask import Flask
from config import Config
from app import create_app
from app.services import AIService, ProjectManager, TaskManager, FileManager
from app.utils.custom_exceptions import AIServiceException, DatabaseConnectionError
import traceback
import logging

class AISoftwareFactory:
    def __init__(self, config: Config):
        self.config = config
        self.app = create_app(self.config)
        self.ai_service = AIService()
        self.project_manager = ProjectManager()
        self.task_manager = TaskManager()
        self.file_manager = FileManager()

    async def run(self):
        try:
            with self.app.app_context():
                await self.initialize_application()
                await self.start_application()
        except Exception as e:
            logging.error(f"An error occurred while running the application: {str(e)}")
            traceback.print_exc()

    async def initialize_application(self):
        try:
            # Initialize database and create tables if they don't exist
            from app import db
            db.create_all()
            logging.info("Database initialized successfully.")
        except DatabaseConnectionError as e:
            logging.error(f"Failed to initialize database: {str(e)}")
            raise

    async def start_application(self):
        # Start the Flask application
        self.app.run(host='0.0.0.0', port=5000, debug=self.config.DEBUG)

    async def plan_project(self, requirements: str) -> dict:
        try:
            plan = await self.ai_service.generate_project_plan(requirements)
            return plan
        except AIServiceException as e:
            logging.error(f"Failed to generate project plan: {str(e)}")
            raise

    async def generate_code(self, plan: dict) -> list:
        try:
            code_files = await self.ai_service.generate_code(plan)
            return code_files
        except AIServiceException as e:
            logging.error(f"Failed to generate code: {str(e)}")
            raise

    async def fix_errors(self, files: list) -> list:
        try:
            fixed_files = await self.ai_service.fix_errors(files)
            return fixed_files
        except AIServiceException as e:
            logging.error(f"Failed to fix errors: {str(e)}")
            raise

    async def incorporate_feedback(self, feedback: str, files: list) -> list:
        try:
            updated_files = await self.ai_service.incorporate_feedback(feedback, files)
            return updated_files
        except AIServiceException as e:
            logging.error(f"Failed to incorporate feedback: {str(e)}")
            raise

    async def create_tests(self, files: list) -> list:
        try:
            test_files = await self.ai_service.generate_tests(files)
            return test_files
        except AIServiceException as e:
            logging.error(f"Failed to create tests: {str(e)}")
            raise

# IMPORTANT: do not remove main function as automated test will fail
# IMPORTANT: do not remove this comment
async def main():
    config = Config()
    factory = AISoftwareFactory(config)
    await factory.run()

if __name__ == "__main__":
    asyncio.run(main())
