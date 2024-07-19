import asyncio
import aiofiles.os
import aiofiles
import os
import shutil
import time
from termcolor import colored

# Updated constants
IGNORE_PATTERNS = [".git", ".system"]  # Example patterns to exclude from backup
DEV_FOLDER = "app"
THIS_DIRECTORY = os.getcwd()
PROJECT_SYSTEM_FOLDER = os.path.join(THIS_DIRECTORY, DEV_FOLDER, ".system")
BACKUP_FOLDER = os.path.join(PROJECT_SYSTEM_FOLDER, f"{DEV_FOLDER}_backup")
LOGS_FOLDER = os.path.join(PROJECT_SYSTEM_FOLDER, "logs")

async def update_backup_folder():
    """
    Asynchronously updates backup files from DEV_FOLDER to BACKUP_FOLDER.
    Creates a new backup folder with a timestamp and maintains a limited number of backups.
    
    Returns:
        True if backup was successful, False otherwise.
    """
    print(colored("Updating backup files ...", "yellow"))

    try:
        if os.path.exists(os.path.join(THIS_DIRECTORY, DEV_FOLDER)):
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            await aiofiles.os.makedirs(BACKUP_FOLDER, exist_ok=True)
            new_backup_folder = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}")

            print(colored(f"Moving {DEV_FOLDER} to {new_backup_folder}", "yellow"))

            if await aiofiles.os.path.exists(os.path.join(THIS_DIRECTORY, DEV_FOLDER)):
                await asyncio.to_thread(shutil.copytree, os.path.join(THIS_DIRECTORY, DEV_FOLDER), new_backup_folder, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))

            # Maintain a limited number of backups
            backups = sorted([d for d in os.listdir(BACKUP_FOLDER) if d.startswith("backup_")])
            while len(backups) > 5:  # Keep only the 5 most recent backups
                shutil.rmtree(os.path.join(BACKUP_FOLDER, backups.pop(0)))

            return True
    except Exception as e:
        print(colored(f"Error updating backup files: {e}", "red"))

    await asyncio.sleep(2)  # Simulate delay even in case of error
    return False

# Example usage:
async def main():
    success = await update_backup_folder()
    if success:
        print(colored("Backup files updated successfully.", "green"))
    else:
        print(colored("Failed to update backup files.", "red"))

if __name__ == "__main__":
    asyncio.run(main())
