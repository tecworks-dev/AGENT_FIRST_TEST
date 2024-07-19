
"""
Desktop user interface implementation.

This file contains the DesktopUI class which manages the desktop user interface
for the secure messaging platform. It provides methods for displaying login and
main screens, as well as showing messages to the user.
"""

import tkinter as tk
from tkinter import messagebox
import traceback
from app.core import messaging, file_sharing, calls
from app.utils import config, logger

DEBUG = True

class DesktopUI:
    """Manages the desktop user interface."""

    def __init__(self):
        """Initialize the DesktopUI."""
        self.root = tk.Tk()
        self.root.title("Secure Messaging Platform")
        self.root.geometry("800x600")
        self.current_user = None
        self.logger = logger.setup_logger()

        if DEBUG:
            self.logger.info("DesktopUI initialized")

    def show_login_screen(self):
        """Display the login screen."""
        try:
            # Clear any existing widgets
            for widget in self.root.winfo_children():
                widget.destroy()

            # Create login form
            tk.Label(self.root, text="Username:").pack()
            username_entry = tk.Entry(self.root)
            username_entry.pack()

            tk.Label(self.root, text="Password:").pack()
            password_entry = tk.Entry(self.root, show="*")
            password_entry.pack()

            login_button = tk.Button(self.root, text="Login", command=lambda: self._handle_login(username_entry.get(), password_entry.get()))
            login_button.pack()

            if DEBUG:
                self.logger.info("Login screen displayed")

        except Exception as e:
            self.logger.error(f"Error in show_login_screen: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.display_message("An error occurred while showing the login screen.")

    def show_main_screen(self):
        """Display the main screen after successful login."""
        try:
            # Clear any existing widgets
            for widget in self.root.winfo_children():
                widget.destroy()

            # Create main screen widgets
            tk.Label(self.root, text=f"Welcome, {self.current_user}!").pack()

            message_button = tk.Button(self.root, text="Send Message", command=self._show_message_screen)
            message_button.pack()

            file_button = tk.Button(self.root, text="Share File", command=self._show_file_sharing_screen)
            file_button.pack()

            call_button = tk.Button(self.root, text="Make Call", command=self._show_call_screen)
            call_button.pack()

            logout_button = tk.Button(self.root, text="Logout", command=self.show_login_screen)
            logout_button.pack()

            if DEBUG:
                self.logger.info(f"Main screen displayed for user: {self.current_user}")

        except Exception as e:
            self.logger.error(f"Error in show_main_screen: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.display_message("An error occurred while showing the main screen.")

    def display_message(self, message: str):
        """Display a message to the user."""
        messagebox.showinfo("Message", message)

        if DEBUG:
            self.logger.info(f"Message displayed: {message}")

    def _handle_login(self, username: str, password: str):
        """Handle the login process."""
        # This is a placeholder for actual authentication logic
        if username and password:
            self.current_user = username
            self.show_main_screen()
        else:
            self.display_message("Invalid username or password")

    def _show_message_screen(self):
        """Show the message sending screen."""
        # Placeholder for message sending functionality
        self.display_message("Message sending functionality not implemented yet.")

    def _show_file_sharing_screen(self):
        """Show the file sharing screen."""
        # Placeholder for file sharing functionality
        self.display_message("File sharing functionality not implemented yet.")

    def _show_call_screen(self):
        """Show the call screen."""
        # Placeholder for call functionality
        self.display_message("Call functionality not implemented yet.")

    def run(self):
        """Run the desktop UI."""
        self.show_login_screen()
        self.root.mainloop()

if __name__ == "__main__":
    ui = DesktopUI()
    ui.run()
