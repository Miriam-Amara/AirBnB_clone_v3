#!/usr/bin/env python3

"""
This module contains City class for the HBNB system.
"""

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, ForeignKey

from models.basemodel import BaseModel, Base


class City(BaseModel, Base):
    """
    Defines City attributes and methods for the system.
    """
    __tablename__ = "cities"

    name = mapped_column(String(128), nullable=False)
    state_id = mapped_column(String(60), ForeignKey("states.id"), nullable=False)
    state = relationship("State", back_populates="cities")
    places = relationship("Place", backref="cities", cascade="all, delete-orphan")
