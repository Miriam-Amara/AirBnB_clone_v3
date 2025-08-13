#!/usr/bin/env python3

"""
This module provides unittest for the BaseModel class.
"""

from datetime import datetime
from uuid import UUID
import unittest

from models import storage
from models.basemodel import BaseModel


class TestBaseModel(unittest.TestCase):
    """
    This class contains test cases for the BaseModel class.
    """

    def setUp(self):
        """
        Creates an instance of the BaseModel class for each test case.
        """
        self.base: BaseModel = BaseModel()

    def tearDown(self) -> None:
        """
        Cleans up after each test method by clearing stored data.
        """
        all_objects = storage.all()
        key = f"{self.base.__class__.__name__}.{self.base.id}"

        if key in all_objects:
            del all_objects[key]
            storage.save()

    def test_attributes_present(self):
        """
        Tests the instance attributes of BaseModel class.
        Attr:
        id (str)
        created_at (datetime)
        updated_at (datetime)
        """
        self.assertIsInstance(UUID(self.base.id), UUID)
        self.assertIsInstance(self.base.created_at, datetime)
        self.assertIsInstance(self.base.updated_at, datetime)

    def test_methods_present(self):
        """
        Tests that the given methods are present in BaseModel class.
        Methods:
        __str__
        save
        to_dict
        """
        self.assertIn("__str__", BaseModel.__dict__)
        self.assertIn("save", BaseModel.__dict__)
        self.assertIn("to_dict", BaseModel.__dict__)

    def test_str_method(self):
        """
        Tests the return value of the str method in BaseModel class
        """
        result = (
            f"[{self.base.__class__.__name__}]"
            f"({self.base.id})({self.base.__dict__})"
        )
        self.assertEqual(self.base.__str__(), result)

    def test_save_method(self):
        """
        Test the save method.
        """
        pass

    def test_to_dict_method(self):
        """
        Tests if to_dict method adds 'class' key and changes
        created_at and updated_at datetime objects to str.
        """
        created_at = self.base.to_dict()["created_at"]
        updated_at = self.base.to_dict()["updated_at"]
        self.assertIn(self.base.__class__.__name__,
                      self.base.to_dict().values())
        self.assertIsInstance(created_at, str)
        self.assertIsInstance(updated_at, str)
        self.assertIsInstance(datetime.fromisoformat(created_at), datetime)
        self.assertIsInstance(datetime.fromisoformat(updated_at), datetime)

    def test_recreate_object(self):
        """
        Tests recreation of an instance kwargs from to_dict method
        """
        base_dict = self.base.to_dict()
        new_base = BaseModel(**base_dict)
        self.assertNotIn("__class__", new_base.__dict__)
        self.assertIsInstance(UUID(new_base.id), UUID)
        self.assertIsInstance(new_base.created_at, datetime)
        self.assertIsInstance(new_base.updated_at, datetime)

        # clear object from storage
        key = f"{new_base.__class__.__name__}.{new_base.id}"
        all_objects = storage.all()
        del all_objects[key]
        storage.save()

    def test_create_instance_with_args(self):
        """
        Tests that a new instance can be created using kwargs.
        """
        new_base = BaseModel(name="HBNB", age=23)
        self.assertIn("name", new_base.__dict__)
        self.assertIn("age", new_base.__dict__)

        # clear object from storage
        key = f"{new_base.__class__.__name__}.{new_base.id}"
        all_objects = storage.all()
        del all_objects[key]
        storage.save()


if __name__ == "__main__":
    unittest.main()
