#!/usr/bin/env python3

"""

"""

from flask import abort, jsonify
import logging
from typing import Any, cast

from api.v1.views import app_views
from api.v1.views.utils import get_obj, get_request_data
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id: str):
    """Add a place to the database."""
    city_obj = get_obj("City", city_id)
    place_data = get_request_data()

    if "name" not in place_data:
        abort(400, description="Missing name")
    if "user_id" not in place_data:
        abort(400, description="Missing user_id")
    get_obj("User", place_data["user_id"])

    place_data["city_id"] = city_obj.id
    try:
        place = Place(**place_data)
        place.save()
    except Exception as e:
        logger.error(f"{e}")
        abort(500, description="Unsuccessful")
    
    return place.to_dict(), 201

@app_views.route("/cities/<city_id>/places")
def all_places(city_id: str):
    """Retrieves all places in a city."""
    city_obj = cast(City, get_obj("City", city_id))
    places: list[dict[str, Any]] = [place.to_dict() for place in city_obj.places]
    return places, 200

@app_views.route("/places_search", methods=["POST"])
def place_search():
    """
    Retrieves all Place objects depending of the JSON in the body of the request.

    The JSON can contain 3 optional keys:

    states: list of State ids
    cities: list of City ids
    amenities: list of Amenity ids
    """
    search_data = get_request_data()
    all_places = storage.all("Place")
    
    if not search_data or not any(search_data.values()):
        return all_places, 200
    
    non_empty_keys = {k.lower() for k, v in search_data.items() if v}
    if non_empty_keys == {"states"}:
        state_objects: list[State] = [
            cast(State, get_obj("State", state_id)) for state_id in search_data["states"]
        ]
        city_objects: list[City] = [
            city_obj for state_obj in state_objects for city_obj in state_obj.cities
        ]
        place_objects: list[Place] = [
            place_obj for city_obj in city_objects for place_obj in city_obj.places
        ]
        places = [place_obj.to_dict() for place_obj in set(place_objects)]
        return places, 200
    
    elif non_empty_keys == {"cities"}:
        city_objects: list[City] = [
            cast(City, get_obj("City", city_id)) for city_id in search_data["cities"]
        ]
        place_objects: list[Place] = [
            place_obj for city_obj in city_objects for place_obj in city_obj.places
        ]
        places = [place_obj.to_dict() for place_obj in set(place_objects)]
        return places, 200
    
    elif non_empty_keys == {"states", "cities"}:
        cities: list[City] = [
            cast(City, get_obj("City", city_id)) for city_id in search_data["cities"]
        ]
        state_objects: list[State] = [
            cast(State, get_obj("State", state_id)) for state_id in search_data["states"]
        ]
        city_objects: list[City] = [
            city_obj for state_obj in state_objects for city_obj in state_obj.cities
        ]
        city_objects.extend(cities)
        place_objects: list[Place] = [
            place_obj for city_obj in set(city_objects) for place_obj in city_obj.places
        ]
        places = [place_obj.to_dict() for place_obj in set(place_objects)]
        return places, 200
    
    elif non_empty_keys == {"states", "amenities"}:
        amenity_objects: list[Amenity] = [
            cast(Amenity, get_obj("Amenity", amenity_id))
            for amenity_id in search_data["amenities"]
        ]
        state_objects: list[State] = [
            cast(State, get_obj("State", state_id))
            for state_id in search_data["states"]
        ]
        city_objects: list[City] = [
            city_obj
            for state_obj in state_objects for city_obj in state_obj.cities
        ]
        place_objects: list[Place] = [
            place_obj
            for city_obj in city_objects for place_obj in city_obj.places
        ]
        places = [
            place_obj.to_dict() for place_obj in set(place_objects)
            if set(place_obj.amenities).issubset(set(amenity_objects))
        ]
        return places, 200
    
    elif non_empty_keys == {"cities", "amenities"}:
        amenity_objects: list[Amenity] = [
            cast(Amenity, get_obj("Amenity", amenity_id))
            for amenity_id in search_data["amenities"]
        ]
        city_objects: list[City] = [
            cast(City, get_obj("City", city_id))
            for city_id in search_data["cities"]
        ]
        place_objects: list[Place] = [
            place_obj for city_obj in city_objects for place_obj in city_obj.places
        ]
        places = [
            place_obj.to_dict() for place_obj in set(place_objects)
            if set(place_obj.amenities).issubset(set(amenity_objects))
        ]
        return places, 200
    
    return jsonify({}), 200


@app_views.route("/places/<place_id>")
def get_place(place_id: str):
    """Retrieves a place from database."""
    place_obj = get_obj("Place", place_id)
    return place_obj.to_dict(), 200

@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id: str):
    """Updates a place in the database."""
    place_obj = get_obj("Place", place_id)
    place_data = get_request_data()

    place_data.pop("id", None)
    place_data.pop("city_id", None)
    place_data.pop("user_id", None)
    place_data.pop("created_at", None)
    place_data.pop("updated_at", None)

    for attr, value in place_data.items():
        setattr(place_obj, attr, value)
    place_obj.save()
    return place_obj.to_dict(), 200

@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id: str):
    """Deletes a place from database."""
    place_obj = get_obj("Place", place_id)
    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200
