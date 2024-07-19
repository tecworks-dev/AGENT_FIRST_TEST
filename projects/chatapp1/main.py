import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO
import chat_server
import config
from database import init_db
from user_management import init_user_management, login_required, register_user, authenticate_user, logout

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    socketio = SocketIO(app)

    # Initialize user management
    init_user_management(app)

    # Initialize database
    init_db()

    @app.route('/')
    @login_required
    def index():
        return render_template('index.html', current_user=session.get('user'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if authenticate_user(username, password):
                return redirect(url_for('index'))
            return render_template('login.html', error='Invalid username or password')
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            success, message = register_user(username, password, email)
            if success:
                return redirect(url_for('login'))
            return render_template('register.html', error=message)
        return render_template('register.html')

    @app.route('/logout')
    @login_required
    def logout_route():
        logout()
        return redirect(url_for('login'))

    @app.route('/send_message', methods=['POST'])
    @login_required
    def send_message():
        data = request.json
        chat_server.handle_message(data)
        return jsonify({"status": "success"})

    @app.route('/get_messages')
    @login_required
    def get_messages():
        messages = chat_server.get_recent_messages()
        return jsonify(messages)

    @socketio.on('message')
    def handle_message(message):
        chat_server.handle_message(message)
        socketio.emit('message', message, broadcast=True)

    @app.route('/favicon.ico')
    def favicon():
        return app.send_static_file('favicon.ico')

    return app, socketio

def main():
    app, socketio = create_app()
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, debug=config.DEBUG, host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()