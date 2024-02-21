#!/usr/bin/env python3
"""Authentication Module
"""
import bcrypt
import uuid
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of the input password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def _generate_uuid() -> str:
    """
    Generates and returns a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user if the user doesn't already exist
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None

        if user is None:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a user's login credentials
        """
        try:
            user = self._db.find_user_by(email=email)

            if user is None:
                return False
            return bcrypt.checkpw(password.encode("utf-8"),
                                  user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """
        Returns the session ID of the email passed
        """
        user = self._db.find_user_by(email=email)

        if user is None:
            return

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Returns a User with session ID corresponding to the parameter passed
        """
        if session_id is None:
            return None
        user = self._db.find_user_by(session_id=session_id)

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Updates a user's session ID to None
        """
        if self._db.find_user_by(id=user_id) is not None:
            self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token and updates the user's reset_token
        Return reset password token generated
        """
        user = self._db.find_user_by(email=email)
        if user is not None:
            reset_token = str(uuid.uuid4())
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a users password
        """
        user = self._db.find_user_by(reset_token=reset_token)
        if user is not None:
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password,
                                 reset_token=None)
            return None
        raise ValueError()
