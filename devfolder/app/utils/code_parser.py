
"""
app/utils/code_parser.py

This file implements code parsing functionality for the AI Software Factory.
It provides a CodeParser class that can parse code in different programming languages
and return a structured representation of the code.
"""

import ast
import traceback
from typing import Dict, Any, List

class CodeParser:
    def __init__(self):
        self.supported_languages = ['python', 'javascript']  # Add more languages as needed

    def parse_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Parse the given code in the specified language and return a structured representation.

        Args:
            code (str): The source code to parse.
            language (str): The programming language of the code.

        Returns:
            Dict[str, Any]: A dictionary containing the parsed code structure.
        """
        if DEBUG:
            print(f"Parsing code in {language}")

        try:
            if language.lower() not in self.supported_languages:
                raise ValueError(f"Unsupported language: {language}")

            if language.lower() == 'python':
                return self._parse_python(code)
            elif language.lower() == 'javascript':
                return self._parse_javascript(code)
            else:
                raise NotImplementedError(f"Parsing for {language} is not yet implemented")

        except Exception as e:
            error_msg = f"Error parsing {language} code: {str(e)}"
            if DEBUG:
                print(error_msg)
                print(traceback.format_exc())
            return {"error": error_msg}

    def _parse_python(self, code: str) -> Dict[str, Any]:
        """
        Parse Python code using the ast module.

        Args:
            code (str): The Python source code to parse.

        Returns:
            Dict[str, Any]: A dictionary containing the parsed Python code structure.
        """
        try:
            tree = ast.parse(code)
            return {
                "type": "module",
                "body": self._parse_python_node(tree)
            }
        except SyntaxError as e:
            return {"error": f"Python syntax error: {str(e)}"}

    def _parse_python_node(self, node: ast.AST) -> Dict[str, Any]:
        """
        Recursively parse a Python AST node.

        Args:
            node (ast.AST): The AST node to parse.

        Returns:
            Dict[str, Any]: A dictionary representing the parsed node.
        """
        if isinstance(node, ast.FunctionDef):
            return {
                "type": "function",
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "body": [self._parse_python_node(n) for n in node.body]
            }
        elif isinstance(node, ast.ClassDef):
            return {
                "type": "class",
                "name": node.name,
                "body": [self._parse_python_node(n) for n in node.body]
            }
        elif isinstance(node, ast.Assign):
            return {
                "type": "assignment",
                "targets": [self._parse_python_node(t) for t in node.targets],
                "value": self._parse_python_node(node.value)
            }
        elif isinstance(node, ast.Name):
            return {
                "type": "name",
                "id": node.id
            }
        elif isinstance(node, ast.Num):
            return {
                "type": "number",
                "value": node.n
            }
        elif isinstance(node, ast.Str):
            return {
                "type": "string",
                "value": node.s
            }
        elif isinstance(node, ast.Module):
            return [self._parse_python_node(n) for n in node.body]
        else:
            return {
                "type": node.__class__.__name__,
                "details": str(node)
            }

    def _parse_javascript(self, code: str) -> Dict[str, Any]:
        """
        Parse JavaScript code.

        Args:
            code (str): The JavaScript source code to parse.

        Returns:
            Dict[str, Any]: A dictionary containing the parsed JavaScript code structure.
        """
        # This is a placeholder for JavaScript parsing
        # In a real implementation, you would use a JavaScript parser like esprima
        return {
            "type": "module",
            "body": [{"type": "placeholder", "details": "JavaScript parsing not yet implemented"}]
        }

# Global debug flag
DEBUG = True

if __name__ == "__main__":
    # Example usage
    parser = CodeParser()
    python_code = """
def hello_world():
    print("Hello, World!")

class Example:
    def __init__(self):
        self.value = 42
    """
    result = parser.parse_code(python_code, "python")
    print(result)
