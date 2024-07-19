
"""
Implements system thinking processes for AI decision-making.

This module provides a SystemThinkingService class that implements different levels
of thinking (System 1, System 2, and System 3) for AI decision-making processes.
These thinking processes are designed to handle different levels of complexity
and decision-making scenarios within the AI Software Factory application.
"""

from typing import List
from app.utils.api_utils import AsyncAnthropic
import os
import traceback

class SystemThinkingService:
    def __init__(self):
        self.anthropic = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def system_1_thinking(self, context: str) -> str:
        """
        Implements System 1 thinking - fast, intuitive, and automatic decision-making.

        Args:
            context (str): The context or situation for decision-making.

        Returns:
            str: The decision or response based on System 1 thinking.
        """
        try:
            prompt = f"Given the following context, provide a quick, intuitive response using System 1 thinking:\n\nContext: {context}\n\nQuick response:"
            response = await self.anthropic.completion(prompt=prompt, max_tokens_to_sample=100)
            return response.completion.strip()
        except Exception as e:
            error_msg = f"Error in system_1_thinking: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return "Unable to process System 1 thinking due to an error."

    async def system_2_thinking(self, context: str, options: List[str]) -> str:
        """
        Implements System 2 thinking - slower, more deliberate, and analytical decision-making.

        Args:
            context (str): The context or situation for decision-making.
            options (List[str]): A list of possible options to consider.

        Returns:
            str: The decision or response based on System 2 thinking.
        """
        try:
            options_str = "\n".join([f"- {option}" for option in options])
            prompt = f"""Given the following context and options, provide a deliberate and analytical response using System 2 thinking:

Context: {context}

Options:
{options_str}

Analytical response:"""
            response = await self.anthropic.completion(prompt=prompt, max_tokens_to_sample=200)
            return response.completion.strip()
        except Exception as e:
            error_msg = f"Error in system_2_thinking: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return "Unable to process System 2 thinking due to an error."

    async def system_3_thinking(self, context: str, options: List[str], constraints: List[str]) -> str:
        """
        Implements System 3 thinking - complex problem-solving considering multiple factors and constraints.

        Args:
            context (str): The context or situation for decision-making.
            options (List[str]): A list of possible options to consider.
            constraints (List[str]): A list of constraints to consider in the decision-making process.

        Returns:
            str: The decision or response based on System 3 thinking.
        """
        try:
            options_str = "\n".join([f"- {option}" for option in options])
            constraints_str = "\n".join([f"- {constraint}" for constraint in constraints])
            prompt = f"""Given the following context, options, and constraints, provide a comprehensive and nuanced response using System 3 thinking:

Context: {context}

Options:
{options_str}

Constraints:
{constraints_str}

Comprehensive analysis and decision:"""
            response = await self.anthropic.completion(prompt=prompt, max_tokens_to_sample=300)
            return response.completion.strip()
        except Exception as e:
            error_msg = f"Error in system_3_thinking: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return "Unable to process System 3 thinking due to an error."

if __name__ == "__main__":
    import asyncio

    async def main():
        service = SystemThinkingService()
        
        # Example usage
        context = "The project deadline is approaching, and there are still unfinished tasks."
        options = ["Work overtime", "Request deadline extension", "Reduce scope"]
        constraints = ["Limited budget", "Team fatigue", "Client expectations"]

        system1_response = await service.system_1_thinking(context)
        print("System 1 Response:", system1_response)

        system2_response = await service.system_2_thinking(context, options)
        print("System 2 Response:", system2_response)

        system3_response = await service.system_3_thinking(context, options, constraints)
        print("System 3 Response:", system3_response)

    asyncio.run(main())
