#!/usr/bin/python3
"""This module create the class FileStorage"""
import json


class FileStorage():
    '''serializes instances to a JSON file and deserializes
       JSON file to instances
    '''
    __file_path = "file.json"
    __objects = {}
    
    def all(self, cls=None):
        '''returns the dict `__objects`'''
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        '''sets in `__objects` the `obj` with key `<obj class name>.id`'''
        name = obj.__class__.__name__
        key = f'{name}.{obj.id}'
        self.__objects[key] = obj

    def save(self):
        '''serializes `__objects` to the JSON file'''
        with open(self.__file_path, 'w') as file:
            dict_rep = {k: v.to_dict() for k, v in self.__objects.items()}
            json.dump(dict_rep, file)

    def reload(self):
        '''deserializes the JSON file to `__objects`'''
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        try:
            with open(self.__file_path, 'r', encoding="utf-8") as file:
                new_obj = json.load(file)
                for value in new_obj.values():
                    loaded_object = eval(value["__class__"])(**value)
                    self.new(loaded_object)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Delete the given object from the storage.
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

        # Check if obj is in the values of __objects
        if obj in self.__objects.values():
            # Find and remove the first occurrence of obj in values
            key_to_remove = next(
                k for k, v in self.__objects.items() if v == obj
            )
            del self.__objects[key_to_remove]

    def close(self):
        """
        Calls reload() method for deserializing the JSON file to objects.
        """
        self.reload()

    def get(self, cls, id):
        """
        Retrieve one object based on the class and its ID.

        Args:
            cls: Class representing the type of object to retrieve.
            id: String representing the object ID.

        Returns:
            The object based on the class and its ID, or None if not found.
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        Count the number of objects in storage matching the given class.
        If no class is passed, return the count of all objects in storage.

        Args:
            cls: Class (optional).

        Returns:
            The number of objects in storage.
        """

        all_classes = classes.values()

        if not cls:
            count = 0
            for class_obj in all_classes:
                count += len(models.storage.all(class_obj).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

