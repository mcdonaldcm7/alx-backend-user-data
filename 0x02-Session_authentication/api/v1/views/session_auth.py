#!/usr/bin/env python3
"""
Route handler for the Session Authentication
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from api.v1.auth.session_auth import SessionAuth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    from models.user import User

    users = User.search({"email": email})
    if users is None or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user_inst = None
    for user in users:
        if user.is_valid_password(password):
            user_inst = user
    if user_inst is None:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    import os

    session_id = auth.create_session(user.id)
    ret = jsonify(user.to_json())
    cookie_name = os.getenv("SESSION_NAME", None)
    ret.set_cookie(cookie_name, session_id)

    return ret
