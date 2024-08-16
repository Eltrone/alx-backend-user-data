#!/usr/bin/env python3
"""
Auth module for handling authentication related operations.
"""

import bcrypt
import uuid
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hash a password for storing."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with an email and password."""
        if self._db.find_user_by(email=email):
            raise ValueError(f"User {email} already exists")
        hashed_password = self._hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials."""
        user = self._db.find_user_by(email=email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            return True
        return False

    def _generate_uuid(self) -> str:
        """Generate a new UUID."""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Create a user session for a valid email."""
        user = self._db.find_user_by(email=email)
        if user:
            session_id = self._generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        return None
