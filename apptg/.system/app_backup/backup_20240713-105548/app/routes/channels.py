
# Purpose: Routes for broadcast channels
# Description: This file contains Flask routes for managing broadcast channels,
# including creating channels, posting messages to channels, and subscribing users to channels.

import traceback
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Channel, Message, User
from app import db
from app.services.encryption import encrypt_message
from app.utils.helpers import generate_unique_id
from app.services.push_notifications import send_notification

channels = Blueprint('channels', __name__)

DEBUG = True

@channels.route('/create', methods=['POST'])
@login_required
def create_channel():
    """
    Creates a new channel.
    """
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description')

        if not name:
            return jsonify({'error': 'Channel name is required'}), 400

        new_channel = Channel(
            id=generate_unique_id(),
            name=name,
            description=description,
            owner_id=current_user.id
        )

        db.session.add(new_channel)
        db.session.commit()

        if DEBUG:
            print(f"Channel created: {new_channel.name}")

        return jsonify({'message': 'Channel created successfully', 'channel_id': new_channel.id}), 201
    except Exception as e:
        if DEBUG:
            print(f"Error creating channel: {str(e)}")
            traceback.print_exc()
        return jsonify({'error': 'An error occurred while creating the channel'}), 500

@channels.route('/<channel_id>/post', methods=['POST'])
@login_required
def post_to_channel(channel_id):
    """
    Posts a message to a channel.
    """
    try:
        channel = Channel.query.get(channel_id)
        if not channel:
            return jsonify({'error': 'Channel not found'}), 404

        if current_user.id != channel.owner_id:
            return jsonify({'error': 'Only channel owner can post messages'}), 403

        data = request.json
        content = data.get('content')

        if not content:
            return jsonify({'error': 'Message content is required'}), 400

        encrypted_content = encrypt_message(content, channel.encryption_key)

        new_message = Message(
            id=generate_unique_id(),
            sender_id=current_user.id,
            channel_id=channel.id,
            content=encrypted_content
        )

        db.session.add(new_message)
        db.session.commit()

        # Send push notifications to subscribers
        for subscriber in channel.subscribers:
            send_notification(subscriber.device_token, f"New message in {channel.name}", "You have a new channel message")

        if DEBUG:
            print(f"Message posted to channel {channel.name}")

        return jsonify({'message': 'Message posted successfully'}), 201
    except Exception as e:
        if DEBUG:
            print(f"Error posting to channel: {str(e)}")
            traceback.print_exc()
        return jsonify({'error': 'An error occurred while posting the message'}), 500

@channels.route('/<channel_id>/subscribe', methods=['POST'])
@login_required
def subscribe_to_channel(channel_id):
    """
    Subscribes a user to a channel.
    """
    try:
        channel = Channel.query.get(channel_id)
        if not channel:
            return jsonify({'error': 'Channel not found'}), 404

        if current_user in channel.subscribers:
            return jsonify({'message': 'You are already subscribed to this channel'}), 200

        channel.subscribers.append(current_user)
        db.session.commit()

        if DEBUG:
            print(f"User {current_user.username} subscribed to channel {channel.name}")

        return jsonify({'message': 'Subscribed to channel successfully'}), 200
    except Exception as e:
        if DEBUG:
            print(f"Error subscribing to channel: {str(e)}")
            traceback.print_exc()
        return jsonify({'error': 'An error occurred while subscribing to the channel'}), 500

# For testing purposes
if __name__ == '__main__':
    import unittest

    class TestChannelRoutes(unittest.TestCase):
        def setUp(self):
            # Set up test client and test database
            pass

        def test_create_channel(self):
            # Test channel creation
            pass

        def test_post_to_channel(self):
            # Test posting a message to a channel
            pass

        def test_subscribe_to_channel(self):
            # Test subscribing to a channel
            pass

    unittest.main()
