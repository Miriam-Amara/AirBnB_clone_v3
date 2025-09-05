#!/usr/bin/env python3

"""

"""

from flask import abort, request
from typing import Any, Optional

from models import storage
from models.basemodel import BaseModel

def get_obj(cls: str, id: str):
    """Checks whether an object exists in the database using its class and id."""
    obj: Optional[BaseModel] = storage.get(cls, id)
    if not obj:
        abort(404, description=f"{cls} {id} not found")
    return obj

def get_request_data() -> dict[str, Any]:
    """Checks if a request data is valid json."""
    try:
        obj_data = request.get_json()
    except Exception:
        abort(400, description="Not a json")
    return obj_data
