#!/usr/bin/env python3

"""
This module contains the storage engine for 
the HBNB system.
"""


from typing import Any, Optional
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import select, func
from sqlalchemy.orm import sessionmaker, scoped_session
import os


from models.basemodel import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

load_dotenv()


class DBStorage:
    """
    This class stores objects of HBNB system in a file or database.
    """

    __engine = None
    __session = None
    __user = os.getenv("HBNB_POSTGRES_USER")
    __password = os.getenv("HBNB_POSTGRES_PWD")
    __host = os.getenv("HBNB_POSTGRES_HOST")
    __port = os.getenv("HBNB_POSTGRES_PORT")
    __db = os.getenv("HBNB_POSTGRES_DB")
    __classes: dict[str, Any] = {
        "Amenity": Amenity,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User,
    }

    def __init__(self) -> None:
        self.__url = (f"postgresql+psycopg2://{self.__user}:{self.__password}"
                         f"@{self.__host}:{self.__port}/{self.__db}")
        self.__engine = create_engine(self.__url, pool_pre_ping=True, echo=True)
        
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls: Optional[str]=None) -> dict[str, str]:
        """
        Returns all the objects or objects of a given class from database.
        """
        if not self.__session:
            raise ValueError("No session assigned")
        
        result = None
        if cls and cls in self.__classes:
            result = self.__session.scalars(select(self.__classes[cls]))
        else:
            for cls_name in self.__classes.values():
                result = self.__session.scalars(select(self.__classes[cls_name]))
        
        if not result:
            raise ValueError("No object found")
        
        objects: dict[str, str] = {}
        for obj in result:
            key = f"{obj.__class__.__name__}.{obj.id}"
            objects[key] = obj.to_dict()
        return objects
    
    def count(self, cls: Optional[str]=None) -> dict[str, Any]:
        """Returns count of objects of a given class or objects of all classes"""
        assert self.__session is not None, "Session has not been initialized"

        if cls in self.__classes:
            cls_objects_count = self.__session.scalar(
                select(func.count()).select_from(self.__classes[cls])
            )
            return {cls: cls_objects_count}
        
        all_objects_count: dict[str, Any] = {}
        for cls_name in self.__classes:
            cls_objects_count = self.__session.scalar(
                select(func.count()).select_from(self.__classes[cls_name])
            )
            all_objects_count[cls_name] = cls_objects_count
        return all_objects_count

       
    def delete(self, obj: Optional[BaseModel]=None) -> None:
        """
        Deletes the given object from session.
        """
        if not self.__session:
            raise ValueError("No session assigned")
        
        if obj:
            self.__session.delete(obj)
      
    def new(self, obj: BaseModel) -> None:
        """
        Adds object to session.
        """
        if not self.__session:
            raise ValueError("No session assigned")
        self.__session.add(obj)

    def save(self):
        """
        Persists changes in objects to the database.
        """
        if not self.__session:
            raise ValueError("No session assigned")
        self.__session.commit()

    def reload(self) -> None:
        """
        Creates tables in the database.
        """
        if not self.__engine:
            raise ValueError("No engine found")
        try:
            Base.metadata.create_all(self.__engine)
        except Exception as e:
            print(e)
        
        self.__session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
            )
