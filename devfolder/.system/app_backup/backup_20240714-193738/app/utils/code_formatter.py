
"""
Purpose: Formats code according to specified style guidelines.
Description: This module provides functionality to format code and detect style violations
using popular code formatting libraries like black and isort.
"""

import black
import isort
from typing import List, Dict, Any
import traceback

DEBUG = True

class CodeFormatter:
    def __init__(self):
        self.black_mode = black.Mode()
        self.isort_config = isort.Config(profile="black")

    def format_code(self, code: str, language: str, style_guide: str) -> str:
        """
        Format the given code according to the specified language and style guide.

        Args:
            code (str): The code to be formatted.
            language (str): The programming language of the code.
            style_guide (str): The style guide to follow (e.g., 'pep8', 'google').

        Returns:
            str: The formatted code.
        """
        try:
            if language.lower() == 'python':
                # Format with black
                formatted_code = black.format_str(code, mode=self.black_mode)
                
                # Sort imports with isort
                formatted_code = isort.code(formatted_code, config=self.isort_config)
                
                if DEBUG:
                    print(f"Code formatted successfully using {style_guide} style guide.")
                
                return formatted_code
            else:
                if DEBUG:
                    print(f"Formatting not supported for language: {language}")
                return code  # Return original code if language is not supported
        except Exception as e:
            if DEBUG:
                print(f"Error occurred while formatting code: {str(e)}")
                print(traceback.format_exc())
            return code  # Return original code if an error occurs

    def detect_style_violations(self, code: str, language: str, style_guide: str) -> List[Dict[str, Any]]:
        """
        Detect style violations in the given code.

        Args:
            code (str): The code to check for style violations.
            language (str): The programming language of the code.
            style_guide (str): The style guide to follow (e.g., 'pep8', 'google').

        Returns:
            List[Dict[str, Any]]: A list of detected style violations.
        """
        violations = []
        try:
            if language.lower() == 'python':
                # Use black to check for formatting issues
                try:
                    black.format_str(code, mode=self.black_mode)
                except black.NothingChanged:
                    pass  # No formatting issues
                except Exception as e:
                    violations.append({
                        "line": getattr(e, "lineno", None),
                        "message": str(e),
                        "type": "formatting"
                    })

                # Use isort to check for import sorting issues
                import_issues = isort.check_code_string(code, config=self.isort_config)
                if import_issues:
                    violations.append({
                        "line": None,
                        "message": "Import sorting issues detected",
                        "type": "import_sorting"
                    })

                if DEBUG:
                    print(f"Style violations detected: {len(violations)}")
            else:
                if DEBUG:
                    print(f"Style violation detection not supported for language: {language}")

        except Exception as e:
            if DEBUG:
                print(f"Error occurred while detecting style violations: {str(e)}")
                print(traceback.format_exc())

        return violations

if __name__ == "__main__":
    # Example usage
    formatter = CodeFormatter()
    
    sample_code = """
import sys
import os
def hello_world():
    print('Hello, World!')
    """
    
    formatted_code = formatter.format_code(sample_code, 'python', 'pep8')
    print("Formatted code:")
    print(formatted_code)
    
    violations = formatter.detect_style_violations(sample_code, 'python', 'pep8')
    print("Style violations:")
    print(violations)
