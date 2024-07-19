
"""
Implements code difference analysis functionality.

This module provides utilities for generating diffs between code versions
and applying patches to code.
"""

import difflib
from typing import List, Tuple


class CodeDiff:
    def __init__(self):
        self.differ = difflib.Differ()

    def generate_diff(self, old_code: str, new_code: str) -> str:
        """
        Generate a diff between two versions of code.

        Args:
            old_code (str): The original version of the code.
            new_code (str): The new version of the code.

        Returns:
            str: A string representation of the diff.
        """
        old_lines = old_code.splitlines()
        new_lines = new_code.splitlines()
        diff = self.differ.compare(old_lines, new_lines)
        return '\n'.join(diff)

    def apply_patch(self, original_code: str, patch: str) -> str:
        """
        Apply a patch to the original code.

        Args:
            original_code (str): The original version of the code.
            patch (str): The patch to apply.

        Returns:
            str: The resulting code after applying the patch.
        """
        original_lines = original_code.splitlines()
        patch_lines = patch.splitlines()
        
        result_lines = []
        original_index = 0

        for line in patch_lines:
            if line.startswith('  '):
                result_lines.append(original_lines[original_index])
                original_index += 1
            elif line.startswith('- '):
                original_index += 1
            elif line.startswith('+ '):
                result_lines.append(line[2:])

        return '\n'.join(result_lines)

    def _parse_unified_diff(self, diff: str) -> List[Tuple[str, List[str]]]:
        """
        Parse a unified diff format.

        Args:
            diff (str): The diff in unified format.

        Returns:
            List[Tuple[str, List[str]]]: A list of tuples containing the change type and affected lines.
        """
        changes = []
        current_change = None
        lines = []

        for line in diff.splitlines():
            if line.startswith('+++') or line.startswith('---'):
                continue
            elif line.startswith('@@'):
                if current_change:
                    changes.append((current_change, lines))
                current_change = None
                lines = []
            elif line.startswith('+'):
                if current_change != 'add':
                    if current_change:
                        changes.append((current_change, lines))
                    current_change = 'add'
                    lines = []
                lines.append(line[1:])
            elif line.startswith('-'):
                if current_change != 'remove':
                    if current_change:
                        changes.append((current_change, lines))
                    current_change = 'remove'
                    lines = []
                lines.append(line[1:])
            else:
                if current_change:
                    changes.append((current_change, lines))
                current_change = None
                lines = []

        if current_change:
            changes.append((current_change, lines))

        return changes

    def apply_unified_patch(self, original_code: str, patch: str) -> str:
        """
        Apply a unified format patch to the original code.

        Args:
            original_code (str): The original version of the code.
            patch (str): The unified format patch to apply.

        Returns:
            str: The resulting code after applying the patch.
        """
        original_lines = original_code.splitlines()
        changes = self._parse_unified_diff(patch)

        result_lines = original_lines.copy()
        offset = 0

        for change_type, lines in changes:
            if change_type == 'add':
                result_lines[offset:offset] = lines
                offset += len(lines)
            elif change_type == 'remove':
                del result_lines[offset:offset + len(lines)]

        return '\n'.join(result_lines)


if __name__ == "__main__":
    # Example usage
    diff_tool = CodeDiff()
    
    old_code = """def hello_world():
    print("Hello, World!")
"""
    new_code = """def hello_world():
    print("Hello, AI Software Factory!")
"""
    
    diff = diff_tool.generate_diff(old_code, new_code)
    print("Generated diff:")
    print(diff)
    
    patched_code = diff_tool.apply_patch(old_code, diff)
    print("\nPatched code:")
    print(patched_code)
    
    assert patched_code == new_code, "Patch application failed"
    print("\nPatch applied successfully!")
