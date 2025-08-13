#!/usr/bin/env python3

"""
This module contains Place class for the HBNB system.
"""

from models.basemodel import BaseModel


class Place(BaseModel):
    """
    Defines Place attributes and Methods for the system.
    """

    city_id: str = ""
    user_id: str = ""
    name: str = ""
    description: str = ""
    number_rooms: int = 0
    number_bathrooms: int = 0
    max_guest: int = 0
    price_by_night: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    amenity_ids: list[str] = []
