#!/usr/bin/env python3

"""

"""

from flask import abort, jsonify
import logging

from api.v1.views import app_views
from api.v1.views.utils import get_obj, get_request_data
from models.state import State
from models import storage


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    filename="api/v1/views/views.log",
    force=True
)

disable_logging: bool = False
if disable_logging:
    logging.disable(logging.CRITICAL)


@app_views.route("/states")
def states():
    """Retrieves the list of objects of all states."""
    all_states = storage.all("State")
    return all_states

@app_views.route("/states", methods=["POST"])
def create_state():
    """Creates a new state and save it to the database."""
    state_data = get_request_data()

    if "name" not in state_data:
        abort(400, description="Missing name")
    
    try:
        state = State(**state_data)
        state.save()
    except Exception as e:
        logging.debug(f"{e}")
        abort(500, description="Unsuccessful")
    
    return state.to_dict(), 201

@app_views.route("/states/<state_id>")
def get_state(state_id: str):
    """Returns a state object by id"""
    state_obj = get_obj("State", state_id)
    return state_obj.to_dict()

@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id: str):
    """Deletes state object from database"""
    state_obj = get_obj("State", state_id)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id: str):
    """Updates a state in the database"""
    state_obj = get_obj("State", state_id)
    state_data = get_request_data()
    
    state_data.pop("id", None)
    state_data.pop("created_at", None)
    state_data.pop("updated_at", None)

    for attr, value in state_data.items():
        setattr(state_obj, attr, value)
    state_obj.save()
    return state_obj.to_dict()
