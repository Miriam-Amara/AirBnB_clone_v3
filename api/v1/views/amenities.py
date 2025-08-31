#!/usr/bin/env python3

"""

"""

from flask import abort, jsonify
import logging

from api.v1.views import app_views
from api.v1.views.utils import get_obj, get_request_data
from models import storage
from models.amenity import Amenity


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    filename="api/v1/views/views.log",
    force=True
)

disable_logging: bool = False
if disable_logging:
    logging.disable(logging.CRITICAL)



@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """Creates amenity and saves it to database."""
    amenity_data = get_request_data()

    if "name" not in amenity_data:
        abort(400, description="Missing name")

    try:
        amenity = Amenity(**amenity_data)
        amenity.save()
    except Exception as e:
        logging.error(f"{e}")
        abort(500, description="Unsuccessful")
    
    return amenity.to_dict(), 201

@app_views.route("/amenities")
def all_amenities():
    """Retrieves the list of all amenities in database."""
    return storage.all("Amenity"), 200

@app_views.route("/amenities/<amenity_id>")
def get_amenity(amenity_id: str):
    """Retrieves an amenity from the database."""
    amenity_obj = get_obj("Amenity", amenity_id)
    return amenity_obj.to_dict(), 200

@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id: str):
    """Updates amenity in database."""
    amenity_obj = get_obj("Amenity", amenity_id)
    amenity_data = get_request_data()

    amenity_data.pop("id", None)
    amenity_data.pop("created_at", None)
    amenity_data.pop("updated_at", None)

    for attr, value in amenity_data.items():
        setattr(amenity_obj, attr, value)
    amenity_obj.save()
    return amenity_obj.to_dict(), 200

@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id: str):
    """Deletes amenity from database."""
    amenity_obj = get_obj("Amenity", amenity_id)
    storage.delete(amenity_obj)
    storage.save()
    return jsonify({}), 200
