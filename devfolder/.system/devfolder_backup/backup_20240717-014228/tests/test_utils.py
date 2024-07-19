
# Purpose: Contains unit tests for various utility classes.
# Description: This file includes comprehensive unit tests for utility classes such as CodeAnalyzer, 
# CodeComplexityAnalyzer, CodeDiff, CodeFormatter, CodeGenerator, and CodeLinter.

import pytest
from app.utils import (
    CodeAnalyzer, CodeComplexityAnalyzer, CodeDiff,
    CodeFormatter, CodeGenerator, CodeLinter
)

class TestCodeAnalyzer:
    def test_analyze_complexity(self):
        analyzer = CodeAnalyzer()
        code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
"""
        result = analyzer.analyze_complexity(code)
        assert 'cyclomatic_complexity' in result
        assert result['cyclomatic_complexity'] > 0

    def test_detect_code_smells(self):
        analyzer = CodeAnalyzer()
        code = """
def long_function():
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    return a + b + c + d + e + f + g + h + i + j
"""
        smells = analyzer.detect_code_smells(code)
        assert len(smells) > 0
        assert any('long function' in smell['description'].lower() for smell in smells)

    def test_suggest_improvements(self):
        analyzer = CodeAnalyzer()
        analysis_result = {
            'cyclomatic_complexity': 10,
            'maintainability_index': 20,
            'code_smells': [{'type': 'long_function', 'description': 'Function is too long'}]
        }
        suggestions = analyzer.suggest_improvements(analysis_result)
        assert len(suggestions) > 0
        assert any('reduce complexity' in suggestion.lower() for suggestion in suggestions)

class TestCodeComplexityAnalyzer:
    def test_calculate_cyclomatic_complexity(self):
        analyzer = CodeComplexityAnalyzer()
        code = """
def complex_function(a, b):
    if a > b:
        if a > 10:
            return a
        else:
            return b
    elif b > a:
        return b
    else:
        return a + b
"""
        complexity = analyzer.calculate_cyclomatic_complexity(code)
        assert complexity > 1

    def test_calculate_cognitive_complexity(self):
        analyzer = CodeComplexityAnalyzer()
        code = """
def cognitive_complex_function(a, b, c):
    if a > b:
        for i in range(c):
            if i % 2 == 0:
                print(i)
            else:
                print(i * 2)
    elif b > a:
        while c > 0:
            c -= 1
    else:
        return a + b + c
"""
        complexity = analyzer.calculate_cognitive_complexity(code)
        assert complexity > 1

    def test_generate_complexity_report(self):
        analyzer = CodeComplexityAnalyzer()
        project_path = '/path/to/project'  # Mock path
        report = analyzer.generate_complexity_report(project_path)
        assert 'average_cyclomatic_complexity' in report
        assert 'average_cognitive_complexity' in report
        assert 'files_analyzed' in report

class TestCodeDiff:
    def test_generate_diff(self):
        diff_tool = CodeDiff()
        old_code = "def hello():\n    print('Hello')\n"
        new_code = "def hello():\n    print('Hello, World!')\n"
        diff = diff_tool.generate_diff(old_code, new_code)
        assert '-    print(\'Hello\')' in diff
        assert '+    print(\'Hello, World!\')' in diff

    def test_apply_patch(self):
        diff_tool = CodeDiff()
        original_code = "def greet(name):\n    print('Hello')\n"
        patch = "@@ -1,2 +1,2 @@\n def greet(name):\n-    print('Hello')\n+    print(f'Hello, {name}!')\n"
        patched_code = diff_tool.apply_patch(original_code, patch)
        assert "print(f'Hello, {name}!')" in patched_code

class TestCodeFormatter:
    def test_format_code(self):
        formatter = CodeFormatter()
        unformatted_code = "def messy_function( a,b ):\n  return a+b"
        formatted_code = formatter.format_code(unformatted_code, 'python', 'pep8')
        assert 'def messy_function(a, b):' in formatted_code
        assert 'return a + b' in formatted_code

    def test_detect_style_violations(self):
        formatter = CodeFormatter()
        code = "def bad_function( a,b ):\n  return a+b"
        violations = formatter.detect_style_violations(code, 'python', 'pep8')
        assert len(violations) > 0
        assert any('whitespace' in violation['description'].lower() for violation in violations)

class TestCodeGenerator:
    def test_generate_class_template(self):
        generator = CodeGenerator()
        class_name = 'TestClass'
        attributes = ['attr1', 'attr2']
        methods = ['method1', 'method2']
        template = generator.generate_class_template(class_name, attributes, methods)
        assert 'class TestClass:' in template
        assert 'def __init__(self' in template
        assert 'def method1(self):' in template
        assert 'def method2(self):' in template

    def test_generate_function_template(self):
        generator = CodeGenerator()
        func_name = 'test_function'
        params = ['param1', 'param2']
        return_type = 'int'
        template = generator.generate_function_template(func_name, params, return_type)
        assert 'def test_function(param1, param2)' in template
        assert '-> int:' in template

class TestCodeLinter:
    def test_lint_code(self):
        linter = CodeLinter()
        code = """
def poorly_formatted_function():
    x=1
    y=2
    z    =3
    return x+y+z
"""
        lint_results = linter.lint_code(code, 'python')
        assert len(lint_results) > 0
        assert any('whitespace' in result['message'].lower() for result in lint_results)

    def test_apply_auto_fixes(self):
        linter = CodeLinter()
        code = "def bad_function( a,b ):\n  return a+b"
        lint_results = [
            {'message': 'Missing whitespace after comma', 'line': 1, 'column': 20},
            {'message': 'Multiple spaces before operator', 'line': 2, 'column': 9}
        ]
        fixed_code = linter.apply_auto_fixes(code, lint_results)
        assert 'def bad_function(a, b):' in fixed_code
        assert 'return a + b' in fixed_code

if __name__ == '__main__':
    pytest.main()
