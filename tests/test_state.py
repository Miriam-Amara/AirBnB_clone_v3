#!/usr/bin/env python3

"""
This module contains unittests for the State class.
"""

from copy import deepcopy
from datetime import datetime
from dotenv import load_dotenv
import json
import os
import unittest

from models import storage
from models.state import State

load_dotenv()


class TestState(unittest.TestCase):
    """
    Implements test cases for the State class.
    """

    def setUp(self) -> None:
        """
        Initializes objects of the State class.
        """
        states = {"one": "Television", "two": "Wifi", "three": "Smart Doors"}
        self.state1 = State()
        self.state2 = State(**states)
        self.filepath = os.getenv("FILE_STORAGE")

    def tearDown(self) -> None:
        """
        Cleans up after each test method by clearing stored data.
        """
        all_objects = storage.all()
        key1 = f"{self.state1.__class__.__name__}.{self.state1.id}"
        key2 = f"{self.state2.__class__.__name__}.{self.state2.id}"
        if key1 in all_objects:
            del all_objects[key1]
        if key2 in all_objects:
            del all_objects[key2]
        storage.save()

    def test_attributes_present(self):
        """
        Tests that the State object has all required attributes.
        """
        self.assertIn("id", self.state1.__dict__)
        self.assertIn("created_at", self.state1.__dict__)
        self.assertIn("updated_at", self.state1.__dict__)
        self.assertIn("one", self.state2.__dict__)
        self.assertIn("two", self.state2.__dict__)
        self.assertIn("three", self.state2.__dict__)
        self.assertIn("name", State.__dict__)

        self.assertIsInstance(self.state1.id, str)
        self.assertIsInstance(self.state1.created_at, datetime)
        self.assertIsInstance(self.state1.updated_at, datetime)
        self.assertIsInstance(State.name, str)

    def test_str_method(self):
        """
        Tests that the __str__() method returns a readable string
        representation of an State object.
        """
        return_value = (
            f"[{self.state1.__class__.__name__}]"
            f"({self.state1.id})({self.state1.__dict__})"
        )
        self.assertEqual(str(self.state1), return_value)

    def test_save_method(self):
        """
        Tests that the save() method serializes and stores the State object.
        """
        self.state1.save()
        key = f"{self.state1.__class__.__name__}.{self.state1.id}"
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
        obj_dict = deepcopy(self.state1.__dict__)
        obj_dict["__class__"] = self.state1.__class__.__name__
        obj_dict["created_at"] = self.state1.created_at.isoformat()
        obj_dict["updated_at"] = self.state1.updated_at.isoformat()
        self.assertEqual(self.state1.to_dict(), obj_dict)

    def test_recreate_obj(self):
        """
        Tests that an object is recreated successfully with
        the kwargs from to_dict method.
        """
        info = self.state2.to_dict()
        new_amenity = State(**info)
        self.assertIsInstance(new_amenity.created_at, datetime)
        self.assertIsInstance(new_amenity.updated_at, datetime)


if __name__ == "__main__":
    unittest.main(verbosity=2)
