#!/usr/bin/env python3
"""
module db
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from user import Base, User  # Assurez-vous d'importer User
from sqlalchemy.exc import InvalidRequestError, NoResultFound


class DB:
    """DB class."""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database and return the user object."""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments."""
        try:
            result = self._session.query(User).filter_by(**kwargs).first()
            if result is None:
                raise NoResultFound("No user found with the given attributes.")
            return result
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query attributes.")

    def update_user(self, user_id: int, **kwargs):
        """Update user's attributes as specified by keyword arguments."""
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            # Transformer l'exception pour une cohérence d'interface.
            raise ValueError("User not found.")

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(
                    f"{key} is not a valid attribute of the user.")

        self._session.commit()
