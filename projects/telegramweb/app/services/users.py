from app.models.user import User

class UserService:
    @staticmethod
    def get_all_users():
        users = User.query.all()
        return [{'id': user.id, 'username': user.username} for user in users]