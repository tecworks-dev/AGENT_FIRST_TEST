
"""
Purpose: Utility functions for file operations.
Description: This module provides functions for reading and writing file contents,
             and updating the backup folder. It includes error handling and logging.
"""

import os
import traceback
import shutil
from termcolor import colored
import aiofiles

DEBUG = True

async def get_file_contents(file_path):
    """
    Asynchronously read the contents of a file.

    Args:
        file_path (str): Path to the file to be read.

    Returns:
        str: Contents of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there's an error reading the file.
    """
    try:
        async with aiofiles.open(file_path, 'r') as file:
            contents = await file.read()
        if DEBUG:
            print(colored(f"Successfully read file: {file_path}", "green"))
        return contents
    except FileNotFoundError:
        error_msg = f"File not found: {file_path}"
        print(colored(error_msg, "red"))
        traceback.print_exc()
        raise
    except IOError as e:
        error_msg = f"Error reading file {file_path}: {str(e)}"
        print(colored(error_msg, "red"))
        traceback.print_exc()
        raise

async def save_file_contents(file_path, contents):
    """
    Asynchronously save contents to a file.

    Args:
        file_path (str): Path to the file to be written.
        contents (str): Contents to be written to the file.

    Raises:
        IOError: If there's an error writing to the file.
    """
    try:
        async with aiofiles.open(file_path, 'w') as file:
            await file.write(contents)
        if DEBUG:
            print(colored(f"Successfully saved file: {file_path}", "green"))
    except IOError as e:
        error_msg = f"Error writing to file {file_path}: {str(e)}"
        print(colored(error_msg, "red"))
        traceback.print_exc()
        raise

def update_backup_folder(source_folder, backup_folder):
    """
    Update the backup folder with the contents of the source folder.

    Args:
        source_folder (str): Path to the source folder.
        backup_folder (str): Path to the backup folder.

    Raises:
        OSError: If there's an error during the backup process.
    """
    try:
        if os.path.exists(backup_folder):
            shutil.rmtree(backup_folder)
        shutil.copytree(source_folder, backup_folder)
        if DEBUG:
            print(colored(f"Successfully updated backup folder: {backup_folder}", "green"))
    except OSError as e:
        error_msg = f"Error updating backup folder: {str(e)}"
        print(colored(error_msg, "red"))
        traceback.print_exc()
        raise

import unittest

class TestFileUtils(unittest.TestCase):
    async def test_get_file_contents(self):
        # Test reading an existing file
        test_file = "test_file.txt"
        test_content = "This is a test file."
        await save_file_contents(test_file, test_content)
        content = await get_file_contents(test_file)
        self.assertEqual(content, test_content)

        # Test reading a non-existent file
        with self.assertRaises(FileNotFoundError):
            await get_file_contents("non_existent_file.txt")

    async def test_save_file_contents(self):
        # Test writing to a file
        test_file = "test_save.txt"
        test_content = "This is a test save."
        await save_file_contents(test_file, test_content)
        content = await get_file_contents(test_file)
        self.assertEqual(content, test_content)

    def test_update_backup_folder(self):
        # Test updating backup folder
        source_folder = "test_source"
        backup_folder = "test_backup"
        os.makedirs(source_folder, exist_ok=True)
        with open(os.path.join(source_folder, "test.txt"), "w") as f:
            f.write("Test file")
        
        update_backup_folder(source_folder, backup_folder)
        self.assertTrue(os.path.exists(backup_folder))
        self.assertTrue(os.path.exists(os.path.join(backup_folder, "test.txt")))

        # Clean up
        shutil.rmtree(source_folder)
        shutil.rmtree(backup_folder)

if __name__ == "__main__":
    unittest.main()
