#!/usr/bin/python3
import unittest
from models.engine.file_storage import FileStorage
from models.state import State
from models.city import City

class TestFileStorageAllMethod(unittest.TestCase):
    def setUp(self):
        # Set up a clean environment before each test
        self.fs = FileStorage()

    def test_all_with_states_and_cities(self):
        """
        Test the all method with both State and City objects in the storage
        """
        storage = FileStorage()
        state = State()
        city = City()

        storage.new(state)
        storage.new(city)

        all_objects = storage.all()

        print("All Objects:", all_objects)  # Add this line to print the objects

        # Check if the State ID is in the list of all objects
        self.assertIn(state.id, [obj.id for obj in all_objects])

        # Check if the City ID is in the list of all objects
        self.assertIn(city.id, [obj.id for obj in all_objects])

    def tests_all_with_states_and_cities(self):
        # Create instances of State and City
        state = State()
        city = City()

        # Save the instances to the storage
        self.fs.new(state)
        self.fs.new(city)
        self.fs.save()

        # Retrieve all instances using the modified all method
        all_objects = self.fs.all()
        print("All Objects:", all_objects)

        # Check if both instances are present in the result
        state_key = "{}.{}".format(state.__class__.__name__, state.id)
        city_key = "{}.{}".format(city.__class__.__name__, city.id)
        
        print("All Objects:", all_objects)
        print("State Key:", state_key)
        print("City Key:", city_key)
        self.assertIn(state_key, all_objects)
        self.assertIn(city_key, all_objects)


if __name__ == '__main__':
    unittest.main()

