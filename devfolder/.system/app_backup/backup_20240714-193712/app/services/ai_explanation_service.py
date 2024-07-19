
# app/services/ai_explanation_service.py
"""
Provides AI-generated explanations for code and concepts.
This service uses the Anthropic API to generate explanations and code comments.
"""

import traceback
from typing import Dict, Any
from app.utils.api_utils import AsyncAnthropic

class AIExplanationService:
    def __init__(self):
        self.client = AsyncAnthropic()

    async def explain_code(self, code: str, language: str) -> str:
        """
        Generate an explanation for the given code snippet.

        Args:
            code (str): The code snippet to explain.
            language (str): The programming language of the code.

        Returns:
            str: An AI-generated explanation of the code.
        """
        try:
            prompt = f"Please explain the following {language} code:\n\n{code}\n\nExplanation:"
            response = await self.client.generate_text(prompt)
            return response.strip()
        except Exception as e:
            error_msg = f"Error in explain_code: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return f"An error occurred while generating the explanation: {error_msg}"

    async def explain_concept(self, concept: str, context: str) -> str:
        """
        Generate an explanation for a given concept within a specific context.

        Args:
            concept (str): The concept to explain.
            context (str): Additional context or domain information.

        Returns:
            str: An AI-generated explanation of the concept.
        """
        try:
            prompt = f"Please explain the concept of '{concept}' in the context of {context}:"
            response = await self.client.generate_text(prompt)
            return response.strip()
        except Exception as e:
            error_msg = f"Error in explain_concept: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return f"An error occurred while explaining the concept: {error_msg}"

    async def generate_code_comments(self, code: str, language: str) -> str:
        """
        Generate inline comments for the given code snippet.

        Args:
            code (str): The code snippet to comment.
            language (str): The programming language of the code.

        Returns:
            str: The original code with AI-generated inline comments.
        """
        try:
            prompt = f"Please add inline comments to explain the following {language} code. Return the code with comments added:\n\n{code}"
            response = await self.client.generate_text(prompt)
            return response.strip()
        except Exception as e:
            error_msg = f"Error in generate_code_comments: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return f"An error occurred while generating code comments: {error_msg}"

    async def debug_code(self, code: str, error_message: str, language: str) -> Dict[str, Any]:
        """
        Analyze code and provide debugging suggestions based on an error message.

        Args:
            code (str): The code snippet with an error.
            error_message (str): The error message or stack trace.
            language (str): The programming language of the code.

        Returns:
            Dict[str, Any]: A dictionary containing the analysis and suggestions.
        """
        try:
            prompt = f"""
            Please analyze the following {language} code and the accompanying error message.
            Provide a diagnosis of the problem and suggest a fix.

            Code:
            {code}

            Error Message:
            {error_message}

            Analysis and Fix:
            """
            response = await self.client.generate_text(prompt)
            return {
                "analysis": response.strip(),
                "original_code": code,
                "error_message": error_message
            }
        except Exception as e:
            error_msg = f"Error in debug_code: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return {
                "analysis": f"An error occurred while debugging the code: {error_msg}",
                "original_code": code,
                "error_message": error_message
            }

# Debugging statements
if __name__ == "__main__":
    import asyncio
    import os

    async def test_service():
        service = AIExplanationService()
        
        # Test explain_code
        code_snippet = """
        def fibonacci(n):
            if n <= 1:
                return n
            else:
                return fibonacci(n-1) + fibonacci(n-2)
        """
        explanation = await service.explain_code(code_snippet, "Python")
        print("Code Explanation:", explanation)

        # Test explain_concept
        concept_explanation = await service.explain_concept("recursion", "computer programming")
        print("Concept Explanation:", concept_explanation)

        # Test generate_code_comments
        commented_code = await service.generate_code_comments(code_snippet, "Python")
        print("Commented Code:", commented_code)

        # Test debug_code
        error_code = """
        def divide(a, b):
            return a / b

        result = divide(10, 0)
        print(result)
        """
        error_message = "ZeroDivisionError: division by zero"
        debug_result = await service.debug_code(error_code, error_message, "Python")
        print("Debug Result:", debug_result)

    asyncio.run(test_service())
