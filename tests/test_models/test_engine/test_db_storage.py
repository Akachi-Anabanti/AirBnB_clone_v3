#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
from unittest.mock import patch
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipIf(models.storage_t != 'db', "Not testing db Storage")
class TestDBStorage(unittest.TestCase):
    """Test the File Storage class"""

    @classmethod
    def setUpClass(cls):
        """Setup for the tests"""
        cls.storage = DBStorage()

    def setUp(self):
        """sets up the tests"""
        self.session_patcher = patch.object(self.storage,
                                            '_DBStorage__session')
        self.mock_session = self.session_patcher.start()

    def tearDown(self):
        """Tears Down the Tests"""
        self.session_patcher.stop()

    def test_all_returns_dict(self):
        """Tests the db method all returns a dict"""
        self.assertIs(type(self.storage.all()), dict)

    def test_all(self):
        """Tests the all method is called"""
        self.storage.all()
        self.mock_session.query.assert_called()

    def test_new(self):
        """Test the new method"""
        state = State()
        self.storage.new(state)
        self.mock_session.add.assert_called_with(state)

    def test_save(self):
        """Tests the save method"""
        self.storage.save()
        self.mock_session.commit.assert_called()

    def test_get_class(self):
        """tests that the get method returns a valid object or none"""
        self.storage.get(State, "1234")
        self.mock_session.query.assert_called()

    def test_count(self):
        """Test the count method returns the actual number of objects"""
        self.storage.count(State)
        self.mock_session.query.assert_called()

    def test_delete(self):
        """Test that an object is succefully deleted"""
        state = State()
        self.storage.delete(state)
        self.mock_session.delete.assert_called_with(state)
