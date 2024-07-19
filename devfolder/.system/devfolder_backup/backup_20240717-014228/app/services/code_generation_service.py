
"""
Handles code generation tasks.

This module provides a CodeGenerationService class that uses AI to generate
and refactor code based on given specifications or instructions.
"""

from typing import Dict, Any, List, Tuple
from app.utils.api_utils import AsyncAnthropic
import os
import traceback

class CodeGenerationService:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def generate_code(self, specifications: Dict[str, Any]) -> List[Tuple[str, str]]:
        """
        Generate code based on the given specifications.

        Args:
            specifications (Dict[str, Any]): A dictionary containing the specifications for code generation.

        Returns:
            List[Tuple[str, str]]: A list of tuples containing the file name and generated code content.
        """
        try:
            generated_files = []
            prompt = f"Generate code based on the following specifications:\n{specifications}"
            
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            if response.content:
                # Parse the response and extract file names and code content
                # This is a simplified example; you may need to adjust based on the actual response format
                files = response.content[0].text.split("FILE:")
                for file in files[1:]:  # Skip the first empty split
                    lines = file.strip().split("\n")
                    file_name = lines[0].strip()
                    code_content = "\n".join(lines[1:])
                    generated_files.append((file_name, code_content))
            
            return generated_files

        except Exception as e:
            print(f"Error in generate_code: {str(e)}")
            traceback.print_exc()
            return []

    async def refactor_code(self, code: str, refactor_instructions: str) -> str:
        """
        Refactor the given code based on the provided instructions.

        Args:
            code (str): The original code to be refactored.
            refactor_instructions (str): Instructions for how to refactor the code.

        Returns:
            str: The refactored code.
        """
        try:
            prompt = f"""Refactor the following code according to these instructions:

Instructions:
{refactor_instructions}

Code:
{code}

Please provide only the refactored code in your response."""

            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            if response.content:
                return response.content[0].text.strip()
            else:
                return "Error: Unable to refactor code."

        except Exception as e:
            print(f"Error in refactor_code: {str(e)}")
            traceback.print_exc()
            return f"Error: {str(e)}"

# Example usage and testing
if __name__ == "__main__":
    import asyncio

    async def test_code_generation_service():
        service = CodeGenerationService()
        
        # Test generate_code
        specs = {
            "language": "Python",
            "task": "Create a simple Flask route that returns 'Hello, World!'",
        }
        generated_files = await service.generate_code(specs)
        print("Generated Files:")
        for file_name, content in generated_files:
            print(f"\nFile: {file_name}\n{content}\n{'='*50}")

        # Test refactor_code
        original_code = """
def calculate_sum(a, b):
    return a + b

result = calculate_sum(5, 10)
print(result)
        """
        refactor_instructions = "Add type hints and a docstring to the function."
        refactored_code = await service.refactor_code(original_code, refactor_instructions)
        print("\nRefactored Code:")
        print(refactored_code)

    asyncio.run(test_code_generation_service())
