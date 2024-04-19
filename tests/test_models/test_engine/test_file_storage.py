#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.state import State
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipIf(models.storage_t == "db", "Not Testing File Storage")
class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """set up"""
        cls.storage = FileStorage()

    def setUp(self):
        """Set up for the storage"""
        self.storage._FileStorage__file_path = "test_file.json"
        self.storage._FileStorage__objects = {}
        self.objects = self.storage._FileStorage__objects

    def tearDown(self):
        """Tear down testfiles and objects"""
        if os.path.exists("test_file.json"):
            os.remove("test_file.json")
        self.storage._FileStorage__objects = {}

    def test_all_with_class(self):
        """Test the class returns all objects"""
        state = State()
        self.storage.new(state)
        self.assertIn(state, self.storage.all(State).values())

    def test_all(self):
        """Returns all objects"""
        self.assertEqual(self.storage.all(), self.objects)

    def test_new(self):
        """Test that a new object is sucessfully created"""
        state = State()
        self.storage.new(state)
        self.assertIn(state, self.storage.all().values())

    def test_save(self):
        """Test the object is saved to file"""
        state = State()
        self.storage.new(state)
        self.storage.save()
        with open("test_file.json", "r") as file:
            self.assertIn(state, self.objects.values())

    def test_delete(self):
        """Tests that an object is deleted"""
        state = State()
        self.storage.new(state)
        self.assertIn(state, self.storage.all(State).values())

        self.storage.delete(state)
        self.assertNotIn(state, self.storage.all(State).values())

    def test_get(self):
        """Test the get a state with id or None"""
        state = State()
        self.storage.new(state)
        self.assertEqual(self.storage.get(State, state.id), state)

    def test_count(self):
        """Test the count returns the actual number of items"""
        state1 = State()
        state2 = State()
        self.storage.new(state1)
        self.storage.new(state2)
        self.assertEqual(self.storage.count(State), 2)
