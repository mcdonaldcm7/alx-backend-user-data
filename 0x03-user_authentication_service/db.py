#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import (InvalidRequestError, IntegrityError)

from user import Base, User
from typing import Any, Dict, Union


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        # If you want less output generated set echo to False
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Save the user to the database
        Return a new User object from the parameters passed
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        try:
            self._session.commit()
        except IntegrityError:
            self._session.rollback()
            raise ValueError("User already exists with this email")
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Returns the first row found in the users table as filtered by the
        **kwargs argument
        """
        try:
            valid_query_args = {"id", "email", "hashed_password", "session_id",
                                "reset_token"}
            invalid_args = set(kwargs.keys()) - valid_query_args
            if invalid_args:
                raise InvalidRequestError()
            query = self._session.query(User)
            result = query.filter_by(**kwargs).first()
            if result is None:
                raise NoResultFound()
            return result
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Locates the user with ID user_id and updates the user's attributes as
        passed in the method's argument then commit changes to the database
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError()
            self._session.commit()
            return user
        except NoResultFound:
            raise NoResultFound()
        except MultipleResultsFound:
            raise MultipleResultsFound()
        except InvalidRequestError:
            raise InvalidRequestError()
