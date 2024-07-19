
"""
Handles code review processes.

This module provides functionality for conducting AI-assisted code reviews,
including analyzing code, generating review comments, and applying suggested changes.
"""

from typing import Dict, Any, List
from app.utils.api_utils import AsyncAnthropic
import os
import traceback

class CodeReviewService:
    def __init__(self):
        self.anthropic = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def review_code(self, code: str, language: str) -> List[Dict[str, Any]]:
        """
        Conduct an AI-assisted code review.

        Args:
            code (str): The code to be reviewed.
            language (str): The programming language of the code.

        Returns:
            List[Dict[str, Any]]: A list of review comments, each containing the line number,
            comment text, and suggested fix (if applicable).
        """
        try:
            prompt = f"""
            You are an expert code reviewer. Please review the following {language} code and provide
            detailed feedback. Focus on code quality, best practices, potential bugs, and performance
            issues. For each issue, provide the line number, a description of the problem, and a
            suggested fix if applicable.

            Code to review:
            ```{language}
            {code}
            ```

            Provide your review in the following format:
            [
                {{"line": <line_number>, "comment": "<comment_text>", "suggestion": "<suggested_fix>"}},
                ...
            ]
            """

            response = await self.anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            review_comments = eval(response.content[0].text)
            return review_comments

        except Exception as e:
            print(f"Error in review_code: {str(e)}")
            traceback.print_exc()
            return []

    async def apply_suggestion(self, code: str, suggestion: Dict[str, Any]) -> str:
        """
        Apply a suggested fix to the code.

        Args:
            code (str): The original code.
            suggestion (Dict[str, Any]): A dictionary containing the line number and suggested fix.

        Returns:
            str: The updated code with the suggestion applied.
        """
        try:
            lines = code.split('\n')
            line_number = suggestion['line']
            suggested_fix = suggestion['suggestion']

            if 0 <= line_number < len(lines):
                lines[line_number] = suggested_fix
            
            return '\n'.join(lines)

        except Exception as e:
            print(f"Error in apply_suggestion: {str(e)}")
            traceback.print_exc()
            return code

if __name__ == "__main__":
    import asyncio

    async def test_code_review_service():
        service = CodeReviewService()
        
        test_code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# Calculate factorial of 5
result = factorial(5)
print(f"Factorial of 5 is {result}")
        """

        review_comments = await service.review_code(test_code, "python")
        print("Review comments:")
        for comment in review_comments:
            print(comment)

        if review_comments:
            updated_code = await service.apply_suggestion(test_code, review_comments[0])
            print("\nUpdated code:")
            print(updated_code)

    asyncio.run(test_code_review_service())
