
# Purpose: Handles AI-driven project planning tasks.
# Description: This service provides methods to generate and update project plans using AI assistance.

from typing import Dict, Any
from app.utils.api_utils import AsyncAnthropic
import os
import traceback

class ProjectPlanningService:
    def __init__(self):
        self.anthropic = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def generate_project_plan(self, requirements: str) -> Dict[str, Any]:
        """
        Generate a project plan based on the given requirements using AI assistance.

        Args:
            requirements (str): The project requirements.

        Returns:
            Dict[str, Any]: The generated project plan.
        """
        try:
            prompt = f"Generate a detailed project plan based on the following requirements:\n\n{requirements}\n\nInclude tasks, milestones, and estimated timelines."
            
            response = await self.anthropic.completion(
                model="claude-3-5-sonnet-20240620",
                prompt=prompt,
                max_tokens_to_sample=2000
            )
            
            # Parse the AI-generated response into a structured project plan
            project_plan = self._parse_ai_response(response.completion)
            
            return project_plan
        except Exception as e:
            if __debug__:
                print(f"Error in generate_project_plan: {str(e)}")
                print(traceback.format_exc())
            raise

    async def update_project_plan(self, current_plan: Dict[str, Any], new_requirements: str) -> Dict[str, Any]:
        """
        Update an existing project plan based on new requirements using AI assistance.

        Args:
            current_plan (Dict[str, Any]): The current project plan.
            new_requirements (str): The new requirements to incorporate.

        Returns:
            Dict[str, Any]: The updated project plan.
        """
        try:
            prompt = f"Update the following project plan based on these new requirements:\n\nCurrent Plan:\n{current_plan}\n\nNew Requirements:\n{new_requirements}\n\nProvide an updated project plan."
            
            response = await self.anthropic.completion(
                model="claude-3-5-sonnet-20240620",
                prompt=prompt,
                max_tokens_to_sample=2000
            )
            
            # Parse the AI-generated response into a structured updated project plan
            updated_plan = self._parse_ai_response(response.completion)
            
            return updated_plan
        except Exception as e:
            if __debug__:
                print(f"Error in update_project_plan: {str(e)}")
                print(traceback.format_exc())
            raise

    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the AI-generated response into a structured project plan.

        Args:
            response (str): The AI-generated response.

        Returns:
            Dict[str, Any]: The parsed project plan.
        """
        # This is a simplified parsing method. In a real-world scenario,
        # you'd want to implement a more robust parsing logic.
        plan = {
            "tasks": [],
            "milestones": [],
            "timeline": {}
        }
        
        lines = response.split("\n")
        current_section = None
        
        for line in lines:
            if line.lower().startswith("tasks:"):
                current_section = "tasks"
            elif line.lower().startswith("milestones:"):
                current_section = "milestones"
            elif line.lower().startswith("timeline:"):
                current_section = "timeline"
            elif line.strip() and current_section:
                if current_section == "timeline":
                    parts = line.split(":")
                    if len(parts) == 2:
                        plan[current_section][parts[0].strip()] = parts[1].strip()
                else:
                    plan[current_section].append(line.strip())
        
        return plan

if __debug__:
    # Add any additional debugging statements here
    print("ProjectPlanningService initialized")
