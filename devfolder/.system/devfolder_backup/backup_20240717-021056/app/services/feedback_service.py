
# app/services/feedback_service.py
"""
Handles user feedback processing and incorporation.
This service is responsible for processing user feedback and incorporating it into the project.
"""

from typing import Dict, Any
from app.utils.api_utils import AsyncAnthropic
import os
import traceback
from app.models import Project, Task
from app.services.ai_service import AIService
from app.utils.logging_service import LoggingService

class FeedbackService:
    def __init__(self):
        self.anthropic = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.ai_service = AIService()
        self.logger = LoggingService()

    async def process_feedback(self, feedback: str, project_id: int) -> Dict[str, Any]:
        """
        Process user feedback for a specific project.

        Args:
            feedback (str): The user feedback to process.
            project_id (int): The ID of the project the feedback is for.

        Returns:
            Dict[str, Any]: A dictionary containing the processed feedback and suggested actions.
        """
        try:
            project = await Project.query.get(project_id)
            if not project:
                raise ValueError(f"Project with ID {project_id} not found.")

            # Use AI to analyze the feedback
            analysis_prompt = f"Analyze the following user feedback for a software project and suggest actionable items:\n\nFeedback: {feedback}\n\nProject context: {project.description}"
            analysis_result = await self.ai_service.generate_text(analysis_prompt, max_tokens=500)

            # Extract actionable items from the analysis
            actionable_items = self._extract_actionable_items(analysis_result)

            processed_feedback = {
                "original_feedback": feedback,
                "analysis": analysis_result,
                "actionable_items": actionable_items
            }

            if __debug__:
                print(f"Processed feedback for project {project_id}: {processed_feedback}")

            return processed_feedback

        except Exception as e:
            self.logger.log_error(f"Error processing feedback: {str(e)}", traceback.format_exc())
            raise

    async def incorporate_feedback(self, processed_feedback: Dict[str, Any], project_id: int) -> bool:
        """
        Incorporate processed feedback into the project.

        Args:
            processed_feedback (Dict[str, Any]): The processed feedback to incorporate.
            project_id (int): The ID of the project to incorporate the feedback into.

        Returns:
            bool: True if the feedback was successfully incorporated, False otherwise.
        """
        try:
            project = await Project.query.get(project_id)
            if not project:
                raise ValueError(f"Project with ID {project_id} not found.")

            for item in processed_feedback["actionable_items"]:
                # Create a new task for each actionable item
                new_task = Task(
                    title=item["title"],
                    description=item["description"],
                    project_id=project_id,
                    status="pending"
                )
                await new_task.save()

            # Update the project description to reflect the incorporated feedback
            update_prompt = f"Update the following project description to incorporate this feedback: {processed_feedback['original_feedback']}\n\nCurrent description: {project.description}"
            updated_description = await self.ai_service.generate_text(update_prompt, max_tokens=300)
            project.description = updated_description
            await project.save()

            if __debug__:
                print(f"Feedback incorporated into project {project_id}")

            return True

        except Exception as e:
            self.logger.log_error(f"Error incorporating feedback: {str(e)}", traceback.format_exc())
            return False

    def _extract_actionable_items(self, analysis: str) -> List[Dict[str, str]]:
        """
        Extract actionable items from the AI analysis of feedback.

        Args:
            analysis (str): The AI-generated analysis of the feedback.

        Returns:
            List[Dict[str, str]]: A list of actionable items, each containing a title and description.
        """
        # This is a simplified implementation. In a real-world scenario, you might use
        # more sophisticated NLP techniques or another AI call to extract actionable items.
        lines = analysis.split('\n')
        actionable_items = []
        for line in lines:
            if line.startswith("- "):
                title = line[2:].strip()
                description = f"Implement the following based on user feedback: {title}"
                actionable_items.append({"title": title, "description": description})
        return actionable_items

# Ensure this code runs only when the module is executed directly
if __name__ == "__main__":
    print("This module is not meant to be run directly. Please import and use the FeedbackService class.")
