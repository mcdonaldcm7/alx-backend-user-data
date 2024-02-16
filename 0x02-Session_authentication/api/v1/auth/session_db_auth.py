#!/usr/bin/env python3
"""
Module for Sessions in database, retrieves user and session info from a
database
"""
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
    Child of SessionExpAuth class that uses a database to store info
    """

    def __init__(self):
        super().__init__()

    def create_session(self, user_id=None):
        """ Creates and Stores a new instance of UserSession and Returns the
        Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        from models.user_session import UserSession

        user_session = UserSession(user_id=user_id, session_id=session_id)

        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns the User ID
        """
        if session_id is None:
            return None

        from models.base import DATA
        from models.user_session import UserSession

        user_id = None
        created_at = None
        if "UserSession" not in DATA:
            return None
        session_db_objs = DATA["UserSession"]
        for k, v in session_db_objs.items():
            if v.session_id == session_id:
                user_id = v.user_id
                created_at = v.created_at

        from datetime import datetime, timedelta

        if self.session_duration <= 0:
            return user_id
        if created_at is None:
            return None
        if ((created_at + timedelta(seconds=self.session_duration)) <
                datetime.utcnow()):
            return None
        return user_id

    def destroy_session(self, request=None):
        """ Destroys the UserSession based on the Session ID from the request
        cookie
        """
        session_id = None
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        from models.base import DATA

        session_db_objs = DATA["UserSession"]
        for k, v in session_db_objs.items():
            if v.session_id == session_id:
                v.remove()
                return True
        return False
