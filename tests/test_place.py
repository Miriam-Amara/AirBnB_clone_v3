#!/usr/bin/env python3

"""
This module contains unittests for the Place class.
"""

from copy import deepcopy
from datetime import datetime
from dotenv import load_dotenv
import json
import os
import unittest

from models.place import Place
from models import storage

load_dotenv()


class TestAmenity(unittest.TestCase):
    """
    Implements test cases for the Place class.
    """

    def setUp(self) -> None:
        """
        Initializes objects of the Place class.
        """
        places = {"one": "Television", "two": "Wifi", "three": "Smart Doors"}
        self.place1 = Place()
        self.place2 = Place(**places)
        self.filepath = os.getenv("FILE_STORAGE")

    def tearDown(self) -> None:
        """
        Cleans up after each test method by clearing stored data.
        """
        all_objects = storage.all()
        key1 = f"{self.place1.__class__.__name__}.{self.place1.id}"
        key2 = f"{self.place2.__class__.__name__}.{self.place2.id}"
        if key1 in all_objects:
            del all_objects[key1]
        if key2 in all_objects:
            del all_objects[key2]
        storage.save()

    def test_attributes_present(self):
        """
        Tests that the Place object has all required attributes.
        """
        self.assertIn("id", self.place1.__dict__)
        self.assertIn("created_at", self.place1.__dict__)
        self.assertIn("updated_at", self.place1.__dict__)
        self.assertIn("one", self.place2.__dict__)
        self.assertIn("two", self.place2.__dict__)
        self.assertIn("three", self.place2.__dict__)
        self.assertIn("name", Place.__dict__)
        self.assertIn("city_id", Place.__dict__)
        self.assertIn("user_id", Place.__dict__)
        self.assertIn("description", Place.__dict__)
        self.assertIn("number_rooms", Place.__dict__)
        self.assertIn("number_bathrooms", Place.__dict__)
        self.assertIn("max_guest", Place.__dict__)
        self.assertIn("price_by_night", Place.__dict__)
        self.assertIn("latitude", Place.__dict__)
        self.assertIn("longitude", Place.__dict__)
        self.assertIn("amenity_ids", Place.__dict__)

        self.assertIsInstance(self.place1.id, str)
        self.assertIsInstance(Place.name, str)
        self.assertIsInstance(self.place1.created_at, datetime)
        self.assertIsInstance(self.place1.updated_at, datetime)

    def test_str_method(self):
        """
        Tests that the __str__() method returns a readable string
        representation of an Place object.
        """
        return_value = (
            f"[{self.place1.__class__.__name__}]"
            f"({self.place1.id})({self.place1.__dict__})"
        )
        self.assertEqual(str(self.place1), return_value)

    def test_save_method(self):
        """
        Tests that the save() method serializes and stores the Place object.
        """
        self.place1.save()
        key = f"{self.place1.__class__.__name__}.{self.place1.id}"
        if not self.filepath:
            raise Exception(f"{self.filepath} storage file not found")
        with open(self.filepath) as file_obj:
            all_objects = json.load(file_obj)
            self.assertIn(key, all_objects)

    def test_to_dict_method(self):
        """
        Tests that the to_dict() method returns a dictionary representation
        suitable for serialization.
        """
        obj_dict = deepcopy(self.place1.__dict__)
        obj_dict["__class__"] = self.place1.__class__.__name__
        obj_dict["created_at"] = self.place1.created_at.isoformat()
        obj_dict["updated_at"] = self.place1.updated_at.isoformat()
        self.assertEqual(self.place1.to_dict(), obj_dict)

    def test_recreate_obj(self):
        """
        Tests that an object is recreated successfully with
        the kwargs from to_dict method.
        """
        info = self.place2.to_dict()
        new_place = Place(**info)
        self.assertIsInstance(new_place.created_at, datetime)
        self.assertIsInstance(new_place.updated_at, datetime)


if __name__ == "__main__":
    unittest.main(verbosity=2)
