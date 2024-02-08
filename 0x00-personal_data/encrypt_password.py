#!/usr/bin/env python3
"""
Task

5. Encrypting passwords

User passwords should NEVER be stored in plain text in a database.

Implement a hash_password function that expects one string argument name
password and returns a salted, hashed password, which is a byte string.

Use the bcrypt package to perform the hashing (with hashpw).
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Uses the bcrypt module to return a hashed version of password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Uses bcrypt to validate that the provided password matches the hashed
    password
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
