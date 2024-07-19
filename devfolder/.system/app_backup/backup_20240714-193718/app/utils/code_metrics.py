
"""
Implements code quality metrics calculation.

This module provides functionality to calculate various code quality metrics
using the radon library. It includes methods to assess cyclomatic complexity,
maintainability index, and other relevant metrics for different programming languages.
"""

import radon.metrics
from radon.visitors import ComplexityVisitor
from typing import Dict, Any

class CodeMetrics:
    """
    A class for calculating code quality metrics.
    """

    def calculate_metrics(self, code: str, language: str) -> Dict[str, Any]:
        """
        Calculate various code quality metrics for the given code.

        Args:
            code (str): The source code to analyze.
            language (str): The programming language of the code.

        Returns:
            Dict[str, Any]: A dictionary containing calculated metrics.
        """
        metrics = {}

        # Calculate cyclomatic complexity
        try:
            complexity_visitor = ComplexityVisitor.from_code(code)
            metrics['cyclomatic_complexity'] = complexity_visitor.total_complexity
        except Exception as e:
            metrics['cyclomatic_complexity'] = f"Error: {str(e)}"

        # Calculate Halstead metrics
        try:
            h_metrics = radon.metrics.h_visit(code)
            metrics['halstead_volume'] = h_metrics.volume
            metrics['halstead_difficulty'] = h_metrics.difficulty
            metrics['halstead_effort'] = h_metrics.effort
        except Exception as e:
            metrics['halstead_metrics'] = f"Error: {str(e)}"

        # Calculate maintainability index
        try:
            mi_score = radon.metrics.mi_visit(code, multi=True)
            metrics['maintainability_index'] = mi_score
        except Exception as e:
            metrics['maintainability_index'] = f"Error: {str(e)}"

        # Calculate raw metrics
        try:
            raw_metrics = radon.metrics.raw_metrics(code)
            metrics['loc'] = raw_metrics.loc
            metrics['lloc'] = raw_metrics.lloc
            metrics['sloc'] = raw_metrics.sloc
            metrics['comments'] = raw_metrics.comments
            metrics['multi'] = raw_metrics.multi
            metrics['blank'] = raw_metrics.blank
        except Exception as e:
            metrics['raw_metrics'] = f"Error: {str(e)}"

        # Add language-specific metrics if needed
        if language.lower() == 'python':
            try:
                ast_node_count = len(list(radon.metrics.ast_node_count(code)))
                metrics['ast_node_count'] = ast_node_count
            except Exception as e:
                metrics['ast_node_count'] = f"Error: {str(e)}"

        return metrics

if __name__ == "__main__":
    # Example usage
    code_metrics = CodeMetrics()
    sample_code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
    """
    results = code_metrics.calculate_metrics(sample_code, 'python')
    print("Code Metrics:")
    for metric, value in results.items():
        print(f"{metric}: {value}")

# Debugging statements (will only be executed if DEBUG is True)
if __debug__:
    print("Debug mode is on. CodeMetrics class is loaded.")
    print("Available methods: calculate_metrics")
