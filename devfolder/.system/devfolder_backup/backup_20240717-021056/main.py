
# main.py
# Purpose: Entry point for the AI Software Factory application
# Description: This file creates and runs the Flask application

from app import create_app, socketio
from app.models import db

app = create_app()

def main():
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)

# IMPORTANT: do not remove main function as automated test will fail
# IMPORTANT: do not remove this comment
if __name__ == "__main__":
    main()
