import os
from functools import wraps

from flask import Blueprint, redirect, request, session, url_for

from utils.response_helpers import error_response, success_response


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def is_admin_logged_in():
    return session.get("is_admin") is True


def admin_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if not is_admin_logged_in():
            return error_response("Admin login required.", 401)

        return view_function(*args, **kwargs)

    return wrapped_view


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        return error_response("Admin credentials are not configured.", 500)

    if username != admin_username or password != admin_password:
        return error_response("Invalid username or password.", 401)

    session.clear()
    session["is_admin"] = True
    session["admin_username"] = admin_username

    return success_response(
        "Logged in successfully.",
        {"username": admin_username, "isAuthenticated": True},
    )


@auth_bp.post("/logout")
def logout():
    session.clear()
    return success_response("Logged out successfully.")


@auth_bp.get("/me")
def current_admin():
    return success_response(
        data={
            "isAuthenticated": is_admin_logged_in(),
            "username": session.get("admin_username"),
        }
    )
