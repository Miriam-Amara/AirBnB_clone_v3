#!/usr/bin/env python3

"""
This module contains User class for the HBNB system.
"""

from models.basemodel import BaseModel


class User(BaseModel):
    """
    Defines blueprint for users in the system.
    """

    email: str = ""
    password: str = ""
    first_name: str = ""
    last_name: str = ""
