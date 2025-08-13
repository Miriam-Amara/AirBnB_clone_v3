#!/usr/bin/env python3

"""
This module contains City class for the HBNB system.
"""

from models.basemodel import BaseModel


class City(BaseModel):
    """
    Defines City attributes and methods for the system.
    """

    state_id: str = ""
    name: str = ""
