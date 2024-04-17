#!/usr/bin/python3
""" City Module for HBNB project """
import models
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship("Place", cascade="all, delete", backref="cities")
    else:
        state_id = ""
        name = ""

    # if models.storage_t != "db":
    #     @property
    #     def cities(self):
    #         """getter for list of city instances related to the state"""
    #         city_list = []
    #         all_cities = models.storage.all(City)
    #         for city in all_cities.values():
    #             if city.state_id == self.id:
    #                 city_list.append(city)
    #         return city_list

    # def __init__(self, *args, **kwargs):
    #     """initializes city"""
    #     super().__init__(*args, **kwargs)
