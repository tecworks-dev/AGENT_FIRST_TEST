
"""
Purpose: Implements code linting functionality.
Description: This module provides a CodeLinter class that can lint code and apply auto-fixes.
"""

import pylint.lint
from pylint.reporters.text import TextReporter
from io import StringIO
import traceback
from typing import List, Dict, Any

class CodeLinter:
    def __init__(self):
        self.pylint_options = [
            '--disable=C0111',  # Missing docstring
            '--disable=C0103',  # Invalid name
            '--disable=C0325',  # Unnecessary parens
            '--disable=W0611',  # Unused import
        ]

    def lint_code(self, code: str, language: str) -> List[Dict[str, Any]]:
        """
        Lint the given code and return a list of linting results.

        Args:
            code (str): The code to be linted.
            language (str): The programming language of the code.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing linting results.
        """
        if language.lower() != 'python':
            return [{'error': f'Linting not supported for {language}'}]

        try:
            output = StringIO()
            reporter = TextReporter(output)
            pylint.lint.Run(['-'], reporter=reporter, exit=False, args=self.pylint_options)
            linting_output = output.getvalue()

            lint_results = []
            for line in linting_output.split('\n'):
                if ':' in line:
                    parts = line.split(':')
                    if len(parts) >= 3:
                        lint_results.append({
                            'line': parts[1],
                            'column': parts[2].split(',')[0] if ',' in parts[2] else '',
                            'type': parts[2].split(',')[1].strip() if ',' in parts[2] else '',
                            'message': ':'.join(parts[3:]).strip()
                        })

            if __debug__:
                print(f"Linting results: {lint_results}")

            return lint_results
        except Exception as e:
            error_message = f"Error during linting: {str(e)}"
            if __debug__:
                print(f"Error: {error_message}")
                print(traceback.format_exc())
            return [{'error': error_message}]

    def apply_auto_fixes(self, code: str, lint_results: List[Dict[str, Any]]) -> str:
        """
        Apply automatic fixes to the code based on linting results.

        Args:
            code (str): The original code.
            lint_results (List[Dict[str, Any]]): The linting results.

        Returns:
            str: The code with automatic fixes applied.
        """
        lines = code.split('\n')
        for result in reversed(lint_results):
            if 'line' in result and 'message' in result:
                line_number = int(result['line']) - 1
                if 0 <= line_number < len(lines):
                    if 'unused import' in result['message'].lower():
                        lines[line_number] = '# ' + lines[line_number]  # Comment out unused imports
                    elif 'missing whitespace' in result['message'].lower():
                        lines[line_number] = lines[line_number].replace('=', ' = ')  # Add whitespace around '='

        fixed_code = '\n'.join(lines)

        if __debug__:
            print(f"Original code:\n{code}")
            print(f"Fixed code:\n{fixed_code}")

        return fixed_code

if __name__ == "__main__":
    # Example usage
    linter = CodeLinter()
    sample_code = """
def add(a,b):
    return a+b

unused_var=10
    """
    lint_results = linter.lint_code(sample_code, 'python')
    print("Lint results:", lint_results)
    fixed_code = linter.apply_auto_fixes(sample_code, lint_results)
    print("Fixed code:", fixed_code)
