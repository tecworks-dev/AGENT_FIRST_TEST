
# app/utils/code_similarity_checker.py
"""
Checks for code similarity to detect potential plagiarism or code duplication.
"""

import logging
from typing import List, Dict, Any
from difflib import SequenceMatcher
from app.models import Project, File
from app import db

class CodeSimilarityChecker:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def check_similarity(self, code1: str, code2: str) -> float:
        """
        Calculate the similarity ratio between two code snippets.

        Args:
            code1 (str): The first code snippet.
            code2 (str): The second code snippet.

        Returns:
            float: A similarity ratio between 0 and 1, where 1 means identical.
        """
        if not code1 or not code2:
            return 0.0

        try:
            return SequenceMatcher(None, code1, code2).ratio()
        except Exception as e:
            self.logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0

    def find_similar_code_blocks(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Find similar code blocks within a project.

        Args:
            project_id (int): The ID of the project to analyze.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing information about similar code blocks.
        """
        similar_blocks = []
        try:
            project = Project.query.get(project_id)
            if not project:
                self.logger.error(f"Project with id {project_id} not found.")
                return similar_blocks

            files = File.query.filter_by(project_id=project_id).all()
            
            for i, file1 in enumerate(files):
                for j, file2 in enumerate(files[i+1:], start=i+1):
                    similarity = self.check_similarity(file1.content, file2.content)
                    if similarity > 0.8:  # Threshold for similarity
                        similar_blocks.append({
                            'file1': file1.name,
                            'file2': file2.name,
                            'similarity': similarity
                        })

        except Exception as e:
            self.logger.error(f"Error finding similar code blocks: {str(e)}")

        return similar_blocks

    def generate_similarity_report(self, project_id: int) -> str:
        """
        Generate a report of code similarities within a project.

        Args:
            project_id (int): The ID of the project to analyze.

        Returns:
            str: A formatted report of code similarities.
        """
        similar_blocks = self.find_similar_code_blocks(project_id)
        report = "Code Similarity Report\n"
        report += "========================\n\n"

        if not similar_blocks:
            report += "No significant code similarities found.\n"
        else:
            for block in similar_blocks:
                report += f"Similar code found in:\n"
                report += f"  File 1: {block['file1']}\n"
                report += f"  File 2: {block['file2']}\n"
                report += f"  Similarity: {block['similarity']:.2%}\n\n"

        return report

    def suggest_refactoring(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Suggest refactoring based on code similarities.

        Args:
            project_id (int): The ID of the project to analyze.

        Returns:
            List[Dict[str, Any]]: A list of refactoring suggestions.
        """
        similar_blocks = self.find_similar_code_blocks(project_id)
        suggestions = []

        for block in similar_blocks:
            suggestion = {
                'files': [block['file1'], block['file2']],
                'similarity': block['similarity'],
                'suggestion': f"Consider refactoring similar code in {block['file1']} and {block['file2']}. "
                              f"You might be able to create a shared function or class to reduce duplication."
            }
            suggestions.append(suggestion)

        return suggestions

if __name__ == "__main__":
    # This block is for testing purposes only
    checker = CodeSimilarityChecker()
    
    # Example usage
    code1 = """
    def add(a, b):
        return a + b
    """
    
    code2 = """
    def add(x, y):
        return x + y
    """
    
    similarity = checker.check_similarity(code1, code2)
    print(f"Similarity between code snippets: {similarity:.2%}")

