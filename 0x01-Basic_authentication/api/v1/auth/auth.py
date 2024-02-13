#!/usr/bin/env python3
"""
Creating the template for the Auth class, the template for all authentication
system that will be implemented
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Template for subsequent authentication system
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks whether or not @path is in @excluded_paths and thus requires
        authentication
        """
        if path is not None and path[len(path) - 1] != '/':
            path += '/'
        if (path is None or excluded_paths is None or
                len(excluded_paths) == 0):
            return True
        for excluded_path in excluded_paths:
            if excluded_path[len(excluded_path) - 1] == '*':
                excluded = excluded_path[:-1]
                if path.startswith(excluded):
                    return False
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Unimplemented method for template
        """
        if 'Authorization' in request.headers:
            return request.headers.get("Authorization")
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Unimplemented method for template
        """
        return None
