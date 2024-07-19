from app.models.user import User
from app.utils.encryption import hash_password, verify_password
from app.extensions import db
from flask import current_app
import traceback

class AuthService:
    @staticmethod
    def register(username: str, password: str) -> dict:
        try:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return {"status": "error", "message": "Username already exists"}

            hashed_password = hash_password(password)
            new_user = User.create_user(username=username, password_hash=hashed_password)

            if new_user:
                return {"status": "success", "user_id": new_user.id, "username": username}
            else:
                return {"status": "error", "message": "Failed to create user"}
        except Exception as e:
            current_app.logger.error(f"Error in user registration: {str(e)}")
            traceback.print_exc()
            return {"status": "error", "message": f"Registration failed: {str(e)}"}

    @staticmethod
    def login(username: str, password: str) -> dict:
        try:
            user = User.query.filter_by(username=username).first()
            if user and verify_password(user.password_hash, password):
                return {"success": True, "user": user}
            else:
                return {"success": False, "message": "Invalid username or password"}
        except Exception as e:
            current_app.logger.error(f"Error in user login: {str(e)}")
            traceback.print_exc()
            return {"success": False, "message": f"Login failed: {str(e)}"}

    @staticmethod
    def logout(user_id: int) -> bool:
        try:
            # In a real application, you might want to invalidate the user's session
            # or perform other logout-related tasks here.
            return True
        except Exception as e:
            current_app.logger.error(f"Error in user logout: {str(e)}")
            traceback.print_exc()
            return False
