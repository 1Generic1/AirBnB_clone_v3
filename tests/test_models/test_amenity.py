#!/usr/bin/python3
import unittest
from datetime import datetime
from models.amenity import Amenity
from models.base_model import BaseModel
import os


class TestBaseModel(unittest.TestCase):
    def test_instance_attributes(self):
        amenity = Amenity()
        self.assertIsInstance(amenity.name, str)


if __name__ == '__main__':
    unittest.main()
