#!/usr/bin/env python3

"""
This module contains Amenity class for the HBNB system.
"""

from models.basemodel import BaseModel


class Amenity(BaseModel):
    """
    Defines Amenity attributes and methods for the system.
    """

    name: str = ""
