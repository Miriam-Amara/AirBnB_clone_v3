#!/usr/bin/env python3

"""
This module contains User class for the HBNB system.
"""

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship

from models.basemodel import BaseModel, Base


class User(BaseModel, Base):
    """
    Defines blueprint for users in the system.
    """
    __tablename__ = "users"

    email = mapped_column(String(128), nullable=False)
    password = mapped_column(String(128), nullable=False)
    first_name = mapped_column(String(128), nullable=False)
    last_name = mapped_column(String(128), nullable=False)
    places = relationship("Place", backref="user", cascade="all, delete-orphan")
    reviews = relationship("Review", backref="user", cascade="all, delete-orphan")
