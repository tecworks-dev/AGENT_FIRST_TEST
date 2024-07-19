
# app/services/error_fixing_service.py
"""
Handles error detection and fixing.
This service provides functionality to analyze code errors and suggest fixes using AI assistance.
"""

from typing import List
from app.utils.api_utils import AsyncAnthropic
import os
import traceback

class ErrorFixingService:
    def __init__(self):
        self.anthropic = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def analyze_and_fix_errors(self, code: str, error_message: str) -> str:
        """
        Analyzes the given code and error message, then attempts to fix the error.

        Args:
            code (str): The code containing the error.
            error_message (str): The error message produced by the code.

        Returns:
            str: The fixed code, or the original code if no fix could be found.
        """
        try:
            prompt = f"""
            Given the following Python code and error message, please analyze the issue and provide a fixed version of the code:

            Code:
            ```python
            {code}
            ```

            Error message:
            {error_message}

            Please provide only the fixed code without any explanations.
            """

            response = await self.anthropic.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            fixed_code = response.content[0].text.strip()

            if fixed_code.startswith("```python"):
                fixed_code = fixed_code[10:-3].strip()

            return fixed_code
        except Exception as e:
            print(f"Error in analyze_and_fix_errors: {str(e)}")
            traceback.print_exc()
            return code

    async def suggest_fixes(self, code: str, error_type: str) -> List[str]:
        """
        Suggests potential fixes for a given error type in the code.

        Args:
            code (str): The code to analyze.
            error_type (str): The type of error to suggest fixes for.

        Returns:
            List[str]: A list of suggested fixes.
        """
        try:
            prompt = f"""
            Given the following Python code and error type, please suggest up to 3 potential fixes:

            Code:
            ```python
            {code}
            ```

            Error type: {error_type}

            Please provide a list of suggested fixes, each on a new line, without any additional explanations.
            """

            response = await self.anthropic.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            suggestions = response.content[0].text.strip().split('\n')
            return [suggestion.strip() for suggestion in suggestions if suggestion.strip()]
        except Exception as e:
            print(f"Error in suggest_fixes: {str(e)}")
            traceback.print_exc()
            return []

if __name__ == "__main__":
    # This block is for testing purposes only
    import asyncio

    async def test_error_fixing_service():
        service = ErrorFixingService()
        
        # Test analyze_and_fix_errors
        code_with_error = """
        def divide(a, b):
            return a / b

        result = divide(10, 0)
        print(result)
        """
        error_message = "ZeroDivisionError: division by zero"
        
        fixed_code = await service.analyze_and_fix_errors(code_with_error, error_message)
        print("Fixed code:")
        print(fixed_code)
        
        # Test suggest_fixes
        code_with_type_error = """
        def greet(name):
            return "Hello, " + name

        result = greet(123)
        print(result)
        """
        error_type = "TypeError"
        
        suggestions = await service.suggest_fixes(code_with_type_error, error_type)
        print("Suggested fixes:")
        for suggestion in suggestions:
            print(f"- {suggestion}")

    asyncio.run(test_error_fixing_service())
