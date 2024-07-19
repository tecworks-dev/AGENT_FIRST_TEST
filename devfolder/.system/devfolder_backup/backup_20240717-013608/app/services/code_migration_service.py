
"""
Purpose: Handles code migration between different programming languages.
Description: This service provides functionality to migrate code from one programming language to another,
             and analyze the feasibility of such migrations.
"""

from typing import Dict, Any
from app.utils.api_utils import AsyncAnthropic
import os
import traceback

class CodeMigrationService:
    def __init__(self):
        self.anthropic = AsyncAnthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    async def migrate_code(self, code: str, source_language: str, target_language: str) -> str:
        """
        Migrates code from the source language to the target language.

        Args:
            code (str): The source code to be migrated.
            source_language (str): The programming language of the source code.
            target_language (str): The target programming language for migration.

        Returns:
            str: The migrated code in the target language.
        """
        try:
            prompt = f"""
            You are an expert programmer in both {source_language} and {target_language}.
            Please migrate the following {source_language} code to {target_language}:

            {code}

            Ensure that the migrated code maintains the same functionality and follows best practices in {target_language}.
            """

            response = await self.anthropic.generate(prompt)
            migrated_code = response.strip()

            if not migrated_code:
                raise ValueError("Failed to generate migrated code.")

            return migrated_code

        except Exception as e:
            error_msg = f"Error in migrate_code: {str(e)}"
            print(error_msg)
            if os.getenv('DEBUG') == 'True':
                print(traceback.format_exc())
            raise

    async def analyze_migration_feasibility(self, code: str, source_language: str, target_language: str) -> Dict[str, Any]:
        """
        Analyzes the feasibility of migrating code from the source language to the target language.

        Args:
            code (str): The source code to be analyzed.
            source_language (str): The programming language of the source code.
            target_language (str): The target programming language for migration.

        Returns:
            Dict[str, Any]: A dictionary containing the feasibility analysis results.
        """
        try:
            prompt = f"""
            You are an expert programmer in both {source_language} and {target_language}.
            Please analyze the feasibility of migrating the following {source_language} code to {target_language}:

            {code}

            Provide a detailed analysis including:
            1. Overall feasibility (easy, moderate, difficult, or nearly impossible)
            2. Key challenges in migration
            3. Estimated time for migration
            4. Potential loss of functionality or performance
            5. Recommendations for a successful migration
            """

            response = await self.anthropic.generate(prompt)
            analysis = response.strip()

            if not analysis:
                raise ValueError("Failed to generate migration feasibility analysis.")

            # Parse the analysis into a structured format
            analysis_dict = self._parse_analysis(analysis)

            return analysis_dict

        except Exception as e:
            error_msg = f"Error in analyze_migration_feasibility: {str(e)}"
            print(error_msg)
            if os.getenv('DEBUG') == 'True':
                print(traceback.format_exc())
            raise

    def _parse_analysis(self, analysis: str) -> Dict[str, Any]:
        """
        Parses the AI-generated analysis into a structured dictionary.

        Args:
            analysis (str): The raw analysis text.

        Returns:
            Dict[str, Any]: A structured representation of the analysis.
        """
        lines = analysis.split('\n')
        result = {
            'overall_feasibility': '',
            'key_challenges': [],
            'estimated_time': '',
            'potential_losses': [],
            'recommendations': []
        }

        current_section = ''
        for line in lines:
            line = line.strip()
            if line.startswith('1. Overall feasibility:'):
                result['overall_feasibility'] = line.split(':')[1].strip()
            elif line.startswith('2. Key challenges'):
                current_section = 'key_challenges'
            elif line.startswith('3. Estimated time'):
                result['estimated_time'] = line.split(':')[1].strip()
                current_section = ''
            elif line.startswith('4. Potential loss'):
                current_section = 'potential_losses'
            elif line.startswith('5. Recommendations'):
                current_section = 'recommendations'
            elif line and current_section:
                result[current_section].append(line)

        return result


# Example usage (for testing purposes)
if __name__ == "__main__":
    import asyncio

    async def test_migration_service():
        service = CodeMigrationService()

        # Test code migration
        python_code = """
        def factorial(n):
            if n == 0:
                return 1
            else:
                return n * factorial(n - 1)
        """
        migrated_code = await service.migrate_code(python_code, "Python", "JavaScript")
        print("Migrated code:")
        print(migrated_code)

        # Test migration feasibility analysis
        analysis = await service.analyze_migration_feasibility(python_code, "Python", "C++")
        print("\nMigration feasibility analysis:")
        print(analysis)

    asyncio.run(test_migration_service())
