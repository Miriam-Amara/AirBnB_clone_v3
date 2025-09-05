#!/usr/bin/env python3

"""

"""

from flask import abort, jsonify
import logging

from api.v1.views import app_views
from api.v1.views.utils import get_obj, get_request_data
from models import storage
from models.user import User


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app_views.route("/register", strict_slashes=False, methods=["POST"])
def create_user():
    """Adds a user to the database."""
    from api.v1.app import bycrypt
    user_data = get_request_data()

    if "email" not in user_data:
        abort(400, description="Missing email")
    if User.search(user_data["email"]):
        abort(400, description="Email already exists")
    if "password" not in user_data:
        abort(400, description="Missing password")
    if "first_name" not in user_data:
        abort(400, description="Missing first_name")
    if "last_name" not in user_data:
        abort(400, description="Missing last_name")
    
    hashed_password: str = (
        bycrypt
        .generate_password_hash(user_data["password"]) # type: ignore
        .decode('utf-8')
    )
    user_data["password"] = hashed_password
    try:
        user = User(**user_data)
        user.save()
    except Exception as e:
        logger.error(f"{e}")
        abort(500, description="Unsuccessful")
    return user.to_dict(), 201

@app_views.route("/users", strict_slashes=False)
def all_user():
    """Retrieves a list of all users in the database."""
    return storage.all("User"), 200

@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user(user_id: str):
    """Retrieves a user from the database"""
    user_obj = get_obj("User", user_id)
    return user_obj.to_dict(), 200

@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id: str):
    """Updates a user info in the database"""
    user_obj = get_obj("User", user_id)
    user_data = get_request_data()

    user_data.pop("id", None)
    user_data.pop("created_at", None)
    user_data.pop("updated_at", None)
    user_data.pop("email", None)
    user_data.pop("password", None)

    for attr, value in user_data.items():
        setattr(user_obj, attr, value)
    user_obj.save()
    return user_obj.to_dict(), 200

@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user(user_id: str):
    """Deletes a user from database."""
    user_obj = get_obj("User", user_id)
    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200
