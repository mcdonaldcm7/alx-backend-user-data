#!/usr/bin/env python3
"""
Module for Session Authentication with expiration
"""
import os
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session Expiration Authentication
    """

    def __init__(self):
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", None))
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a Session ID for a user ID and stored the user_id and
        created_at
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
                }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None

        session_dictionary = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_dictionary["user_id"]
        if "created_at" not in session_dictionary:
            return None
        if ((session_dictionary["created_at"] + timedelta(
                seconds=self.session_duration)) < datetime.now()):
            return None
        return session_dictionary["user_id"]
