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


    def __init__(self, *args: tuple[Any, ...], **kwargs: Any):
        """Intializes instance attributes"""
        if "__class__" in kwargs:
            kwargs.pop("__class__")
            kwargs["created_at"] = datetime.fromisoformat(kwargs["created_at"])
            kwargs["updated_at"] = datetime.fromisoformat(kwargs["updated_at"])
            self.__dict__.update(kwargs)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.__dict__.update(kwargs)

    def __str__(self):
        """
        Returns a user friendly string representation
        of an object in the HBNB system.
        """
        return f"[{self.__class__.__name__}]({self.id})({self.__dict__})"

    def save(self):
        """
        Saves an object of the HBNB system to storage.
        """
        self.updated_at = datetime.now()
        from models import storage
        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of an object in the
        HBNB system.
        """
        obj_dict = deepcopy(self.__dict__)
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        obj_dict.pop("_sa_instance_state", None)
        return obj_dict
    
    def delete(self) -> None:
        """
        Deletes object from storage.
        """
        from models import storage
        storage.delete(self)


def main():
    logging.debug("Start Program")
    base = BaseModel()
    base_kwargs = BaseModel(name="ALX")
    base_dict = base.to_dict()
    new_base = BaseModel(**base_dict)
    logging.debug(f"base.__dict__: {base.__dict__}")
    logging.debug(f"base_kwargs: {base_kwargs.__dict__}")
    logging.debug(f"base.__str__: {base}")
    logging.debug(f"base.to_dict(): {base_dict}")
    logging.debug(f"base.__dict__: {base.__dict__}")
    logging.debug(f"new_base.__dict__: {new_base.__dict__}")
    logging.debug("End Program")


if __name__ == "__main__":
    main()
