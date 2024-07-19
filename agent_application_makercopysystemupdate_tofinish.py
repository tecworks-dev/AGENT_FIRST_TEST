import asyncio
import os
import sys
import shutil
import time
import xml.etree.ElementTree as ET
import re
from collections import deque
from typing import List, Dict, Any
import logging
from anthropic import AsyncAnthropic, RateLimitError, APIError
from termcolor import colored
import aiofiles
import subprocess
from requirements import do_requirements
from fileselector import select_files_manually

# Configuration
CONFIG = {
    "DEV_FOLDER": "app",
    "BACKUP_FOLDER": "app_backups",
    "LOGS_FOLDER": "logs",
    "MAX_BACKUPS": 5,
    "API_RATE_LIMIT": 145,
    "API_TIME_WINDOW": 60,
    "MAX_RETRIES": 20,
    "BASE_DELAY": 60,
}

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AIAssistedDevelopmentTool:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.request_timestamps = deque()
        self.request_counter = 0

    async def create_application(self, coding_phase: str):
        try:
            coding_phase, final_plan = await self.create_plan(coding_phase)
            while True:
                if coding_phase != "feedback":
                    error_message = await self.run_application()
                    if not error_message:
                        break
                    await self.fix_application_files(error_message)
                else:
                    feedback = await self.get_user_feedback()
                    if feedback.lower() == 'quit':
                        break
                    await self.update_application_files(feedback)
                
                await self.update_requirements()
                await self.run_tests()
        except Exception as e:
            logging.error(f"Error in create_application: {str(e)}")
            raise

    async def create_plan(self, coding_phase: str):
        # Implementation for creating or loading a plan
        pass

    async def run_application(self) -> str:
        # Implementation for running the application and capturing errors
        pass

    async def fix_application_files(self, error_message: str):
        # Implementation for fixing errors in application files
        pass

    async def get_user_feedback(self) -> str:
        return input(colored("Please provide your feedback (or type 'quit' to exit): ", "green"))

    async def update_application_files(self, feedback: str):
        selection_method = await self.get_string_from_user("Choose file selection method (model/manual): ", default_string="model")
        
        if selection_method.lower() == "manual":
            relevant_files = select_files_manually(location=CONFIG["DEV_FOLDER"])
        else:
            application_plan = await self.load_application_plan()
            relevant_files = await self.select_relevant_files(feedback, application_plan)

        file_contents = await self.get_project_files_contents(relevant_files)
        updated_files = await self.get_model_updates(feedback, file_contents, application_plan)
        
        await self.apply_updates(updated_files)
        await self.update_application_plan(updated_files)

    async def update_requirements(self):
        logging.info("Updating requirements.txt ...")
        do_requirements(CONFIG["DEV_FOLDER"])
        logging.info("requirements.txt has been updated.")

    async def run_tests(self):
        # Implementation for running tests
        pass

    async def rate_limited_request(self, *args: Any, **kwargs: Any) -> Any:
        current_time = time.time()
        while self.request_timestamps and current_time - self.request_timestamps[0] > CONFIG["API_TIME_WINDOW"]:
            self.request_timestamps.popleft()
        
        if len(self.request_timestamps) >= CONFIG["API_RATE_LIMIT"]:
            sleep_time = CONFIG["API_TIME_WINDOW"] - (current_time - self.request_timestamps[0])
            if sleep_time > 0:
                logging.info(f"Rate limit reached. Waiting for {sleep_time:.2f} seconds...")
                await asyncio.sleep(sleep_time)
        
        for request_attempt in range(CONFIG["MAX_RETRIES"]):
            try:
                response = await self.client.messages.create(*args, **kwargs)
                self.request_counter += 1
                self.request_timestamps.append(time.time())
                return response
            except (RateLimitError, APIError) as e:
                if request_attempt < CONFIG["MAX_RETRIES"] - 1:
                    delay = CONFIG["BASE_DELAY"] * (2 ** request_attempt)
                    logging.warning(f"API Error: {str(e)}. Retrying in {delay} seconds... (Attempt {request_attempt + 1}/{CONFIG['MAX_RETRIES']})")
                    await asyncio.sleep(delay)
                else:
                    logging.error(f"Max retries reached. Last error: {str(e)}")
                    return None
        
        logging.error("Max retries reached without successful request")
        return None

    # Additional helper methods...

if __name__ == "__main__":
    tool = AIAssistedDevelopmentTool()
    asyncio.run(tool.create_application("start"))