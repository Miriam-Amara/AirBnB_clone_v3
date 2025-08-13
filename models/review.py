#!/usr/bin/env python3

"""
This module contains Review class for the HBNB system.
"""

from models.basemodel import BaseModel


class Review(BaseModel):
    """
    Defines Review attributes and methods for the system.
    """

    place_id: str = ""
    user_id: str = ""
    text: str = ""
