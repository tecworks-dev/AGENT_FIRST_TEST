# app/models/media.py
# Defines the Media model for storing information about uploaded media files

from app.extensions import db
from datetime import datetime
import traceback

class Media(db.Model):
    """
    Media model for storing information about uploaded media files.

    Attributes:
    - id: Unique identifier for the media file
    - user_id: ID of the user who uploaded the file
    - filename: Name of the uploaded file
    - file_type: Type of the uploaded file (e.g., 'image', 'video', 'audio')
    - timestamp: Date and time when the file was uploaded
    """

    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Changed 'user.id' to 'users.id'
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, filename, file_type):
        self.user_id = user_id
        self.filename = filename
        self.file_type = file_type

    def __repr__(self):
        return f'<Media {self.id}: {self.filename}>'

    def to_dict(self):
        """
        Convert the Media object to a dictionary for easy serialization.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'file_type': self.file_type,
            'timestamp': self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Media object from a dictionary.
        """
        try:
            return Media(
                user_id=data['user_id'],
                filename=data['filename'],
                file_type=data['file_type']
            )
        except KeyError as e:
            print(f"Error creating Media object from dictionary: {str(e)}")
            traceback.print_exc()
            return None

# Debugging statements
if __name__ == '__main__':
    print("Debugging Media model...")
    test_media = Media(user_id=1, filename='test.jpg', file_type='image')
    print(f"Test Media object: {test_media}")
    print(f"Test Media dict: {test_media.to_dict()}")
    test_dict = {'user_id': 2, 'filename': 'test2.mp4', 'file_type': 'video'}
    test_media2 = Media.from_dict(test_dict)
    print(f"Test Media object from dict: {test_media2}")