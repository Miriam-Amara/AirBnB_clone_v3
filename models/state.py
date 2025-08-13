#!/usr/bin/env python3

"""
This module contains State class for the HBNB system.
"""

from models.basemodel import BaseModel


class State(BaseModel):
    """
    Defines the State attributes and methods for the system.
    """

    name: str = ""
