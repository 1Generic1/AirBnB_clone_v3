#!/usr/bin/pyhton3
"""This module defines a class `Amenity`"""

from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String, ForeignKey
from models import storage_t


class Amenity(BaseModel, Base):
    '''Defines a Amenity'''
    if models.storage_t == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)

    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Return the string representation of the object."""
        state_dict = self.__dict__.copy()
        # Remove the '_sa_instance_state' attribute
        state_dict.pop('_sa_instance_state', None)
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, state_dict)
