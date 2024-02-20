#!/usr/bin/env python3
"""
Basic Flask app Module
"""
from flask import (Flask, jsonify, request, abort, make_response, redirect,
                   url_for)
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=["GET"])
def index():
    """
    Simple index route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    Creates a user if user doesn't exists
    """
    email = request.form["email"]
    password = request.form["password"]

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"})


@app.route("/sessions", methods=["POST"])
def login():
    """
    Validates user's login credentials and logs the user in
    """
    email = request.form["email"]
    password = request.form["password"]

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    Logs a user out and deletes their session_id
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('index'))


@app.route("/profile", methods=["GET"])
def profile():
    """
    Find and return user profile details
    For now: {"email": "<user email>"}
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """
    Sends a generated reset password token to the email in the request,
    Otherwise respond with a 403 status code if the email is not registered
    """
    email = request.form["email"]
    try:
        reset_token = AUTH.get_reset_password_token(email)

        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """
    Handles the request to update the user's password
    """
    email = request.form["email"]
    reset_token = request.form["reset_token"]
    new_password = request.form["new_password"]

    if AUTH.update_password(reset_token, new_password) is None:
        return jsonify({"email": email, "message": "Password updated"}), 200
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
