
# app/services/natural_language_requirements_service.py
"""
Processes natural language requirements and converts them into structured project tasks.
"""

from typing import List, Dict, Any
from app.utils.api_utils import AsyncAnthropic
import os
import traceback

DEBUG = True

class NaturalLanguageRequirementsService:
    def __init__(self):
        self.anthropic_client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    async def process_requirements(self, requirements_text: str) -> List[Dict[str, Any]]:
        """
        Process natural language requirements and convert them into structured project tasks.

        Args:
            requirements_text (str): The raw natural language requirements text.

        Returns:
            List[Dict[str, Any]]: A list of structured tasks derived from the requirements.
        """
        try:
            if DEBUG:
                print(f"Processing requirements: {requirements_text[:100]}...")

            prompt = f"""
            Given the following project requirements, generate a list of structured tasks:

            Requirements:
            {requirements_text}

            For each task, provide the following information:
            1. Task title
            2. Task description
            3. Estimated complexity (Low, Medium, High)
            4. Estimated time to complete (in hours)
            5. Dependencies (list of task titles this task depends on, if any)

            Format the output as a JSON list of task objects.
            """

            response = await self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            if DEBUG:
                print(f"AI response received. Length: {len(response.content[0].text)}")

            # Parse the JSON response
            import json
            tasks = json.loads(response.content[0].text)

            return tasks

        except Exception as e:
            if DEBUG:
                print(f"Error in process_requirements: {str(e)}")
                print(traceback.format_exc())
            raise

    async def generate_user_stories(self, requirements_text: str) -> List[str]:
        """
        Generate user stories from natural language requirements.

        Args:
            requirements_text (str): The raw natural language requirements text.

        Returns:
            List[str]: A list of user stories derived from the requirements.
        """
        try:
            if DEBUG:
                print(f"Generating user stories from requirements: {requirements_text[:100]}...")

            prompt = f"""
            Given the following project requirements, generate a list of user stories:

            Requirements:
            {requirements_text}

            Each user story should follow the format:
            "As a [type of user], I want [goal] so that [benefit]."

            Generate at least 5 user stories, but no more than 10.
            """

            response = await self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            if DEBUG:
                print(f"AI response received. Length: {len(response.content[0].text)}")

            # Split the response into individual user stories
            user_stories = [story.strip() for story in response.content[0].text.split("\n") if story.strip().startswith("As a")]

            return user_stories

        except Exception as e:
            if DEBUG:
                print(f"Error in generate_user_stories: {str(e)}")
                print(traceback.format_exc())
            raise

if DEBUG:
    print("NaturalLanguageRequirementsService initialized")
