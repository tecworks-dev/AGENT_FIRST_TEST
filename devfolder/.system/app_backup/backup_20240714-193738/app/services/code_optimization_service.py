
# Purpose: Handles code optimization tasks.
# Description: This service provides methods for optimizing code, profiling performance, and suggesting optimizations.

from typing import Dict, Any, List
from app.utils.api_utils import AsyncAnthropic
import os
import traceback
import asyncio

class CodeOptimizationService:
    def __init__(self):
        self.anthropic_client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def optimize_code(self, code: str, language: str) -> str:
        """
        Optimizes the given code using AI assistance.

        Args:
            code (str): The code to be optimized.
            language (str): The programming language of the code.

        Returns:
            str: The optimized code.
        """
        try:
            prompt = f"Please optimize the following {language} code:\n\n{code}\n\nProvide only the optimized code without explanations."
            response = await self.anthropic_client.completion(prompt=prompt, max_tokens_to_sample=2000)
            optimized_code = response.completion.strip()
            
            if os.environ.get("DEBUG") == "True":
                print(f"Original code:\n{code}\n\nOptimized code:\n{optimized_code}")
            
            return optimized_code
        except Exception as e:
            print(f"Error in optimize_code: {str(e)}")
            traceback.print_exc()
            return code  # Return original code if optimization fails

    async def profile_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Profiles the given code to identify performance bottlenecks.

        Args:
            code (str): The code to be profiled.
            language (str): The programming language of the code.

        Returns:
            Dict[str, Any]: A dictionary containing profiling results.
        """
        try:
            prompt = f"Analyze and profile the following {language} code for performance:\n\n{code}\n\nProvide a JSON object with the following structure:\n{{\"execution_time\": float, \"memory_usage\": float, \"bottlenecks\": [string], \"suggestions\": [string]}}"
            response = await self.anthropic_client.completion(prompt=prompt, max_tokens_to_sample=1000)
            profiling_result = eval(response.completion.strip())
            
            if os.environ.get("DEBUG") == "True":
                print(f"Profiling result: {profiling_result}")
            
            return profiling_result
        except Exception as e:
            print(f"Error in profile_code: {str(e)}")
            traceback.print_exc()
            return {"execution_time": 0, "memory_usage": 0, "bottlenecks": [], "suggestions": []}

    async def suggest_optimizations(self, profiling_result: Dict[str, Any]) -> List[str]:
        """
        Suggests optimizations based on the profiling result.

        Args:
            profiling_result (Dict[str, Any]): The result of code profiling.

        Returns:
            List[str]: A list of optimization suggestions.
        """
        try:
            prompt = f"Based on the following profiling result, suggest code optimizations:\n\n{profiling_result}\n\nProvide a list of optimization suggestions."
            response = await self.anthropic_client.completion(prompt=prompt, max_tokens_to_sample=1000)
            suggestions = eval(response.completion.strip())
            
            if os.environ.get("DEBUG") == "True":
                print(f"Optimization suggestions: {suggestions}")
            
            return suggestions
        except Exception as e:
            print(f"Error in suggest_optimizations: {str(e)}")
            traceback.print_exc()
            return []

if __name__ == "__main__":
    async def main():
        service = CodeOptimizationService()
        code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(30))
"""
        optimized_code = await service.optimize_code(code, "python")
        print("Optimized code:", optimized_code)

        profiling_result = await service.profile_code(code, "python")
        print("Profiling result:", profiling_result)

        suggestions = await service.suggest_optimizations(profiling_result)
        print("Optimization suggestions:", suggestions)

    asyncio.run(main())
