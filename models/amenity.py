#!/usr/bin/env python3

"""
This module contains Amenity class for the HBNB system.
"""

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship

from models.basemodel import BaseModel, Base


class Amenity(BaseModel, Base):
    """
    Defines Amenity attributes and methods for the system.
    """
    __tablename__ = "amenities"
    name = mapped_column(String(128), nullable=False)
    from models.place import place_amenity
    place_ammenities = relationship("Place", secondary=place_amenity)
