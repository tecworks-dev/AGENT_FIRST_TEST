
# app/utils/code_analyzer.py
"""
Provides code analysis utilities.

This module contains the CodeAnalyzer class, which offers methods for analyzing
code complexity, detecting code smells, and suggesting improvements.
"""

import ast
import radon.metrics
from radon.visitors import ComplexityVisitor
from typing import Dict, Any, List
import traceback

DEBUG = True

class CodeAnalyzer:
    def analyze_complexity(self, code: str) -> Dict[str, Any]:
        """
        Analyzes the complexity of the given code.

        Args:
            code (str): The code to analyze.

        Returns:
            Dict[str, Any]: A dictionary containing complexity metrics.
        """
        try:
            if DEBUG:
                print(f"Analyzing complexity of code:\n{code[:100]}...")

            # Parse the code into an AST
            tree = ast.parse(code)

            # Calculate cyclomatic complexity
            cv = ComplexityVisitor.from_ast(tree)
            cyclomatic_complexity = cv.total_complexity

            # Calculate Halstead metrics
            h = radon.metrics.h_visit(code)
            halstead_metrics = {
                'h1': h.h1,
                'h2': h2,
                'N1': h.N1,
                'N2': h.N2,
                'vocabulary': h.vocabulary,
                'length': h.length,
                'calculated_length': h.calculated_length,
                'volume': h.volume,
                'difficulty': h.difficulty,
                'effort': h.effort,
                'time': h.time,
                'bugs': h.bugs
            }

            # Calculate maintainability index
            mi = radon.metrics.mi_visit(code, multi=True)

            result = {
                'cyclomatic_complexity': cyclomatic_complexity,
                'halstead_metrics': halstead_metrics,
                'maintainability_index': mi
            }

            if DEBUG:
                print(f"Complexity analysis result: {result}")

            return result
        except Exception as e:
            if DEBUG:
                print(f"Error in analyze_complexity: {str(e)}")
                print(traceback.format_exc())
            return {'error': str(e)}

    def detect_code_smells(self, code: str) -> List[Dict[str, Any]]:
        """
        Detects potential code smells in the given code.

        Args:
            code (str): The code to analyze.

        Returns:
            List[Dict[str, Any]]: A list of detected code smells.
        """
        try:
            if DEBUG:
                print(f"Detecting code smells in code:\n{code[:100]}...")

            smells = []

            # Parse the code into an AST
            tree = ast.parse(code)

            # Check for long functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if len(node.body) > 20:  # Arbitrary threshold
                        smells.append({
                            'type': 'Long Function',
                            'location': f'Function {node.name} at line {node.lineno}',
                            'description': f'Function {node.name} has {len(node.body)} lines, which may be too long.'
                        })

            # Check for deep nesting
            def check_nesting(node, depth=0):
                if isinstance(node, (ast.If, ast.For, ast.While)):
                    if depth > 3:  # Arbitrary threshold
                        smells.append({
                            'type': 'Deep Nesting',
                            'location': f'Line {node.lineno}',
                            'description': f'Nesting depth of {depth} at line {node.lineno} may be too deep.'
                        })
                    for child in ast.iter_child_nodes(node):
                        check_nesting(child, depth + 1)
                else:
                    for child in ast.iter_child_nodes(node):
                        check_nesting(child, depth)

            check_nesting(tree)

            if DEBUG:
                print(f"Detected {len(smells)} code smells: {smells}")

            return smells
        except Exception as e:
            if DEBUG:
                print(f"Error in detect_code_smells: {str(e)}")
                print(traceback.format_exc())
            return [{'error': str(e)}]

    def suggest_improvements(self, analysis_result: Dict[str, Any]) -> List[str]:
        """
        Suggests improvements based on the analysis result.

        Args:
            analysis_result (Dict[str, Any]): The result from analyze_complexity.

        Returns:
            List[str]: A list of suggested improvements.
        """
        try:
            if DEBUG:
                print(f"Suggesting improvements based on analysis result: {analysis_result}")

            suggestions = []

            cc = analysis_result.get('cyclomatic_complexity', 0)
            if cc > 10:
                suggestions.append(f"Consider refactoring to reduce cyclomatic complexity (current: {cc}).")

            mi = analysis_result.get('maintainability_index', 0)
            if mi < 65:
                suggestions.append(f"The code may be difficult to maintain (MI: {mi}). Consider simplifying.")

            halstead = analysis_result.get('halstead_metrics', {})
            if halstead.get('difficulty', 0) > 30:
                suggestions.append("The code may be too complex. Consider breaking it into smaller functions.")

            if DEBUG:
                print(f"Generated {len(suggestions)} improvement suggestions: {suggestions}")

            return suggestions
        except Exception as e:
            if DEBUG:
                print(f"Error in suggest_improvements: {str(e)}")
                print(traceback.format_exc())
            return [f"Error generating suggestions: {str(e)}"]

if __name__ == "__main__":
    # Simple test
    code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
    """
    analyzer = CodeAnalyzer()
    complexity = analyzer.analyze_complexity(code)
    smells = analyzer.detect_code_smells(code)
    suggestions = analyzer.suggest_improvements(complexity)
    
    print("Complexity:", complexity)
    print("Code Smells:", smells)
    print("Suggestions:", suggestions)
