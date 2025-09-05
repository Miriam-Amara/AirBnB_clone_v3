#!/usr/bin/env python3

"""

"""

from flask import abort
from typing import cast
import logging

from api.v1.views import app_views
from api.v1.views.utils import get_request_data
from api.v1.auth.jwt_bearer import JWTBearerAuth
from models.user import User


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

jwt_auth = JWTBearerAuth()

@app_views.route("/login", strict_slashes=False, methods=["POST"])
def login():
    from api.v1.app import bycrypt
    """Login user"""
    user_data = get_request_data()
    if "email" not in user_data:
        abort(400, description="Missing email")
    if "password" not in user_data:
        abort(400, description="Missing password")

    user_obj: User = cast(User, User.search(user_data["email"]))
    if not user_obj:
        abort(404)
    
    is_valid_password = (
        bycrypt
        .check_password_hash(user_obj.password, user_data["password"]) # type: ignore
    )
    if not is_valid_password:
        abort(400, description="Invalid password")
    
    access_token = jwt_auth.encode_jwt_token(user_obj.id)
    return access_token, 200


@app_views.route("/logout", strict_slashes=False, methods=["POST"])
def logout():
    """Logout user"""
    return {"msg": "Logout successful"}
