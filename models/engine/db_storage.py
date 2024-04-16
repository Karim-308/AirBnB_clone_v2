#!/usr/bin/python3
"""
The DBStorage class 
"""

import models
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import environ
from os import getenv
from models.base_model import BaseModel
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """the MySQL database interaction interface"""
    __engine = None
    __session = None

    def __init__(self):
        """ Initialize DBStorage """
    def __init__(self):
        """ Initialize DBStorage """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST', 'localhost'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query objects depending on class name """
        obj_dict = {}
        if cls is None:
            cls_list = [User, State, City, Amenity, Place, Review]
        else:
            cls_list = [cls]

        for c in cls_list:
            objs = self.__session.query(c).all()
            for obj in objs:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[key] = obj

        return (obj_dict)

    def new(self, obj):
        """ Add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database and create the current database session """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()