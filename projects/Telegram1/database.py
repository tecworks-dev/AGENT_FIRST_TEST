import traceback
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import DATABASE_URI, DEBUG

Base = declarative_base()

# Define database models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship('Message', back_populates='user')

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    content = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='messages')

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

def get_db_connection():
    """
    Get a database connection.
    
    Returns:
    A SQLAlchemy Session object.
    """
    return Session()

def init_db():
    """
    Initialize the database by creating all tables.
    """
    try:
        Base.metadata.create_all(engine)
        if DEBUG:
            print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        if DEBUG:
            traceback.print_exc()

def get_user(user_id=None, username=None, email=None):
    """
    Retrieve a user by their ID, username, or email.

    Args:
    user_id (int): The ID of the user to retrieve.
    username (str): The username of the user to retrieve.
    email (str): The email of the user to retrieve.

    Returns:
    A dictionary containing user information or None if not found.
    """
    session = get_db_connection()
    try:
        if user_id:
            user = session.query(User).filter_by(id=user_id).first()
        elif username:
            user = session.query(User).filter_by(username=username).first()
        elif email:
            user = session.query(User).filter_by(email=email).first()
        else:
            return None

        if user:
            return {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at
            }
        return None
    except Exception as e:
        print(f"Error retrieving user: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        return None
    finally:
        session.close()

def update_user(user_id, data):
    """
    Update user information.

    Args:
    user_id (int): The ID of the user to update.
    data (dict): A dictionary containing the fields to update.

    Returns:
    True if the update was successful, False otherwise.
    """
    session = get_db_connection()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            session.commit()
            if DEBUG:
                print(f"User {user_id} updated successfully.")
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Error updating user: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    init_db()