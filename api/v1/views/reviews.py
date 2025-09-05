#!/usr/bin/env python3

"""

"""

from flask import abort, jsonify
import logging
from typing import Any

from api.v1.views import app_views
from api.v1.views.utils import get_obj, get_request_data
from models import storage
from models.review import Review


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app_views.route("/places/<place_id>/reviews", strict_slashes=False, methods=["POST"])
def create_review(place_id: str):
    place_obj = get_obj("Place", place_id)
    review_data = get_request_data()

    if "text" not in review_data:
        abort(400, description="Missing text")
    if "user_id" not in review_data:
        abort(400, description="Missing user_id")
    user_exists = get_obj("User", review_data["user_id"]) # type: ignore

    review_data["place_id"] = place_obj.id
    try:
        review = Review(**review_data)
        review.save()
    except Exception as e:
        logger.error(f"{e}")
        abort(500, description="Unsuccessful")
    return review.to_dict(), 201

@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def all_reviews(place_id: str):
    """Retrieves all the reviews of a place from database."""
    place_obj = get_obj("Place", place_id)
    place_reviews: list[dict[str, Any]] = [review.to_dict() for review in place_obj.reviews] # type: ignore
    return place_reviews, 200

@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id: str):
    """Retrieves a review from database."""
    review_obj = get_obj("Review", review_id)
    return review_obj.to_dict(), 200

@app_views.route("/review/<review_id>", strict_slashes=False, methods=["PUT"])
def update_review(review_id: str):
    """Updates a review in the database."""
    review_obj = get_obj("Review", review_id)
    review_data = get_request_data()

    review_data.pop("id", None)
    review_data.pop("place_id", None)
    review_data.pop("user_id", None)
    review_data.pop("created_at", None)
    review_data.pop("updated_at", None)

    for attr, value in review_data.items():
        setattr(review_obj, attr, value)
    review_obj.save()
    return review_obj.to_dict(), 200

@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["DELETE"])
def delete_review(review_id: str):
    """Deletes a review from database."""
    review_obj = get_obj("Review", review_id)
    storage.delete(review_obj)
    storage.save
    return jsonify({}), 200
