#!/usr/bin/env python3

"""
This module contains Review class for the HBNB system.
"""

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column

from models.basemodel import BaseModel, Base


class Review(BaseModel, Base):
    """
    Defines Review attributes and methods for the system.
    """
    __tablename__ = "reviews"
    place_id = mapped_column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = mapped_column(String(60), ForeignKey("users.id"), nullable=False)
    text = mapped_column(String(1024), nullable=False)
