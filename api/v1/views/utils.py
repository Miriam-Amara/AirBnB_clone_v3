#!/usr/bin/env python3

"""

"""

from flask import abort, request

from models import storage

def get_obj(cls: str, id: str):
    """Checks whether an object exists in the database using its class and id."""
    obj = storage.get(cls, id)
    if not obj:
        abort(404, description=f"{cls} {id} not found")
    return obj

def get_request_data():
    """Checks if a request data is valid json."""
    try:
        obj_data = request.get_json()
    except Exception:
        abort(400, description="Not a json")
    return obj_data
