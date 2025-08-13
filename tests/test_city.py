#!/usr/bin/env python3

"""
This module contains unittests for the City class.
"""

from copy import deepcopy
from datetime import datetime
from dotenv import load_dotenv
import json
import os
import unittest

from models import storage
from models.city import City

load_dotenv()


class TestCity(unittest.TestCase):
    """
    Implements test cases for the City class.
    """

    def setUp(self) -> None:
        """
        Initializes objects of the City class.
        """
        cities = {"one": "Television", "two": "Wifi", "three": "Smart Doors"}
        self.city1 = City()
        self.city2 = City(**cities)
        self.filepath = os.getenv("FILE_STORAGE")

    def tearDown(self) -> None:
        """
        Cleans up after each test method by clearing stored data.
        """
        all_objects = storage.all()
        key1 = f"{self.city1.__class__.__name__}.{self.city1.id}"
        key2 = f"{self.city2.__class__.__name__}.{self.city2.id}"
        if key1 in all_objects:
            del all_objects[key1]
        if key2 in all_objects:
            del all_objects[key2]
        storage.save()

    def test_attributes_present(self):
        """
        Tests that the City object has all required attributes.
        """
        self.assertIn("id", self.city1.__dict__)
        self.assertIn("created_at", self.city1.__dict__)
        self.assertIn("updated_at", self.city1.__dict__)
        self.assertIn("one", self.city2.__dict__)
        self.assertIn("two", self.city2.__dict__)
        self.assertIn("three", self.city2.__dict__)
        self.assertIn("name", City.__dict__)
        self.assertIn("state_id", City.__dict__)

        self.assertIsInstance(self.city1.id, str)
        self.assertIsInstance(City.name, str)
        self.assertIsInstance(self.city1.created_at, datetime)
        self.assertIsInstance(self.city1.updated_at, datetime)

    def test_str_method(self):
        """
        Tests that the __str__() method returns a readable string
        representation of an City object.
        """
        return_value = (
            f"[{self.city1.__class__.__name__}]"
            f"({self.city1.id})({self.city1.__dict__})"
        )
        self.assertEqual(str(self.city1), return_value)

    def test_save_method(self):
        """
        Tests that the save() method serializes and stores the City object.
        """
        self.city1.save()
        key = f"{self.city1.__class__.__name__}.{self.city1.id}"
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
        obj_dict = deepcopy(self.city1.__dict__)
        obj_dict["__class__"] = self.city1.__class__.__name__
        obj_dict["created_at"] = self.city1.created_at.isoformat()
        obj_dict["updated_at"] = self.city1.updated_at.isoformat()
        self.assertEqual(self.city1.to_dict(), obj_dict)


if __name__ == "__main__":
    unittest.main(verbosity=2)
