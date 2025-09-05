#!/usr/bin/env python3

"""

"""

from flask import abort, jsonify
from typing import Any, cast
import logging

from api.v1.views import app_views
from api.v1.views.utils import get_obj, get_request_data
from models import storage
from models.city import City
from models.state import State


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app_views.route("/states/<state_id>/cities", strict_slashes=False, methods=["POST"])
def create_city(state_id: str):
    """Creates a city and saves it to database."""
    state_obj = get_obj("State", state_id)
    city_data = get_request_data()
    
    if "name" not in city_data:
        abort(400, description="Missing name")

    city_data["state_id"] = state_obj.id
    try:
        city = City(**city_data)
        city.save()
    except Exception as e:
        logger.error(f"{e}")
        abort(500, description="Unsuccessful")
    return city.to_dict(), 201

@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_state_cities(state_id: str):
    """Retrieves all the cities in a state."""
    state_obj = cast(State, get_obj("State", state_id))

    state_cities: list[dict[str, Any]] = [city.to_dict() for city in state_obj.cities]
    return state_cities, 200

@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def update_city(city_id: str):
    """Updates a city in the database"""
    city_obj = get_obj("City", city_id)
    city_data = get_request_data()

    city_data.pop("id", None)
    city_data.pop("state_id", None)
    city_data.pop("created_at", None)
    city_data.pop("updated_at", None)

    for attr, value in city_data.items():
        setattr(city_obj, attr, value)
    city_obj.save()
    return city_obj.to_dict(), 200
    
@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def delete_city(city_id: str):
    """Deletes a city from the database."""
    city_obj = get_obj("City", city_id)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200
