#!/usr/bin/env python3
"""
Implementation of the Baic Authentication method
"""
import base64
from .auth import Auth
from typing import TypeVar
from flask import request


class BasicAuth(Auth):
    """
    Basic Authentication using the Auth template
    """

    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """
        Returns the Base64 part of the Authentication header for Basic
        Authentication
        """
        if (authorization_header is None or type(authorization_header) is not
                str or not authorization_header.startswith("Basic ")):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
        Returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if (base64_authorization_header is None or type(
                base64_authorization_header) is not str):
            return None

        decoded = None
        try:
            decoded = base64.b64decode(
                    base64_authorization_header, validate=True)
            try:
                return decoded.decode("utf-8")
            except UnicodeDecodeError as e:
                return decoded
        except base64.binascii.Error as e:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value
        """
        if (decoded_base64_authorization_header is None or type(
            decoded_base64_authorization_header) is not str or ":" not in
                decoded_base64_authorization_header):
            return (None, None)

        credentials = decoded_base64_authorization_header.split(":")

        return (credentials[0], credentials[1])

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """
        Returns the user instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return None

        if user_pwd is None or type(user_pwd) is not str:
            return None

        from models.user import User

        user_obj = User.search({"email": user_email})
        if user_obj is None or len(user_obj) == 0:
            return None
        for user in user_obj:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overloads Auth and retrieves the User instance for a request
        """
        auth_header = None
        extracted_header = None
        decoded_header = None
        user_credentials = None
        user_instance = None

        auth_header = self.authorization_header(request)
        if auth_header is not None:
            extracted_header = self.extract_base64_authorization_header(
                    auth_header)
        if extracted_header is not None:
            decoded_header = self.decode_base64_authorization_header(
                    extracted_header)
        if decoded_header is not None:
            user_credentials = self.extract_user_credentials(decoded_header)
        if user_credentials is not None:
            user_instance = self.user_object_from_credentials(
                    user_credentials[0], user_credentials[1])
        return user_instance
