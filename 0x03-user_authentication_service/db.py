#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError, MultipleResultsFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        # If you want more output generated set echo to True
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

    def add_user(self, email, hashed_password):
        """Save the user to the database
        Return a new User object from the parameters passed
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        try:
            self._session.commit()
        except IntegrityError:
            self._session.rollback()
            raise ValueError("User already exists with this email!")
        return new_user

    def find_user_by(self, **kwargs):
        """
        Returns the first row found in the users table as filtered by the
        **kwargs argument
        """
        try:
            query = self._session.query(User)
            result = query.filter_by(**kwargs).first()
            return result
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError

    def update_user(self, user_id, **kwargs):
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