
# ui/web_ui.py
"""
This module implements the web-based interface with responsive design for the secure communication suite.
It provides a WebUI class that handles the web server and page rendering functionality.
"""

import flask
import traceback
from flask import Flask, render_template, request, jsonify
from config import Config

DEBUG = True

app = Flask(__name__)

class WebUI:
    def __init__(self):
        self.config = Config()

    def start_web_server(self):
        """
        Starts the Flask web server for the application.
        """
        try:
            port = self.config.get_setting('web_port')
            if DEBUG:
                print(f"Starting web server on port {port}")
            app.run(host='0.0.0.0', port=port, debug=DEBUG)
        except Exception as e:
            print(f"Error starting web server: {str(e)}")
            if DEBUG:
                traceback.print_exc()

    def render_page(self, page: str) -> str:
        """
        Renders the specified page using Flask's template engine.

        Args:
            page (str): The name of the page to render.

        Returns:
            str: The rendered HTML content of the page.
        """
        try:
            if DEBUG:
                print(f"Rendering page: {page}")
            return render_template(f"{page}.html")
        except Exception as e:
            print(f"Error rendering page {page}: {str(e)}")
            if DEBUG:
                traceback.print_exc()
            return "Error: Page not found", 404

@app.route('/')
def home():
    return WebUI().render_page('home')

@app.route('/login')
def login():
    return WebUI().render_page('login')

@app.route('/register')
def register():
    return WebUI().render_page('register')

@app.route('/chat')
def chat():
    return WebUI().render_page('chat')

@app.route('/files')
def files():
    return WebUI().render_page('files')

@app.route('/calls')
def calls():
    return WebUI().render_page('calls')

@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    # Here you would typically process the API request and return a response
    return jsonify({"status": "success", "message": "API request received"})

if __name__ == '__main__':
    web_ui = WebUI()
    web_ui.start_web_server()
