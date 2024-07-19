
# app/utils/code_complexity_analyzer.py
"""
Analyzes code complexity using various metrics.

This module provides a CodeComplexityAnalyzer class that calculates cyclomatic complexity,
cognitive complexity, and generates complexity reports for Python code.
"""

import ast
from typing import Dict, Any, List
import os
from radon.complexity import cc_visit
from radon.metrics import mi_visit
import traceback

DEBUG = True

class CodeComplexityAnalyzer:
    """
    A class for analyzing code complexity using various metrics.
    """

    def calculate_cyclomatic_complexity(self, code: str) -> int:
        """
        Calculate the cyclomatic complexity of the given code.

        Args:
            code (str): The Python code to analyze.

        Returns:
            int: The cyclomatic complexity score.
        """
        try:
            result = cc_visit(code)
            if DEBUG:
                print(f"Cyclomatic complexity calculated: {sum(cc.complexity for cc in result)}")
            return sum(cc.complexity for cc in result)
        except Exception as e:
            print(f"Error calculating cyclomatic complexity: {str(e)}")
            if DEBUG:
                traceback.print_exc()
            return -1

    def calculate_cognitive_complexity(self, code: str) -> int:
        """
        Calculate the cognitive complexity of the given code.

        Args:
            code (str): The Python code to analyze.

        Returns:
            int: The cognitive complexity score.
        """
        try:
            tree = ast.parse(code)
            cognitive_complexity = 0

            class CognitiveComplexityVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.complexity = 0
                    self.nesting_level = 0

                def visit_FunctionDef(self, node):
                    self.nesting_level += 1
                    self.generic_visit(node)
                    self.nesting_level -= 1

                def visit_If(self, node):
                    self.complexity += 1 + self.nesting_level
                    self.nesting_level += 1
                    self.generic_visit(node)
                    self.nesting_level -= 1

                def visit_For(self, node):
                    self.complexity += 1 + self.nesting_level
                    self.nesting_level += 1
                    self.generic_visit(node)
                    self.nesting_level -= 1

                def visit_While(self, node):
                    self.complexity += 1 + self.nesting_level
                    self.nesting_level += 1
                    self.generic_visit(node)
                    self.nesting_level -= 1

            visitor = CognitiveComplexityVisitor()
            visitor.visit(tree)
            cognitive_complexity = visitor.complexity

            if DEBUG:
                print(f"Cognitive complexity calculated: {cognitive_complexity}")
            return cognitive_complexity
        except Exception as e:
            print(f"Error calculating cognitive complexity: {str(e)}")
            if DEBUG:
                traceback.print_exc()
            return -1

    def generate_complexity_report(self, project_path: str) -> Dict[str, Any]:
        """
        Generate a complexity report for all Python files in the given project path.

        Args:
            project_path (str): The path to the project directory.

        Returns:
            Dict[str, Any]: A dictionary containing complexity metrics for each file.
        """
        try:
            report = {}
            for root, _, files in os.walk(project_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as f:
                            code = f.read()
                        
                        cyclomatic_complexity = self.calculate_cyclomatic_complexity(code)
                        cognitive_complexity = self.calculate_cognitive_complexity(code)
                        maintainability_index = mi_visit(code, multi=True)
                        
                        report[file_path] = {
                            'cyclomatic_complexity': cyclomatic_complexity,
                            'cognitive_complexity': cognitive_complexity,
                            'maintainability_index': maintainability_index
                        }
            
            if DEBUG:
                print(f"Complexity report generated for {len(report)} files")
            return report
        except Exception as e:
            print(f"Error generating complexity report: {str(e)}")
            if DEBUG:
                traceback.print_exc()
            return {}

if __name__ == "__main__":
    # Example usage
    analyzer = CodeComplexityAnalyzer()
    
    # Example code to analyze
    example_code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    """
    
    print("Example Code:")
    print(example_code)
    print("\nAnalysis Results:")
    print(f"Cyclomatic Complexity: {analyzer.calculate_cyclomatic_complexity(example_code)}")
    print(f"Cognitive Complexity: {analyzer.calculate_cognitive_complexity(example_code)}")
    
    # Example project path (replace with an actual path to test)
    example_project_path = "./example_project"
    if os.path.exists(example_project_path):
        print("\nProject Complexity Report:")
        print(analyzer.generate_complexity_report(example_project_path))
    else:
        print(f"\nExample project path '{example_project_path}' not found. Skipping project report.")
