#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""

    def __init__(self, *args, **kwargs):
        '''the constructor'''
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)
        if kwargs:
            if len(kwargs) == 0:
                self.id = str(uuid.uuid4())
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
            else:
                regex_Str = "%Y-%m-%dT%H:%M:%S.%f"
                for key, value in kwargs.items():
                    if key == "created_at" or key == "updated_at":
                        setattr(self, key, datetime.strptime(value, regex_Str))
                    elif key == "__class__":
                        continue
                    else:
                        setattr(self, key, value)
        else:
                self.id = str(uuid.uuid4())
                self.created_at = datetime.utcnow()
                self.updated_at = self.created_at      

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary
   
    def delete(self): 
        """ delete the current instance from the storage """
        models.storage.delete(self)
