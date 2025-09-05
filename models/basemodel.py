#!/usr/bin/env python3

"""
This module contains the base class 'BaseModel'
for AirBnB system.
"""

from copy import deepcopy
from datetime import datetime
from uuid import uuid4
from typing import Any
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import String, DateTime
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format=" %(asctime)s - %(levelname)s - %(message)s",
    filename="models/models.log",
)

disable_logging: bool = False
if disable_logging:
    logging.disable(logging.CRITICAL)

class Base(DeclarativeBase):
    pass

class BaseModel:
    """
    A base class for the HBNB system
    """
    id = mapped_column(String(36), nullable=False, primary_key=True, sort_order=-3)
    created_at = mapped_column(DateTime, nullable=False, default=datetime.now(), sort_order=-2)
    updated_at = mapped_column(DateTime, nullable=False, default=datetime.now(), sort_order=-1)


    def __init__(self, *args: tuple[Any, ...], **kwargs: Any) -> None:
        """Intializes instance attributes"""
        if "__class__" in kwargs:
            kwargs.pop("__class__")
            kwargs["created_at"] = datetime.fromisoformat(kwargs["created_at"])
            kwargs["updated_at"] = datetime.fromisoformat(kwargs["updated_at"])
            self.__dict__.update(kwargs)
        else:
            kwargs.pop("id", None)
            kwargs.pop("created_at", None)
            kwargs.pop("updated_at", None)
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.__dict__.update(kwargs)

    def __str__(self) -> str:
        """
        Returns a user friendly string representation
        of an object in the HBNB system.
        """
        obj_dict_copy = deepcopy(self.__dict__)
        obj_dict_copy.pop("_sa_instance_state", None)
        return f"[{self.__class__.__name__}]({self.id})({obj_dict_copy})"

    def delete(self) -> None:
        """
        Deletes object from storage.
        """
        from models import storage
        storage.delete(self)

    def save(self) -> None:
        """
        Saves an object of the HBNB system to storage.
        """
        self.updated_at = datetime.now()
        from models import storage
        storage.new(self)
        storage.save()

    def to_dict(self) -> dict[str, Any]:
        """
        Returns a dictionary representation of an object in the
        HBNB system.
        """
        obj_dict = deepcopy(self.__dict__)
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        obj_dict.pop("_sa_instance_state", None)
        obj_dict.pop("password", None)
        return obj_dict
