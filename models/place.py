#!/usr/bin/env python3

"""
This module contains Place class for the HBNB system.
"""

from sqlalchemy import String, Integer, Float, ForeignKey, Table, Column
from sqlalchemy.orm import mapped_column, relationship

from models.basemodel import BaseModel, Base


place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id"), primary_key=True, nullable=False),
    Column("amenity_id", String(60), ForeignKey("amenities.id"), primary_key=True, nullable=False)
)

class Place(BaseModel, Base):
    """
    Defines Place attributes and Methods for the system.
    """
    __tablename__ = "places"
    city_id = mapped_column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = mapped_column(String(60), ForeignKey("users.id"), nullable= False)
    name = mapped_column(String(128), nullable=False)
    description = mapped_column(String(1024))
    number_rooms = mapped_column(Integer, nullable=False, default=0)
    number_bathrooms = mapped_column(Integer, nullable=False, default=0)
    max_guest = mapped_column(Integer, nullable=False, default=0)
    price_by_night = mapped_column(Integer, nullable=False, default=0)
    latitude = mapped_column(Float)
    longitude = mapped_column(Float)
    reviews = relationship("Review", backref="place", cascade="all, delete-orphan")
    amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)
