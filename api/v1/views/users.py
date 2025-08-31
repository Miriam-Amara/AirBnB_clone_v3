#!/usr/bin/env python3

"""

"""

from flask import abort, jsonify
import logging

from api.v1.views import app_views
from api.v1.views.utils import get_obj, get_request_data
from models import storage
from models.user import User


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    filename="api/v1/views/views.log",
    force=True
)

disable_logging: bool = False
if disable_logging:
    logging.disable(logging.CRITICAL)



@app_views.route("/users", methods=["POST"])
def create_user():
    """Adds a user to the database."""
    user_data = get_request_data()

    if "email" not in user_data:
        abort(400, description="Missing email")
    if "password" not in user_data:
        abort(400, description="Missing password")
    if "first_name" not in user_data:
        abort(400, description="Missing first name")
    if "last_name" not in user_data:
        abort(400, description="Missing last name")
    
    try:
        user = User(**user_data)
        user.save()
    except Exception as e:
        logging.error(f"{e}")
        abort(500, description="Unsuccessful")
    return user.to_dict(), 201

@app_views.route("/users")
def all_user():
    """Retrieves a list of all users in the database."""
    return storage.all("User"), 200

@app_views.route("/users/<user_id>")
def get_user(user_id: str):
    """Retrieves a user from the database"""
    user_obj = get_obj("User", user_id)
    return user_obj.to_dict(), 200

@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id: str):
    """Updates a user info in the database"""
    user_obj = get_obj("User", user_id)
    user_data = get_request_data()

    user_data.pop("id", None)
    user_data.pop("created_at", None)
    user_data.pop("updated_at", None)
    user_data.pop("email", None)

    for attr, value in user_data.items():
        setattr(user_obj, attr, value)
    user_obj.save()
    return user_obj.to_dict(), 200

@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id: str):
    """Deletes a user from database."""
    user_obj = get_obj("User", user_id)
    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200
