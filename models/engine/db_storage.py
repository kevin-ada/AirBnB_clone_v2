#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
from models.base_model import Base


class DBStorage:
    """"Representation of a DB storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """"Initialize a DB storage engine"""
        from os import getenv
        from sqlalchemy import create_engine
        from models.base_model import Base


        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, pwd, host, db),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):

        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review


        """Returns a dictionary of models currently in storage"""
        objects = dict()
        all_classes = (User, State, City, Amenity, Place, Review)
        if cls is None:
            for class_type in all_classes:
                query = self.__session.query(class_type)
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[obj_key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[obj_key] = obj
        return objects

    def new(self, obj):
        """Add the object to the current database session"""

        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Removes an object from the storage database"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        from sqlalchemy.orm import sessionmaker, scoped_session

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)
