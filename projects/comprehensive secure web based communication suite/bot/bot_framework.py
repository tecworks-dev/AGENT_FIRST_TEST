
# bot/bot_framework.py
"""
Implements a bot framework for automated interactions.

This module provides a BotManager class that allows registration and management of bots
for automated interactions within the secure communication suite. It handles bot
registration and command processing, integrating with the messaging system.
"""

import traceback
from typing import List, Dict
from communication.messaging import MessagingManager

DEBUG = True

class BotManager:
    def __init__(self):
        self.bots: Dict[str, Dict] = {}
        self.messaging_manager = MessagingManager()

    def register_bot(self, name: str, commands: List[str]) -> str:
        """
        Register a new bot with the given name and supported commands.

        Args:
            name (str): The name of the bot.
            commands (List[str]): List of commands supported by the bot.

        Returns:
            str: The unique ID assigned to the registered bot.
        """
        try:
            bot_id = f"bot_{len(self.bots) + 1}"
            self.bots[bot_id] = {
                "name": name,
                "commands": commands
            }
            if DEBUG:
                print(f"Bot registered: {bot_id} - {name}")
            return bot_id
        except Exception as e:
            error_msg = f"Error registering bot: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return ""

    def process_command(self, bot_id: str, command: str, args: List[str]) -> str:
        """
        Process a command for a specific bot.

        Args:
            bot_id (str): The ID of the bot to process the command.
            command (str): The command to be processed.
            args (List[str]): Arguments for the command.

        Returns:
            str: The result of the command processing.
        """
        try:
            if bot_id not in self.bots:
                return "Error: Bot not found"

            bot = self.bots[bot_id]
            if command not in bot["commands"]:
                return f"Error: Command '{command}' not supported by {bot['name']}"

            # Here, you would implement the actual command processing logic
            # For this example, we'll just return a simple message
            result = f"Bot {bot['name']} processed command: {command} with args: {args}"

            # Use the messaging manager to send the result
            # Assuming a system user for the bot
            self.messaging_manager.send_message(f"system_{bot_id}", "user", result)

            if DEBUG:
                print(f"Command processed: {bot_id} - {command} {args}")

            return result
        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return error_msg

    def list_bots(self) -> List[Dict]:
        """
        List all registered bots and their supported commands.

        Returns:
            List[Dict]: A list of dictionaries containing bot information.
        """
        return [{"id": bot_id, "name": bot["name"], "commands": bot["commands"]} 
                for bot_id, bot in self.bots.items()]

    def remove_bot(self, bot_id: str) -> bool:
        """
        Remove a registered bot.

        Args:
            bot_id (str): The ID of the bot to be removed.

        Returns:
            bool: True if the bot was successfully removed, False otherwise.
        """
        try:
            if bot_id in self.bots:
                del self.bots[bot_id]
                if DEBUG:
                    print(f"Bot removed: {bot_id}")
                return True
            return False
        except Exception as e:
            error_msg = f"Error removing bot: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return False

if __name__ == "__main__":
    # Simple test for the BotManager
    bot_manager = BotManager()
    test_bot_id = bot_manager.register_bot("TestBot", ["hello", "echo"])
    print(bot_manager.process_command(test_bot_id, "hello", []))
    print(bot_manager.process_command(test_bot_id, "echo", ["Hello, World!"]))
    print(bot_manager.list_bots())
    print(bot_manager.remove_bot(test_bot_id))
