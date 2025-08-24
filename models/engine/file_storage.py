#!/usr/bin/env python3

"""
This module contains the storage engine for 
the HBNB system.
"""


from typing import Any, Optional
from dotenv import load_dotenv
import json
import os


from models.basemodel import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

load_dotenv()


class FileStorage:
    """
    This class stores objects of HBNB system in a file or database.
    """

    __file_path: str = os.getenv("FILE_STORAGE", "storage.json")
    __objects: dict[str, BaseModel] = {}
    __classes: dict[str, Any] = {
        "BaseModel": BaseModel,
        "Amenity": Amenity,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User,
    }

    def all(self, cls: Optional[str]=None) -> dict[str, Any]:
        """
        Returns all the objects of HBNB system in storage or
        all objects of a given class.
        """
        if cls and cls in self.__classes:
            class_objects = {
                cls_id: obj for cls_id, obj in self.__objects.items() if cls in cls_id
                }
            return class_objects
        return self.__objects
    
    def delete(self, obj: Optional[BaseModel]=None) -> None:
        """
        Deletes the given object from storage.
        """
        if obj == None:
            return
        key = f"{obj.__class__.__name__}.{obj.id}"
        if key in self.__objects:
            self.__objects.pop(key, "Obj not found")


    def new(self, obj: BaseModel):
        """
        Sets in __objects the obj with key <obj classname>.id
        """
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """
        Serializes __objects to the json file (path: __file_path)
        """
        with open(FileStorage.__file_path, "w") as file_obj:
            all_objects = {}
            for obj_cls_id, obj in FileStorage.__objects.items():
                all_objects[obj_cls_id] = obj.to_dict()
            json.dump(all_objects, file_obj, indent=4)

    def reload(self) -> None:
        """
        Deserializes json file to __objects
        (only if the json file (__file_path) exists);
        otherwise, do nothing).
        """
        all_objects: dict[str, Any] = {}
        try:
            with open(self.__file_path) as file_obj:
                all_objects = json.load(file_obj)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            pass

        for cls_id, obj_dict in all_objects.items():
            class_name = cls_id.split(".")[0]
            obj: BaseModel = self.__classes[class_name](**obj_dict)
            self.__objects[cls_id] = obj
