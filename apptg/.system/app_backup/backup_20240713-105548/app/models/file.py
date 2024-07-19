
# File: /project_root/app/models/file.py
# Purpose: Define the File model for managing shared files in the application.
# Description: This module contains the File model class, which represents
#              shared files in the database and provides methods for file management.

from app import db
from datetime import datetime
import traceback
import logging
from app.models.user import User  # Import User model to ensure it's initialized first

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class File(db.Model):
    """File model for managing shared files"""
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Changed 'user.id' to 'users.id'
    is_deleted = db.Column(db.Boolean, default=False)

    def __init__(self, filename, file_path, file_size, mime_type, uploader_id):
        self.filename = filename
        self.file_path = file_path
        self.file_size = file_size
        self.mime_type = mime_type
        self.uploader_id = uploader_id

    def __repr__(self):
        return f"<File {self.filename}>"

    @classmethod
    def create_file(cls, filename, file_path, file_size, mime_type, uploader_id):
        """
        Create a new file record in the database.
        """
        try:
            new_file = cls(filename=filename, file_path=file_path, file_size=file_size,
                           mime_type=mime_type, uploader_id=uploader_id)
            db.session.add(new_file)
            db.session.commit()
            logger.info(f"File created: {filename}")
            return new_file
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating file: {str(e)}")
            logger.debug(traceback.format_exc())
            return None

    @classmethod
    def get_file_by_id(cls, file_id):
        """
        Retrieve a file by its ID.
        """
        try:
            return cls.query.get(file_id)
        except Exception as e:
            logger.error(f"Error retrieving file with ID {file_id}: {str(e)}")
            logger.debug(traceback.format_exc())
            return None

    @classmethod
    def get_files_by_uploader(cls, uploader_id):
        """
        Retrieve all files uploaded by a specific user.
        """
        try:
            return cls.query.filter_by(uploader_id=uploader_id, is_deleted=False).all()
        except Exception as e:
            logger.error(f"Error retrieving files for uploader {uploader_id}: {str(e)}")
            logger.debug(traceback.format_exc())
            return []

    def soft_delete(self):
        """
        Soft delete the file by marking it as deleted.
        """
        try:
            self.is_deleted = True
            db.session.commit()
            logger.info(f"File soft deleted: {self.filename}")
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error soft deleting file {self.filename}: {str(e)}")
            logger.debug(traceback.format_exc())
            return False

    def update_file_info(self, filename=None, file_size=None, mime_type=None):
        """
        Update file information.
        """
        try:
            if filename:
                self.filename = filename
            if file_size:
                self.file_size = file_size
            if mime_type:
                self.mime_type = mime_type
            db.session.commit()
            logger.info(f"File info updated: {self.filename}")
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating file info for {self.filename}: {str(e)}")
            logger.debug(traceback.format_exc())
            return False


# Debugging statements
if __name__ == "__main__":
    if db.engine.url.drivername == 'sqlite':
        import sqlite3
        sqlite3.connect(db.engine.url.database)
    
    logger.debug("File model initialized")
    logger.debug(f"Table name: {File.__tablename__}")
    logger.debug(f"Columns: {', '.join(column.name for column in File.__table__.columns)}")


import unittest
from app import create_app, db

class TestFileModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_file(self):
        file = File.create_file("test.txt", "/path/to/test.txt", 1024, "text/plain", 1)
        self.assertIsNotNone(file)
        self.assertEqual(file.filename, "test.txt")

    def test_get_file_by_id(self):
        file = File.create_file("test.txt", "/path/to/test.txt", 1024, "text/plain", 1)
        retrieved_file = File.get_file_by_id(file.id)
        self.assertIsNotNone(retrieved_file)
        self.assertEqual(retrieved_file.filename, "test.txt")

    def test_get_files_by_uploader(self):
        File.create_file("test1.txt", "/path/to/test1.txt", 1024, "text/plain", 1)
        File.create_file("test2.txt", "/path/to/test2.txt", 2048, "text/plain", 1)
        files = File.get_files_by_uploader(1)
        self.assertEqual(len(files), 2)

    def test_soft_delete(self):
        file = File.create_file("test.txt", "/path/to/test.txt", 1024, "text/plain", 1)
        self.assertTrue(file.soft_delete())
        self.assertTrue(file.is_deleted)

    def test_update_file_info(self):
        file = File.create_file("test.txt", "/path/to/test.txt", 1024, "text/plain", 1)
        self.assertTrue(file.update_file_info(filename="updated.txt", file_size=2048))
        self.assertEqual(file.filename, "updated.txt")
        self.assertEqual(file.file_size, 2048)

if __name__ == '__main__':
    unittest.main()
