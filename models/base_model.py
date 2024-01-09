#!/usr/bin/python3
"""This Module creates the class named BaseModel"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from sqlalchemy import Column, String, DateTime
import models


Base = declarative_base()

class BaseModel:
    """Defines all common attributes/methods for other classes"""
    

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid4())
            time_format = "%Y-%m-%dT%H:%M:%S.%f"
            if 'created_at' in kwargs:
                self.created_at = datetime.strptime(kwargs['created_at'], time_format)
            if 'updated_at' in kwargs:
                self.updated_at = datetime.strptime(kwargs['updated_at'], time_format)

    def __str__(self):
        """prints an instance of the object specified"""
        className = self.__class__.__name__
        selfId = self.id
        selfDict = self.__dict__

        return "[{}] ({}) {}".format(className, selfId, selfDict)

    def save(self):
        """updates the 'updated_at' attribute with current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the __dict__
           of the instance
        """
        dictionary = self.__dict__.copy()
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        dictionary.update({"__class__": self.__class__.__name__})
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()

        return dictionary

    def delete(self):
        """Delete the current instance from the storage"""
        models.storage.delete(self)
