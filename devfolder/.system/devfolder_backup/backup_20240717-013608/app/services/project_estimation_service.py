
"""
Purpose: Provides project estimation features based on project requirements and historical data.

This service utilizes AI capabilities to estimate project duration, cost, and analyze risk factors
based on the given project requirements and historical data from similar projects.
"""

from typing import List, Dict, Any
from app.utils.api_utils import AsyncAnthropic
import os
import logging
import traceback
from datetime import timedelta

class ProjectEstimationService:
    def __init__(self):
        self.anthropic = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.logger = logging.getLogger(__name__)

    async def estimate_project_duration(self, project_requirements: List[Dict[str, Any]]) -> int:
        """
        Estimates the project duration in days based on the given requirements.

        Args:
            project_requirements (List[Dict[str, Any]]): List of project requirements.

        Returns:
            int: Estimated project duration in days.
        """
        try:
            # Prepare the prompt for the AI model
            prompt = f"Based on the following project requirements, estimate the project duration in days:\n\n"
            for req in project_requirements:
                prompt += f"- {req['description']}\n"
            prompt += "\nProvide your estimate as a single integer representing the number of days."

            # Get AI response
            response = await self.anthropic.generate_text(prompt, max_tokens=100)
            
            # Extract the estimated duration from the response
            estimated_duration = int(response.strip())
            
            return estimated_duration
        except Exception as e:
            self.logger.error(f"Error estimating project duration: {str(e)}")
            self.logger.debug(traceback.format_exc())
            return 0

    async def estimate_project_cost(self, project_requirements: List[Dict[str, Any]]) -> float:
        """
        Estimates the project cost based on the given requirements.

        Args:
            project_requirements (List[Dict[str, Any]]): List of project requirements.

        Returns:
            float: Estimated project cost.
        """
        try:
            # Prepare the prompt for the AI model
            prompt = f"Based on the following project requirements, estimate the project cost in USD:\n\n"
            for req in project_requirements:
                prompt += f"- {req['description']}\n"
            prompt += "\nProvide your estimate as a single float representing the cost in USD."

            # Get AI response
            response = await self.anthropic.generate_text(prompt, max_tokens=100)
            
            # Extract the estimated cost from the response
            estimated_cost = float(response.strip())
            
            return estimated_cost
        except Exception as e:
            self.logger.error(f"Error estimating project cost: {str(e)}")
            self.logger.debug(traceback.format_exc())
            return 0.0

    async def analyze_risk_factors(self, project_requirements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyzes risk factors based on the given project requirements.

        Args:
            project_requirements (List[Dict[str, Any]]): List of project requirements.

        Returns:
            List[Dict[str, Any]]: List of identified risk factors with their descriptions and severity levels.
        """
        try:
            # Prepare the prompt for the AI model
            prompt = f"Analyze the following project requirements and identify potential risk factors:\n\n"
            for req in project_requirements:
                prompt += f"- {req['description']}\n"
            prompt += "\nProvide a list of risk factors, each with a description and severity level (Low, Medium, High)."

            # Get AI response
            response = await self.anthropic.generate_text(prompt, max_tokens=500)
            
            # Parse the response and extract risk factors
            risk_factors = []
            for line in response.strip().split('\n'):
                if ':' in line:
                    risk, description = line.split(':', 1)
                    severity = "Medium"  # Default severity
                    if "high" in description.lower():
                        severity = "High"
                    elif "low" in description.lower():
                        severity = "Low"
                    risk_factors.append({
                        "risk": risk.strip(),
                        "description": description.strip(),
                        "severity": severity
                    })
            
            return risk_factors
        except Exception as e:
            self.logger.error(f"Error analyzing risk factors: {str(e)}")
            self.logger.debug(traceback.format_exc())
            return []

    async def generate_estimation_report(self, project_requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates a comprehensive estimation report including duration, cost, and risk factors.

        Args:
            project_requirements (List[Dict[str, Any]]): List of project requirements.

        Returns:
            Dict[str, Any]: A dictionary containing the estimation report.
        """
        try:
            duration = await self.estimate_project_duration(project_requirements)
            cost = await self.estimate_project_cost(project_requirements)
            risk_factors = await self.analyze_risk_factors(project_requirements)

            report = {
                "estimated_duration": duration,
                "estimated_cost": cost,
                "risk_factors": risk_factors,
                "estimated_completion_date": (datetime.now() + timedelta(days=duration)).strftime("%Y-%m-%d")
            }

            return report
        except Exception as e:
            self.logger.error(f"Error generating estimation report: {str(e)}")
            self.logger.debug(traceback.format_exc())
            return {}

# For debugging purposes
if __name__ == "__main__":
    import asyncio

    async def main():
        service = ProjectEstimationService()
        sample_requirements = [
            {"description": "Develop a user authentication system"},
            {"description": "Implement a RESTful API for data management"},
            {"description": "Create a responsive front-end using React"}
        ]
        
        duration = await service.estimate_project_duration(sample_requirements)
        print(f"Estimated duration: {duration} days")
        
        cost = await service.estimate_project_cost(sample_requirements)
        print(f"Estimated cost: ${cost:.2f}")
        
        risks = await service.analyze_risk_factors(sample_requirements)
        print("Risk factors:")
        for risk in risks:
            print(f"- {risk['risk']} ({risk['severity']}): {risk['description']}")

    asyncio.run(main())
