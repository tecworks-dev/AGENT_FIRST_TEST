from flask_restful import Resource, reqparse
from database import db, User, Message

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get_or_404(user_id)
            return {'id': user.id, 'username': user.username, 'email': user.email}
        users = User.query.all()
        return [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        new_user = User(username=args['username'], email=args['email'])
        new_user.set_password(args['password'])
        db.session.add(new_user)
        db.session.commit()

        return {'id': new_user.id, 'username': new_user.username, 'email': new_user.email}, 201

class MessageResource(Resource):
    def get(self, message_id=None):
        if message_id:
            message = Message.query.get_or_404(message_id)
            return {'id': message.id, 'sender_id': message.sender_id, 'recipient_id': message.recipient_id, 'content': message.content}
        messages = Message.query.all()
        return [{'id': m.id, 'sender_id': m.sender_id, 'recipient_id': m.recipient_id, 'content': m.content} for m in messages]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sender_id', type=int, required=True)
        parser.add_argument('recipient_id', type=int, required=True)
        parser.add_argument('content', required=True)
        args = parser.parse_args()

        new_message = Message(sender_id=args['sender_id'], recipient_id=args['recipient_id'], content=args['content'])
        db.session.add(new_message)
        db.session.commit()

        return {'id': new_message.id, 'sender_id': new_message.sender_id, 'recipient_id': new_message.recipient_id, 'content': new_message.content}, 201