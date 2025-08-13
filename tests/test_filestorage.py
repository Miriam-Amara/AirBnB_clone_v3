#!/usr/bin/env python3

"""
This module provides unittests for the FileStorage class.
"""

import os
import logging
import unittest
from dotenv import load_dotenv

from models.engine.file_storage import FileStorage
from models.basemodel import BaseModel


load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    format=" %(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    filename="tests/tests.log",
    force=True,
)

disable_logging: bool = False
if disable_logging:
    logging.disable(logging.CRITICAL)


class TestFileStorage(unittest.TestCase):
    """
    This class contains test cases for the BaseModel class.
    """

    def setUp(self) -> None:
        """
        Creates an instance of the BaseModel and FileStorage class
        for each test case.
        """
        self.base = BaseModel(name="HBNB", age=32)
        self.storage = FileStorage()
        self.file_storage = os.getenv("FILE_STORAGE")
        logging.debug("Start test_filestorage")

    def tearDown(self) -> None:
        """
        Cleans up after each test method by clearing stored data.
        """
        all_objects = self.storage.all()
        key = f"{self.base.__class__.__name__}.{self.base.id}"

        if key in all_objects:
            logging.debug(f"{key}")
            del all_objects[key]
            self.storage.save()
        logging.debug("End test_filestorage")

    def test_class_attributes_present(self) -> None:
        """
        Tests whether the given file attributes are present
        in FileStorage class.
        """
        logging.debug(f"Ist: {self.storage.all()}")
        self.assertIn("_FileStorage__objects", FileStorage.__dict__)
        self.assertIn("_FileStorage__objects", FileStorage.__dict__)

    def test_all_method(self) -> None:
        """
        Tests that the all method returns dictionary of objects.
        """
        logging.debug(f"2nd: {self.storage.all()}")
        all_objects = self.storage.all()
        self.assertIsInstance(all_objects, dict)
        for obj in all_objects.values():
            self.assertIsInstance(obj, BaseModel)

    def test_save_method(self) -> None:
        """
        Tests that the save method saves objects in the file storage.
        """
        logging.debug(f"3rd: {self.storage.all()}")
        self.base.save()
        if not self.file_storage:
            raise Exception(f"{self.file_storage} file does not exist.")
        file_storage_length = os.path.getsize(self.file_storage)
        self.assertGreater(file_storage_length, 0)
