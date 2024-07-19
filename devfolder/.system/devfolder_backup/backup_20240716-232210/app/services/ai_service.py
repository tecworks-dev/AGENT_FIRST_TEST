
# app/services/ai_service.py
"""
This module provides AI-related services without direct database interactions.
It includes functionalities for text generation, code analysis, unit test generation,
and code optimization using the Anthropic API.
"""

from typing import Dict, Any, List
from app.utils.api_utils import AsyncAnthropic
import os
import traceback

class AIService:
    def __init__(self):
        self.anthropic = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def generate_text(self, prompt: str, max_tokens: int) -> str:
        """
        Generates text based on a prompt using the Anthropic API.

        Args:
            prompt (str): The input prompt for text generation.
            max_tokens (int): The maximum number of tokens to generate.

        Returns:
            str: The generated text.
        """
        try:
            response = await self.anthropic.completions.create(
                model="claude-2",
                prompt=prompt,
                max_tokens_to_sample=max_tokens
            )
            return response.completion
        except Exception as e:
            print(f"Error in generate_text: {str(e)}")
            traceback.print_exc()
            return ""

    async def analyze_code(self, code: str) -> Dict[str, Any]:
        """
        Analyzes code and returns insights using the Anthropic API.

        Args:
            code (str): The code to be analyzed.

        Returns:
            Dict[str, Any]: A dictionary containing code analysis results.
        """
        try:
            prompt = f"Analyze the following code and provide insights:\n\n{code}\n\nAnalysis:"
            response = await self.anthropic.completions.create(
                model="claude-2",
                prompt=prompt,
                max_tokens_to_sample=1000
            )
            
            # Parse the response and structure it as a dictionary
            analysis_lines = response.completion.strip().split("\n")
            analysis_dict = {}
            for line in analysis_lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    analysis_dict[key.strip()] = value.strip()
            
            return analysis_dict
        except Exception as e:
            print(f"Error in analyze_code: {str(e)}")
            traceback.print_exc()
            return {"error": str(e)}

    async def generate_unit_tests(self, code: str) -> List[str]:
        """
        Generates unit tests for given code using the Anthropic API.

        Args:
            code (str): The code for which to generate unit tests.

        Returns:
            List[str]: A list of generated unit tests.
        """
        try:
            prompt = f"Generate unit tests for the following code:\n\n{code}\n\nUnit tests:"
            response = await self.anthropic.completions.create(
                model="claude-2",
                prompt=prompt,
                max_tokens_to_sample=1500
            )
            
            # Split the response into individual test cases
            test_cases = response.completion.strip().split("\n\n")
            return [test.strip() for test in test_cases if test.strip()]
        except Exception as e:
            print(f"Error in generate_unit_tests: {str(e)}")
            traceback.print_exc()
            return []

    async def optimize_code(self, code: str) -> str:
        """
        Suggests optimizations for given code using the Anthropic API.

        Args:
            code (str): The code to be optimized.

        Returns:
            str: The optimized code.
        """
        try:
            prompt = f"Optimize the following code:\n\n{code}\n\nOptimized code:"
            response = await self.anthropic.completions.create(
                model="claude-2",
                prompt=prompt,
                max_tokens_to_sample=2000
            )
            return response.completion.strip()
        except Exception as e:
            print(f"Error in optimize_code: {str(e)}")
            traceback.print_exc()
            return code  # Return original code if optimization fails

if __name__ == "__main__":
    # This block is for testing purposes only
    import asyncio

    async def test_ai_service():
        ai_service = AIService()
        
        # Test generate_text
        text = await ai_service.generate_text("Write a short poem about AI.", 100)
        print("Generated Text:", text)

        # Test analyze_code
        sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
        """
        analysis = await ai_service.analyze_code(sample_code)
        print("Code Analysis:", analysis)

        # Test generate_unit_tests
        tests = await ai_service.generate_unit_tests(sample_code)
        print("Generated Unit Tests:", tests)

        # Test optimize_code
        optimized = await ai_service.optimize_code(sample_code)
        print("Optimized Code:", optimized)

    asyncio.run(test_ai_service())
