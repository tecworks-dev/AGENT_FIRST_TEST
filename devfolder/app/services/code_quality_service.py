
# app/services/code_quality_service.py
"""
This module handles code quality checks and improvements.
It provides services for analyzing code quality, suggesting improvements,
and applying those improvements to the code.
"""

from typing import Dict, Any, List
from app.utils.code_analyzer import CodeAnalyzer
import traceback


class CodeQualityService:
    def __init__(self):
        self.code_analyzer = CodeAnalyzer()

    def analyze_code_quality(self, code: str, language: str) -> Dict[str, Any]:
        """
        Analyzes the quality of the given code.

        Args:
            code (str): The code to analyze.
            language (str): The programming language of the code.

        Returns:
            Dict[str, Any]: A dictionary containing various code quality metrics.
        """
        try:
            # Perform code quality analysis using the CodeAnalyzer
            complexity = self.code_analyzer.analyze_complexity(code)
            code_smells = self.code_analyzer.detect_code_smells(code)

            # Calculate additional metrics
            lines_of_code = len(code.split('\n'))
            comment_ratio = self._calculate_comment_ratio(code)

            analysis_result = {
                "complexity": complexity,
                "code_smells": code_smells,
                "lines_of_code": lines_of_code,
                "comment_ratio": comment_ratio,
                "language": language
            }

            if __debug__:
                print(f"Code quality analysis completed for {language} code.")

            return analysis_result
        except Exception as e:
            print(f"Error in analyze_code_quality: {str(e)}")
            traceback.print_exc()
            return {"error": str(e)}

    def suggest_improvements(self, analysis_result: Dict[str, Any]) -> List[str]:
        """
        Suggests improvements based on the code quality analysis result.

        Args:
            analysis_result (Dict[str, Any]): The result of the code quality analysis.

        Returns:
            List[str]: A list of suggested improvements.
        """
        try:
            suggestions = []

            # Suggest improvements based on complexity
            if analysis_result["complexity"]["cyclomatic_complexity"] > 10:
                suggestions.append("Consider breaking down complex functions to reduce cyclomatic complexity.")

            # Suggest improvements based on code smells
            for smell in analysis_result["code_smells"]:
                suggestions.append(f"Address the code smell: {smell['type']} - {smell['description']}")

            # Suggest improvements based on comment ratio
            if analysis_result["comment_ratio"] < 0.1:
                suggestions.append("Consider adding more comments to improve code readability.")

            if __debug__:
                print(f"Generated {len(suggestions)} improvement suggestions.")

            return suggestions
        except Exception as e:
            print(f"Error in suggest_improvements: {str(e)}")
            traceback.print_exc()
            return ["Error generating suggestions"]

    def apply_improvements(self, code: str, improvements: List[str]) -> str:
        """
        Applies the suggested improvements to the code.

        Args:
            code (str): The original code.
            improvements (List[str]): The list of improvements to apply.

        Returns:
            str: The improved code.
        """
        try:
            improved_code = code

            for improvement in improvements:
                if "breaking down complex functions" in improvement:
                    improved_code = self._break_down_complex_functions(improved_code)
                elif "adding more comments" in improvement:
                    improved_code = self._add_comments(improved_code)
                # Add more improvement applications as needed

            if __debug__:
                print(f"Applied {len(improvements)} improvements to the code.")

            return improved_code
        except Exception as e:
            print(f"Error in apply_improvements: {str(e)}")
            traceback.print_exc()
            return code  # Return original code if improvements fail

    def _calculate_comment_ratio(self, code: str) -> float:
        """
        Calculates the ratio of comments to code.

        Args:
            code (str): The code to analyze.

        Returns:
            float: The ratio of comments to code.
        """
        lines = code.split('\n')
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        total_lines = len(lines)
        return comment_lines / total_lines if total_lines > 0 else 0

    def _break_down_complex_functions(self, code: str) -> str:
        """
        Breaks down complex functions in the code.
        This is a placeholder and should be implemented with more sophisticated logic.

        Args:
            code (str): The code to improve.

        Returns:
            str: The improved code with complex functions broken down.
        """
        # Placeholder implementation
        return code

    def _add_comments(self, code: str) -> str:
        """
        Adds comments to the code to improve readability.
        This is a placeholder and should be implemented with more sophisticated logic.

        Args:
            code (str): The code to improve.

        Returns:
            str: The improved code with additional comments.
        """
        # Placeholder implementation
        return code


if __name__ == "__main__":
    # For testing purposes
    service = CodeQualityService()
    sample_code = """
def complex_function(a, b, c):
    if a > b:
        if b > c:
            return a
        elif a > c:
            return b
        else:
            return c
    elif b > c:
        return b
    else:
        return c
    """
    analysis = service.analyze_code_quality(sample_code, "python")
    suggestions = service.suggest_improvements(analysis)
    improved_code = service.apply_improvements(sample_code, suggestions)
    print("Analysis:", analysis)
    print("Suggestions:", suggestions)
    print("Improved Code:", improved_code)
