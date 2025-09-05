#!/usr/bin/env python3

"""

"""

from flask import abort, jsonify
import logging
from typing import Any, cast

from api.v1.views import app_views
from api.v1.views.utils import get_obj
from models.place import Place
from models.amenity import Amenity


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", strict_slashes=False, methods=["POST"])
def add_place_amenity(place_id: str, amenity_id: str):
    """Links amenity object to a place"""
    place_obj = cast(Place, get_obj("Place", place_id))
    amenity_obj = cast(Amenity, get_obj("Amenity", amenity_id))

    if amenity_obj in place_obj.amenities:
        return amenity_obj.to_dict(), 200
    place_obj.amenities.append(amenity_obj)
    place_obj.save()
    return amenity_obj.to_dict(), 201

@app_views.route("/places/<place_id>/amenities", strict_slashes=False)
def get_place_amenities(place_id: str):
    """Retrieves the list of all amenities of a Place."""
    place_obj = cast(Place, get_obj("Place", place_id))
    amenities: list[dict[str, Any]] = [amenity.to_dict() for amenity in place_obj.amenities]
    return amenities, 200

@app_views.route("/places/<place_id>/amenities/<amenity_id>", strict_slashes=False, methods=["DELETE"])
def delete_place_amenity(place_id: str, amenity_id: str):
    """Deletes an Amenity object to a Place"""
    place_obj = cast(Place, get_obj("Place", place_id))
    amenity_obj = cast(Amenity, get_obj("Amenity", amenity_id))

    if amenity_obj not in place_obj.amenities:
        abort(404)
    place_obj.amenities.remove(amenity_obj)
    place_obj.save()
    return jsonify({}), 200
