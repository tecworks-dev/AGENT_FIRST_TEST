
"""
app/services/code_explanation_service.py

This module provides a service for explaining complex code snippets and generating code summaries.
It uses the AsyncAnthropic API to leverage AI capabilities for code explanation.
"""

from app.utils.api_utils import AsyncAnthropic
import os
import traceback

class CodeExplanationService:
    def __init__(self):
        self.anthropic = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def explain_code(self, code: str, language: str) -> str:
        """
        Generates an explanation for the given code snippet.

        Args:
            code (str): The code snippet to explain.
            language (str): The programming language of the code.

        Returns:
            str: A detailed explanation of the code.
        """
        try:
            prompt = f"Explain the following {language} code in detail:\n\n```{language}\n{code}\n```"
            response = await self.anthropic.completion(prompt=prompt)
            return response.completion

        except Exception as e:
            error_msg = f"Error in explain_code: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return f"An error occurred while explaining the code: {error_msg}"

    async def generate_code_summary(self, code: str, language: str) -> str:
        """
        Generates a concise summary of the given code snippet.

        Args:
            code (str): The code snippet to summarize.
            language (str): The programming language of the code.

        Returns:
            str: A concise summary of the code.
        """
        try:
            prompt = f"Provide a concise summary of the following {language} code:\n\n```{language}\n{code}\n```"
            response = await self.anthropic.completion(prompt=prompt)
            return response.completion

        except Exception as e:
            error_msg = f"Error in generate_code_summary: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return f"An error occurred while generating the code summary: {error_msg}"

# Debugging statements
if __name__ == "__main__" and os.environ.get("DEBUG") == "True":
    import asyncio

    async def debug_code_explanation_service():
        service = CodeExplanationService()
        
        # Test code explanation
        test_code = """
        def fibonacci(n):
            if n <= 1:
                return n
            else:
                return fibonacci(n-1) + fibonacci(n-2)
        """
        explanation = await service.explain_code(test_code, "python")
        print("Code Explanation:")
        print(explanation)
        
        # Test code summary
        summary = await service.generate_code_summary(test_code, "python")
        print("\nCode Summary:")
        print(summary)

    asyncio.run(debug_code_explanation_service())
