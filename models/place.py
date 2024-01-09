#!/usr/bin/pyhton3
"""This module defines a class `Place`"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from models import storage_t
import models
from sqlalchemy.orm import relationship
from models.review import Review

if models.storage_t == 'db':
    place_amenity = Table(
                        'place_amenity',
                        Base.metadata,
                        Column('place_id', String(60),
                               ForeignKey('places.id', onupdate='CASCADE',
                                          ondelete='CASCADE'), nullable=False,
                                 primary_key=True),
                        Column('amenity_id', String(60),
                                 ForeignKey('amenities.id', onupdate='CASCADE',
                                            ondelete='CASCADE'), nullable=False,
                                 primary_key=True)
                          )


class Place(BaseModel, Base):
    '''Defines a Place'''
    if models.storage_t == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place", cascade="all, delete-orphan")
        amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)
    
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []
    
    if models.storage_t != 'db':
        @property
        def reviews(self):
            """getter attribute returns the list of Review instances"""
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """getter attribute returns the list of Amenity instances"""
            from models.amenity import Amenity
            amenity_list = []
            all_amenities = models.storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.place_id == self.id:
                    amenity_list.append(amenity)
            return amenity_list

    def __str__(self):
        """Return the string representation of the object."""
        state_dict = self.__dict__.copy()
        # Remove the '_sa_instance_state' attribute
        state_dict.pop('_sa_instance_state', None)
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, state_dict)

