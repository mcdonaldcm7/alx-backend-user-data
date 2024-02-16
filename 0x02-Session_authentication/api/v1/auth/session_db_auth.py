#!/usr/bin/env python3
"""
"""
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
    """

    def create_session(self, user_id=None):
        """ Creates and Stores a new instance of UserSession and Returns the
        Session ID
        """
        # session_id = super().create_session(user_id)
        if user_id is None:
            return None
        import uuid

        session_id = str(uuid.uuid4())
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

        session_db_objs = DATA["UserSession"]
        for k, v in session_db_objs.items():
            if v.session_id == session_id:
                return k

        return None

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
        # if self.user_id_for_session_id(session_id) is None:
        #    return False
        # del self.user_id_by_session_id[session_id]

        from models.base import DATA

        session_db_objs = DATA["UserSession"]
        for k, v in session_db_objs.items():
            if v.session_id == session_id:
                v.remove()
                return True
        return False
