#!/usr/bin/env python3

"""
This module contains unittests for the Review class.
"""

from copy import deepcopy
from datetime import datetime
from dotenv import load_dotenv
import json
import os
import unittest

from models import storage
from models.review import Review

load_dotenv()


class TestReview(unittest.TestCase):
    """
    Implements test cases for the Review class.
    """

    def setUp(self) -> None:
        """
        Initializes objects of the Review class.
        """
        reviews = {"one": "Television", "two": "Wifi", "three": "Smart Doors"}
        self.review1 = Review()
        self.review2 = Review(**reviews)
        self.filepath = os.getenv("FILE_STORAGE")

    def tearDown(self) -> None:
        """
        Cleans up after each test method by clearing stored data.
        """
        all_objects = storage.all()
        key1 = f"{self.review1.__class__.__name__}.{self.review1.id}"
        key2 = f"{self.review2.__class__.__name__}.{self.review2.id}"
        if key1 in all_objects:
            del all_objects[key1]
        if key2 in all_objects:
            del all_objects[key2]
        storage.save()

    def test_attributes_present(self):
        """
        Tests that the Review object has all required attributes.
        """
        self.assertIn("id", self.review1.__dict__)
        self.assertIn("created_at", self.review1.__dict__)
        self.assertIn("updated_at", self.review1.__dict__)
        self.assertIn("one", self.review2.__dict__)
        self.assertIn("two", self.review2.__dict__)
        self.assertIn("three", self.review2.__dict__)
        self.assertIn("place_id", Review.__dict__)
        self.assertIn("user_id", Review.__dict__)
        self.assertIn("text", Review.__dict__)

        self.assertIsInstance(self.review1.id, str)
        self.assertIsInstance(Review.text, str)
        self.assertIsInstance(self.review1.created_at, datetime)
        self.assertIsInstance(self.review1.updated_at, datetime)

    def test_str_method(self):
        """
        Tests that the __str__() method returns a readable string
        representation of an Review object.
        """
        return_value = (
            f"[{self.review1.__class__.__name__}]"
            f"({self.review1.id})({self.review1.__dict__})"
        )
        self.assertEqual(str(self.review1), return_value)

    def test_save_method(self):
        """
        Tests that the save() method serializes and stores the Review object.
        """
        self.review1.save()
        key = f"{self.review1.__class__.__name__}.{self.review1.id}"
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
        obj_dict = deepcopy(self.review1.__dict__)
        obj_dict["__class__"] = self.review1.__class__.__name__
        obj_dict["created_at"] = self.review1.created_at.isoformat()
        obj_dict["updated_at"] = self.review1.updated_at.isoformat()
        self.assertEqual(self.review1.to_dict(), obj_dict)

    def test_recreate_obj(self):
        """
        Tests that an object is recreated successfully with
        the kwargs from to_dict method.
        """
        info = self.review2.to_dict()
        new_amenity = Review(**info)
        self.assertIsInstance(new_amenity.created_at, datetime)
        self.assertIsInstance(new_amenity.updated_at, datetime)


if __name__ == "__main__":
    unittest.main(verbosity=2)
