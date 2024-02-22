#!/usr/bin/env python3
"""
End-to-end Integration test
"""
import requests


url = "http://127.0.0.1:5000/"


def register_user(email: str, password: str) -> None:
    """
    Test for the /users route which creates a new user from the given
    parameters if the user doesn't exist or abort if the user does exist
    """
    response = requests.post((url + "users"), data={
        "email": email, "password": password})
    response_2 = requests.post((url + "users"), data={"email": email,
                                                      "password": password})
    assert response.json() == {"email": email, "message": "user created"}
    assert response.status_code == 200
    assert response_2.json() == {"message": "email already registered"}
    assert response_2.status_code == 400


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Response test for wrong password login attempts
    """
    response = requests.post((url + 'sessions'), data={"email": email,
                                                       "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Response test for valid user credential information passed
    """
    response = requests.post(url + 'sessions', data={"email": email,
                                                     "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}

    session_id = response.cookies.get("session_id")

    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """
    Response test for user login attempt without session ID
    """
    response = requests.get(url + "profile")

    assert response.status_code == 403
    assert response.reason == "FORBIDDEN"


def profile_logged(session_id: str) -> None:
    """
    Response test for user login attempt with session ID
    """
    response = requests.get((url + "profile"), cookies={"session_id":
                                                        session_id})

    assert response.status_code == 200
    assert "email" in response.json()
    assert response.reason == "OK"


def log_out(session_id: str) -> None:
    """
    Response test for user logout with session ID
    """
    response = requests.delete(url + "sessions", cookies={"session_id":
                                                          session_id})
    assert response.status_code == 200
    assert response.url == url
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    Response test for password reset token request
    """
    response = requests.post(url + "reset_password", data={"email": email})

    assert response.status_code == 200

    response_json = response.json()

    assert "reset_token" in response_json
    assert "email" in response_json
    assert response.reason == "OK"
    return response_json.get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Response test for user update password request
    """
    response = requests.put(url + "reset_password", data={
        "email": email, "reset_token": reset_token,
        "new_password": new_password})

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}
    assert response.reason == "OK"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
