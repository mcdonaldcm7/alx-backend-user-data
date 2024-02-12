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
        """Unimplemented method for template
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Unimplemented method for template
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Unimplemented method for template
        """
        return None
