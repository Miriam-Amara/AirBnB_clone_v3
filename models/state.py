#!/usr/bin/env python3

"""
This module contains State class for the HBNB system.
"""

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String

from models.basemodel import BaseModel, Base


class State(BaseModel, Base):
    """
    Defines the State attributes and methods for the system.
    """
    __tablename__ = "states"
    name = mapped_column(String(128), nullable=False)
    cities = relationship("City", back_populates="state", cascade="all, delete-orphan")
